import HomePage from './HomePage.jsx'
import PricingPage from './PricingPage.jsx'
import BlogIndexPage from './BlogIndexPage.jsx'
import BlogCategoryPage from './BlogCategoryPage.jsx'
import BlogArticlePage from './BlogArticlePage.jsx'
import TextPage from './TextPage.jsx'
import LegalPage from './LegalPage.jsx'

// Route table: exact paths first, then pattern matchers (checked in order).
// Each page component owns its own header/footer composition.
// Dead sitemap slugs (/baby-tracker etc.) deliberately have no route: they 404 on the original too.
export const exactRoutes = {
  '/': HomePage,
  '/pricing': PricingPage,
  '/blog': BlogIndexPage,
  '/editorial-process': TextPage,
  '/tos': () => <LegalPage kind="tos" />,
  '/privacy': () => <LegalPage kind="privacy" />,
  '/cookies': () => <LegalPage kind="cookies" />,
}

export const patternRoutes = [
  { test: /^\/blog\/(development|feeding|health|news|pregnancy|sleep)$/, component: BlogCategoryPage },
  // Unknown slugs fall back to NotFound inside BlogArticlePage.
  { test: /^\/blog\/([^/]+)\/([^/]+)$/, component: BlogArticlePage },
]
