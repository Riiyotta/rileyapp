import { createContext, useContext, useEffect, useState } from 'react'

// Minimal client router. Same-origin and rileyapp.com links route locally;
// other domains (app store onelinks etc.) navigate normally.
const INTERNAL_HOSTS = new Set([window.location.host, 'rileyapp.com', 'www.rileyapp.com'])
const RouterContext = createContext({ path: '/', navigate: () => {} })

export const usePath = () => useContext(RouterContext).path
export const useNavigate = () => useContext(RouterContext).navigate

const normalize = (p) => (p.length > 1 ? p.replace(/\/+$/, '') : p)

export function RouterProvider({ children }) {
  const [path, setPath] = useState(() => normalize(window.location.pathname))

  const navigate = (to) => {
    const url = new URL(to, window.location.origin)
    const next = normalize(url.pathname)
    window.history.pushState({}, '', next + url.search + url.hash)
    setPath(next)
    if (!url.hash) window.scrollTo(0, 0)
  }

  useEffect(() => {
    const onPop = () => setPath(normalize(window.location.pathname))
    const onClick = (e) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
      const a = e.target.closest('a[href]')
      if (!a || a.target === '_blank' || a.hasAttribute('download')) return
      const url = new URL(a.getAttribute('href'), window.location.href)
      if (!/^https?:$/.test(url.protocol) || !INTERNAL_HOSTS.has(url.host)) return
      e.preventDefault()
      navigate(url.pathname + url.search + url.hash)
    }
    window.addEventListener('popstate', onPop)
    document.addEventListener('click', onClick)
    return () => {
      window.removeEventListener('popstate', onPop)
      document.removeEventListener('click', onClick)
    }
  }, [])

  return <RouterContext.Provider value={{ path, navigate }}>{children}</RouterContext.Provider>
}
