import { useCallback, useEffect, useRef } from 'react'

// Port of embla-carousel v8's motion model (as shipped on rileyapp.com, chunk 8207-*.js) for a
// {loop:true} carousel of equal-width slides. Options used by the original are embla defaults:
// duration 25, dragFree false, skipSnaps false, dragThreshold 10.
//
// ScrollBody (fixed 60Hz step, render interpolation between previous and current location):
//   v += (target - location) / duration;  v *= friction;  location += v
// base duration 25, base friction 0.68; while dragging duration 0.75 / friction 0.3;
// after a drag: duration 25 - 10*boost, friction 0.68 + boost/50.
// Settles when |target - renderedLocation| < 0.001.
const STEP = 1000 / 60
const BASE_DURATION = 25
const BASE_FRICTION = 0.68
const DRAG_THRESHOLD = 10 // px before a drag cancels the click
const BASE_FORCE = { mouse: 300, touch: 400 }
const VELOCITY_WINDOW = 170 // ms

const sign = (n) => (n > 0 ? 1 : n < 0 ? -1 : 0)
const mod = (n, m) => ((n % m) + m) % m

export default function useEmblaLoop(count, { canDrag } = {}) {
  const viewportRef = useRef(null)
  const containerRef = useRef(null)
  const slideRefs = useRef([])
  const s = useRef({
    location: 0,
    previous: 0,
    offset: 0,
    target: 0,
    velocity: 0,
    duration: BASE_DURATION,
    friction: BASE_FRICTION,
    index: 0,
    raf: 0,
    last: null,
    acc: 0,
    pointer: null,
    preventClick: false,
  }).current

  const slideSize = () => {
    const a = slideRefs.current[0]
    const b = slideRefs.current[1]
    if (!a) return 1
    return b ? b.offsetLeft - a.offsetLeft : a.offsetWidth
  }

  const render = useCallback(
    (alpha) => {
      s.offset = s.location * alpha + s.previous * (1 - alpha)
      const size = slideSize()
      const content = size * count
      const container = containerRef.current
      if (container) container.style.transform = `translate3d(${Math.round(s.offset * 100) / 100}px, 0px, 0px)`
      // slide looper: keep each slide in [-size, content - size) relative to the viewport
      slideRefs.current.forEach((el, i) => {
        if (!el) return
        const x = i * size + s.offset
        const shift = x < -size ? Math.ceil((-size - x) / content) * content : x >= content - size ? -Math.ceil((x - (content - size) + 0.0001) / content) * content : 0
        el.style.transform = shift ? `translate3d(${shift}px, 0px, 0px)` : 'translate3d(0px, 0px, 0px)'
      })
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [count],
  )

  const update = () => {
    const diff = s.target - s.location
    const from = s.location
    if (s.duration) {
      s.previous = s.location
      s.velocity += diff / s.duration
      s.velocity *= s.friction
      s.location += s.velocity
    } else {
      s.velocity = 0
      s.previous = s.target
      s.location = s.target
    }
    // scroll looper (embla ScrollLooper): shift all positions by the content length (visually a no-op) only
    // when moving past the limit in that direction, with embla's 0.1px joint safety.
    const dir = sign(s.duration ? s.location - from : diff)
    const content = slideSize() * count
    const shift = dir === 1 && s.location > 0.1 ? -content : dir === -1 && s.location < -content + 0.1 ? content : 0
    if (shift) {
      s.location += shift
      s.previous += shift
      s.target += shift
      if (s.pointer) s.pointer.base += shift
    }
  }

  const settled = () => Math.abs(s.target - s.offset) < 0.001

  const tick = (ts) => {
    if (!s.raf) return
    if (s.last === null) {
      s.last = ts
      update()
      update()
    }
    const dt = ts - s.last
    s.last = ts
    s.acc += dt
    while (s.acc >= STEP) {
      update()
      s.acc -= STEP
    }
    render(s.acc / STEP)
    if (settled() && !s.pointer) {
      stop()
      return
    }
    s.raf = requestAnimationFrame(tick)
  }
  const start = () => {
    if (!s.raf) s.raf = requestAnimationFrame(tick)
  }
  const stop = () => {
    cancelAnimationFrame(s.raf)
    s.raf = 0
    s.last = null
    s.acc = 0
  }

  // shortest loop distance to snap of `index` from the current target, optionally constrained to a direction
  const distanceToIndex = (index, direction) => {
    const content = slideSize() * count
    const d = -index * slideSize() - s.target
    const options = [d, d + content, d - content]
    const byAbs = (list) => list.slice().sort((a, b) => Math.abs(a) - Math.abs(b))[0]
    if (!direction) return byAbs(options)
    const same = options.filter((o) => sign(o) === direction)
    return same.length ? byAbs(same) : Math.max(...options) - content
  }
  const nearestIndex = (location) => mod(Math.round(-location / slideSize()), count)

  const scrollBy = (distance, index) => {
    s.target += distance
    if (distance) start()
    s.index = index
  }

  const scrollTo = useCallback((delta) => {
    s.duration = BASE_DURATION
    s.friction = BASE_FRICTION
    const index = mod(s.index + delta, count)
    scrollBy(distanceToIndex(index, -sign(delta)), index)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [count])

  const next = useCallback(() => scrollTo(1), [scrollTo])
  const prev = useCallback(() => scrollTo(-1), [scrollTo])

  // ---- drag (embla DragHandler + DragTracker) ----
  const onPointerDown = (e) => {
    const isMouse = e.pointerType === 'mouse'
    if (isMouse && e.button !== 0) return
    if (canDrag && !canDrag(e)) return
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.nodeName)) return
    s.preventClick = false
    s.duration = 0
    s.friction = 0
    s.target = s.location
    s.pointer = { id: e.pointerId, isMouse, startX: e.clientX, startY: e.clientY, lastX: e.clientX, first: { x: e.clientX, t: e.timeStamp }, last: { x: e.clientX, t: e.timeStamp }, horizontal: isMouse ? true : null, base: 0 }
    try {
      e.currentTarget.setPointerCapture(e.pointerId)
    } catch {
      /* synthetic or already-released pointer */
    }
  }

  const onPointerMove = (e) => {
    const p = s.pointer
    if (!p || p.id !== e.pointerId) return
    if (p.horizontal === null) {
      const dx = Math.abs(e.clientX - p.startX)
      const dy = Math.abs(e.clientY - p.startY)
      if (!dx && !dy) return
      p.horizontal = dx > dy
    }
    if (!p.horizontal) return
    const diff = e.clientX - p.last.x
    if (e.timeStamp - p.first.t > VELOCITY_WINDOW) p.first = { x: e.clientX, t: e.timeStamp }
    p.last = { x: e.clientX, t: e.timeStamp }
    if (Math.abs(e.clientX - p.startX) > DRAG_THRESHOLD) s.preventClick = true
    s.duration = 0.75
    s.friction = 0.3
    start()
    s.target += diff
    if (e.cancelable) e.preventDefault()
  }

  const onPointerUp = (e) => {
    const p = s.pointer
    if (!p || p.id !== e.pointerId) return
    s.pointer = null
    // DragTracker.pointerUp: px/ms over the last <=170ms, 0 if stale or tiny
    const dx = p.last.x - p.first.x
    const dt = e.timeStamp - p.first.t
    const stale = e.timeStamp - p.last.t > VELOCITY_WINDOW
    const v = dx / dt
    const velocity = dt && !stale && Math.abs(v) > 0.1 ? v : 0
    const force = velocity * (p.isMouse ? BASE_FORCE.mouse : BASE_FORCE.touch)
    const viewport = viewportRef.current?.offsetWidth || 0
    const minForce = Math.min(Math.max(viewport * 0.2, 50), 225)
    let distance
    let index
    if (Math.abs(force) < minForce) {
      // snap to the slide nearest to target + force
      const l = s.target + force
      index = nearestIndex(l)
      const d = -index * slideSize() - l
      const content = slideSize() * count
      const snapDiff = [d, d + content, d - content].sort((a, b) => Math.abs(a) - Math.abs(b))[0]
      distance = force + snapDiff
    } else {
      index = mod(s.index - sign(force), count)
      distance = distanceToIndex(index, 0)
    }
    const boost = !force || !distance || Math.abs(force) <= Math.abs(distance) ? 0 : Math.abs((Math.abs(force) - Math.abs(distance)) / force)
    s.duration = BASE_DURATION - 10 * boost
    s.friction = BASE_FRICTION + boost / 50
    scrollBy(distance, index)
    start()
  }

  const onClickCapture = (e) => {
    if (s.preventClick) {
      e.stopPropagation()
      e.preventDefault()
      s.preventClick = false
    }
  }

  // initial render + keep pixel positions valid on resize (embla reInit keeps the selected index)
  useEffect(() => {
    render(1)
    const ro = new ResizeObserver(() => {
      stop()
      s.velocity = 0
      s.location = s.previous = s.target = -s.index * slideSize()
      render(1)
    })
    if (viewportRef.current) ro.observe(viewportRef.current)
    return () => {
      ro.disconnect()
      stop()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [render])

  return {
    viewportRef,
    containerRef,
    slideRef: (i) => (el) => {
      slideRefs.current[i] = el
    },
    next,
    prev,
    viewportProps: {
      ref: viewportRef,
      onPointerDown,
      onPointerMove,
      onPointerUp,
      onPointerCancel: onPointerUp,
      onClickCapture,
      onDragStart: (e) => e.preventDefault(),
    },
  }
}
