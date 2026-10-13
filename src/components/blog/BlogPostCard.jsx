import CategoryTag from './CategoryTag.jsx'
import { formatPostDate, postHref } from './categories.js'

// Blog spec §2.5(b). variant: 'wide' (first grid item, 30/36 title, 4-line excerpt) | 'normal' (24/32, 3 lines).
// authorLink: true on the featured "placement" cards, where the author name links to /blog/author/<slug>.
// The live DOM really nests that author <a> inside the card <a> (verified on /blog), so React's dev-only
// validateDOMNesting warning is the cost of matching it.
export default function BlogPostCard({ post, variant = 'normal', authorLink = false, className = '' }) {
  const wide = variant === 'wide'
  const date = formatPostDate(post.date)
  return (
    <div className={`group flex h-full flex-col items-start gap-8 self-stretch overflow-hidden rounded-3xl bg-white ${className}`}>
      <a href={postHref(post)} className="flex w-full flex-col gap-8">
        <div className="flex w-full flex-col items-start self-stretch">
          <img src={post.image} alt={post.imageAlt || ''} loading="lazy" className="h-48 w-full object-cover lg:h-[16rem]" />
        </div>
        <div className="flex flex-1 flex-col items-start justify-between gap-5 self-stretch px-6 pb-8 md:px-10">
          <div className="flex flex-col items-start gap-3 self-stretch">
            <div className="flex items-center gap-6">
              {date && <p className="text-base leading-6 text-text-primary">{date}</p>}
              {date && post.readTime && <p className="text-base leading-6 text-text-primary">{post.readTime} min read</p>}
            </div>
            <h2
              className={`mb-2 font-sans-regular text-text-primary transition-all duration-300 ${
                wide ? 'text-[30px] leading-[36px]' : 'text-[24px] leading-[32px]'
              }`}
            >
              {post.title}
            </h2>
          </div>
          <p className={`self-stretch text-base leading-6 text-text-primary ${wide ? 'line-clamp-4' : 'line-clamp-3'}`}>{post.excerpt}</p>
          <div className="flex flex-col gap-1 self-stretch">
            <div className="flex items-center gap-3 text-base leading-6 text-text-primary">
              <span>By</span>
              {authorLink ? (
                <a href={`/blog/author/${post.authorSlug}`} className="transition-colors duration-200">
                  {post.author}
                </a>
              ) : (
                <span>{post.author}</span>
              )}
            </div>
            <div className="text-base leading-6">
              <span className="text-text-primary">{post.authorTitle}</span>
            </div>
          </div>
          <CategoryTag post={post} size="small" />
        </div>
      </a>
    </div>
  )
}
