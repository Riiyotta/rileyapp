import { useEffect, useLayoutEffect, useRef, useState } from 'react'

// §2.6 Hero parallax clouds + motion §14 M3 (horizontal float) / M3b (scroll parallax)
const C1 = { src: '/assets/icons/hero-cloud-1.svg', w: 411, h: 251 }
const C2 = { src: '/assets/icons/hero-cloud-2.svg', w: 592, h: 362 }
const C3 = { src: '/assets/icons/hero-cloud-3.svg', w: 411, h: 251 }
const C4 = { src: '/assets/icons/hero-cloud-4.svg', w: 592, h: 362 }

// Each cloud is rendered as a pair: one normal + one `.cloud-alt` (negative delay).
const pair = (cloud, cls) => [
  { cloud, cls: `${cls}` },
  { cloud, cls: `${cls} cloud-alt` },
]

const LAYERS = [
  {
    range: 20,
    expanded: true,
    wrapper: 'absolute inset-0',
    banner: 'bg-hero',
    clouds: pair(C1, 'animate-float-slow absolute -right-40 top-10'),
  },
  {
    range: 35,
    expanded: true,
    wrapper: 'pointer-events-none absolute inset-0 -z-50',
    banner: 'bg-transparent',
    clouds: [
      ...pair(C2, 'animate-float-medium -left-[120px] top-[120px] absolute'),
      ...pair(C3, 'animate-float-medium absolute top-1/2'),
    ],
  },
  {
    range: 50,
    expanded: true,
    wrapper: 'pointer-events-none absolute inset-0 -z-30',
    banner: 'bg-transparent',
    clouds: [
      ...pair(C1, 'animate-float-fast -left-[120px] absolute bottom-20'),
      ...pair(C3, 'animate-float-fast absolute -right-40'),
    ],
  },
  {
    range: 100,
    expanded: false,
    scale: [0.8, 1.2],
    wrapper: 'pointer-events-none absolute inset-0 -z-10',
    banner: 'bg-transparent',
    innerStyle: { transform: 'translateY(25%)' },
    clouds: [
      { cloud: C4, cls: 'animate-float-fast absolute -left-20' },
      { cloud: C4, cls: 'animate-float-fast cloud-alt absolute left-20' },
    ],
  },
]

const layerTransform = (layer, p) => {
  const t = `translateY(${-layer.range * p}%)`
  if (!layer.scale) return t
  const [s0, s1] = layer.scale
  return `${t} scale(${s0 + (s1 - s0) * p})`
}

// Defaults = homepage. /pricing (marketing spec §1.4) passes withBg={false} (no bg-hero, all layer wrappers
// plain `absolute inset-0`) and its own root className. Progress target is always the root's parent element
// (the homepage Hero wrapper, or the PricingHero section).
export default function HeroParallaxClouds({ withBg = true, className = 'absolute inset-0 w-full' }) {
  const rootRef = useRef(null)
  const layerRefs = useRef([])
  const [bannerHeight, setBannerHeight] = useState(0)

  // Expanded layers are inset by -(range% of banner height) at the top. The original (react-scroll-parallax
  // ParallaxBanner) reads the banner rect once at hydration, before final layout, and never updates it. That
  // frozen height is deterministic on rileyapp.com: 992px at >=1024, settled height + 82.06px at 768-1023,
  // settled height + 51.30px below 768 (measured 320-1920). Homepage only; /pricing keeps the settled height.
  useLayoutEffect(() => {
    const el = rootRef.current
    if (!el) return undefined
    const hydrationHeight = (h) => {
      if (!withBg) return h
      const w = window.innerWidth
      return w >= 1024 ? 992 : w >= 768 ? h + 82.06 : h + 51.3
    }
    const measure = () => setBannerHeight(hydrationHeight(el.offsetHeight))
    measure()
    const ro = new ResizeObserver(measure)
    ro.observe(el)
    return () => ro.disconnect()
  }, [withBg])

  // p = clamp(scrollY / (heroTop + heroHeight), 0, 1)
  useEffect(() => {
    let frame = 0
    const update = () => {
      frame = 0
      const hero = rootRef.current?.parentElement
      if (!hero) return
      const heroTop = hero.getBoundingClientRect().top + window.scrollY
      const end = heroTop + hero.offsetHeight
      const p = end > 0 ? Math.min(Math.max(window.scrollY / end, 0), 1) : 0
      LAYERS.forEach((layer, i) => {
        const node = layerRefs.current[i]
        if (node) node.style.transform = layerTransform(layer, p)
      })
    }
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update)
    }
    update()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      if (frame) cancelAnimationFrame(frame)
    }
  }, [])

  return (
    <div ref={rootRef} className={className}>
      {LAYERS.map((layer, i) => (
        <div key={i} className={withBg ? layer.wrapper : 'absolute inset-0'}>
          <div className={`${withBg ? layer.banner : ''} h-full w-full`} style={{ position: 'relative', overflow: 'hidden', width: '100%' }}>
            <div
              ref={(n) => (layerRefs.current[i] = n)}
              style={{
                position: 'absolute',
                inset: `${layer.expanded ? -(layer.range / 100) * bannerHeight : 0}px 0px 0px`,
                willChange: 'transform',
                transform: layerTransform(layer, 0),
              }}
            >
              <div className="absolute inset-0 h-full" style={layer.innerStyle}>
                {layer.clouds.map(({ cloud, cls }, j) => (
                  <div key={j} className={`cloud-wrapper ${cls}`}>
                    <img src={cloud.src} width={cloud.w} height={cloud.h} className="max-w-none" alt="" aria-hidden="true" draggable="false" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
