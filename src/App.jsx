import { RouterProvider, usePath } from './router.jsx'
import { exactRoutes, patternRoutes } from './pages/routes.jsx'
import NotFound from './pages/NotFound.jsx'
import CookieConsent from './components/blog/CookieConsent.jsx'

function Routes() {
  const path = usePath()
  const Exact = exactRoutes[path]
  if (Exact) return <Exact />
  for (const r of patternRoutes) {
    const m = path.match(r.test)
    if (m) return <r.component params={m.slice(1)} />
  }
  return <NotFound />
}

export default function App() {
  return (
    <RouterProvider>
      <Routes />
      <CookieConsent />
    </RouterProvider>
  )
}
