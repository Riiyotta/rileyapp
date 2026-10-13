import { useEffect, useState } from 'react'
import { usePath } from '../../router.jsx'

// The router only tracks pathname, so /blog -> /blog?page=2 doesn't re-render.
// Patch pushState/replaceState once to emit an event, then re-read location.search
// on path change, popstate and that event.
const EVENT = 'blog:locationchange'
if (typeof window !== 'undefined' && !window.history.__blogPatched) {
  for (const m of ['pushState', 'replaceState']) {
    const orig = window.history[m]
    window.history[m] = function (...args) {
      const r = orig.apply(this, args)
      window.dispatchEvent(new Event(EVENT))
      return r
    }
  }
  window.history.__blogPatched = true
}

export function useLocationSearch() {
  const path = usePath()
  const [search, setSearch] = useState(() => window.location.search)
  useEffect(() => {
    const read = () => setSearch(window.location.search)
    read()
    window.addEventListener('popstate', read)
    window.addEventListener(EVENT, read)
    return () => {
      window.removeEventListener('popstate', read)
      window.removeEventListener(EVENT, read)
    }
  }, [path])
  return search
}

export function useSearchParam(name) {
  const search = useLocationSearch()
  return new URLSearchParams(search).get(name)
}
