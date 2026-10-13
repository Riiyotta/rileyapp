// Blog spec §0.2: CategoryTag map (bg colour + icon per category) and §2.4 tab order.
export const CATEGORIES = {
  sleep: { title: 'Sleep', bg: '#EACDFF', icon: '/assets/blog/icons/moon.svg' },
  feeding: { title: 'Feeding', bg: '#FFEAA7', icon: '/assets/blog/icons/bowl.svg' },
  development: { title: 'Development', bg: '#E0FFE0', icon: '/assets/blog/icons/duck.svg' },
  news: { title: 'News', bg: '#CFF6FF', icon: '/assets/blog/icons/lightbulb.svg' },
  health: { title: 'Health', bg: '#FFC7C3', icon: '/assets/blog/icons/first-aid.svg' },
  pregnancy: { title: 'Pregnancy', bg: '#8DE8B2', icon: '/assets/blog/icons/octopus.svg' },
}

// default: gray-200 bg, no icon
export const DEFAULT_CATEGORY = { title: '', bg: '#e5e7eb', icon: null }

export const getCategory = (slug) => CATEGORIES[slug] || DEFAULT_CATEGORY

// §2.4 tab order (from /api/get-blog-categories on the original)
export const BLOG_TABS = [
  { key: 'all', label: 'All', href: '/blog' },
  { key: 'feeding', label: 'Feeding', href: '/blog/feeding' },
  { key: 'pregnancy', label: 'Pregnancy', href: '/blog/pregnancy' },
  { key: 'sleep', label: 'Sleep', href: '/blog/sleep' },
  { key: 'health', label: 'Health', href: '/blog/health' },
  { key: 'development', label: 'Development', href: '/blog/development' },
  { key: 'news', label: 'News', href: '/blog/news' },
  { key: 'authors', label: 'Authors', href: '/blog/authors' },
]

export const postHref = (post) => `/blog/${post.category}/${post.slug}`

// §0.5: `updatedAt` in the viewer's local timezone, en-GB short month, no comma ("8 Apr 2025").
const dateFmt = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
// Chrome's en-GB gives "Sept"; the original renders "Sep" (measured: "Updated: 24 Sep 2025").
export const formatPostDate = (iso) => (iso ? dateFmt.format(new Date(iso)).replace('Sept', 'Sep') : null)

// The original's <992 article header shows the server-rendered (UTC) date while the ≥992 header shows the viewer's
// local date (measured in IST: mobile "Updated: 23 Jul 2025" vs desktop "24 Jul 2025" for 2025-07-23T19:41Z).
const dateFmtUTC = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
export const formatPostDateUTC = (iso) => (iso ? dateFmtUTC.format(new Date(iso)).replace('Sept', 'Sep') : null)
