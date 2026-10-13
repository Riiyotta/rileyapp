import { usePath } from '../router.jsx'
import BlogIndexPage from './BlogIndexPage.jsx'

// /blog/<category> (development, feeding, health, news, pregnancy, sleep). Spec §1.2:
// same template, no AnnouncementBar, only that category's featured set, "Page 1 of 1".
// Category comes from the `category` prop, route params[0], or the current path.
export default function BlogCategoryPage({ category, params }) {
  const path = usePath()
  const slug = category || params?.[0] || path.split('/')[2]
  return <BlogIndexPage category={slug} />
}
