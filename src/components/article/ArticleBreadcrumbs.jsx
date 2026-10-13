import { getCategory } from '../blog/categories.js'
import MaskIcon from './MaskIcon.jsx'

// Blog spec §3.3 (desktop) / §3.4 (mobile: no "Blog" crumb, no first chevron).
// The original uses `space-x-3` on the ol; `gap-3` gives the same 12px spacing without a leading margin
// when the first li is display:none (<992). The pill shows the CMS `seoTitle` field (stored as `crumbTitle`), not the full title.
// Original markup: li[Blog] · li[chevron (lg only), category] · li[chevron, pill]. The chevron lives in the same li as
// the item after it, and is shrinkable like the original inline svg (it narrows to 14.9px beside a wrapping pill).
const Chevron = ({ className = '' }) => (
  <MaskIcon src="/assets/blog/icons/breadcrumb-chevron.svg" size={16} color="#99a1af" shrink className={className} />
)

export default function ArticleBreadcrumbs({ post }) {
  const cat = getCategory(post.category)
  return (
    <nav aria-label="Breadcrumb">
      <ol className="flex items-center gap-3">
        <li className="hidden items-center gap-3 lg:flex">
          <a href="/blog" className="text-base leading-6 text-text-primary hover:text-gray-700">Blog</a>
        </li>
        <li className="flex items-center gap-3">
          <Chevron className="hidden lg:block" />
          <a href={`/blog/${post.category}`} className="text-base leading-6 text-text-primary hover:text-gray-700">
            {post.categoryTitle || cat.title}
          </a>
        </li>
        <li className="flex items-center gap-3">
          <Chevron />
          <span className="rounded-full px-6 py-2 text-base leading-6 text-text-primary" style={{ backgroundColor: cat.bg }} aria-current="page">
            {post.crumbTitle || post.title}
          </span>
        </li>
      </ol>
    </nav>
  )
}
