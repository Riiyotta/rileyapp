import { formatPostDate, formatPostDateUTC } from '../blog/categories.js'
import ArticleBreadcrumbs from './ArticleBreadcrumbs.jsx'
import ShareButtons from './ShareButtons.jsx'
import AuthorByline from './AuthorByline.jsx'

// Blog spec §3.3 (desktop ≥992) and §3.4 (mobile/tablet <992). Two separate markups, as on the original.
function Bylines({ post, reviewer = true }) {
  return (
    <>
      <AuthorByline
        label="Written by:"
        name={post.author}
        title={post.authorTitle}
        image={post.authorImage}
        href={`/blog/author/${post.authorSlug}`}
      />
      {reviewer && post.reviewer && (
        <AuthorByline
          label="Reviewed by:"
          name={post.reviewer}
          title={post.reviewerTitle}
          image={post.reviewerImage}
          href={`/blog/reviewer/${post.reviewerSlug}`}
        />
      )}
    </>
  )
}

export function ArticleHeaderDesktop({ post, shareUrl }) {
  const updated = formatPostDate(post.updatedAt)
  return (
    <div className="hidden flex-col items-center gap-[4.5rem] self-stretch lg:flex lg:max-xl:px-[6.5rem] xl:px-[13rem]">
      <div className="flex flex-col items-center justify-center gap-8 self-stretch">
        <div className="flex w-full items-start justify-between self-stretch">
          <ArticleBreadcrumbs post={post} />
          <ShareButtons variant="top" url={shareUrl} title={post.title} />
        </div>
        <div className="flex flex-col items-start gap-4 self-stretch">
          <h1 className="w-full text-left text-text-primary">{post.title}</h1>
          <h3 className="text-base leading-[1.575rem] text-text-primary">{post.excerpt}</h3>
        </div>
        <div className="flex w-full items-start justify-between">
          <div className="flex flex-1 items-end gap-4">
            <Bylines post={post} />
          </div>
          <div className="flex flex-col items-end justify-center gap-2 text-base leading-6">
            {updated && <p className="text-text-primary">Updated: {updated}</p>}
            {post.readTime && <p className="text-ink">{post.readTime} min read</p>}
          </div>
        </div>
      </div>
      {/* hero sits in the outer gap-72 column, not the gap-32 one (measured: meta row bottom → hero = 72) */}
      <div className="flex items-start self-stretch">
        <div className="flex max-h-[30rem] flex-1 flex-col items-center justify-center overflow-hidden rounded-2xl">
          <img src={post.image} alt={post.imageAlt || ''} className="h-auto self-stretch" />
        </div>
      </div>
    </div>
  )
}

export function ArticleHeaderMobile({ post }) {
  const updated = formatPostDateUTC(post.updatedAt)
  return (
    <div className="flex flex-col items-start gap-[4.5rem] self-stretch lg:hidden">
      <div className="flex flex-col items-center justify-center gap-8 self-stretch">
        <div className="flex w-full items-start justify-between self-stretch">
          <ArticleBreadcrumbs post={post} />
        </div>
        <h1 className="h1-mobile self-stretch text-text-primary">{post.title}</h1>
        <div className="flex flex-col items-start gap-8">
          <div className="flex h-[16.5rem] w-full flex-col items-start justify-center overflow-hidden rounded-2xl">
            <img src={post.image} alt={post.imageAlt || ''} className="h-auto w-full self-stretch object-cover" />
          </div>
          <h3 className="text-base leading-[1.575rem] text-text-primary">{post.excerpt}</h3>
        </div>
        <div className="flex w-full items-center justify-between text-base leading-6">
          {updated && <p className="text-text-primary">Updated: {updated}</p>}
          {post.readTime && <p className="text-ink">{post.readTime} min read</p>}
        </div>
        {/* <992 the original renders only the author byline (no reviewer) */}
        <div className="flex flex-col items-start justify-end gap-4 self-stretch">
          <Bylines post={post} reviewer={false} />
        </div>
      </div>
    </div>
  )
}

export default function ArticleHeader({ post, shareUrl }) {
  return (
    <>
      <ArticleHeaderDesktop post={post} shareUrl={shareUrl} />
      <ArticleHeaderMobile post={post} />
    </>
  )
}
