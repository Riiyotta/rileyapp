import CategoryTag from './CategoryTag.jsx'
import { postHref } from './categories.js'

const ReadMore = () => (
  <div className="flex items-center gap-4">
    <span className="font-sans-bold text-base leading-6 text-ink">Read more</span>
    <img src="/assets/blog/icons/read-more-chevron.svg" alt="" width="6" height="11" />
  </div>
)

const Author = ({ post }) => (
  <div className="flex items-center gap-4">
    <img src={post.authorImage} alt={post.author} width="48" height="48" className="h-12 w-12 rounded-full" />
    <div>
      <p className="font-sans-bold text-base leading-6 text-text-primary">{post.author}</p>
      <div className="text-base leading-6 text-text-primary">{post.authorTitle}</div>
    </div>
  </div>
)

// Blog spec §2.5(a): horizontal banner >=992, stacked card <992. Both rendered; CSS toggles.
export default function BlogFeaturedCard({ post }) {
  const href = postHref(post)
  return (
    <div className="col-span-full">
      <div className="bg-blogFeature group hidden items-center justify-between self-stretch overflow-hidden rounded-3xl bg-white lg:flex">
        <a href={href} className="group flex flex-1 items-center gap-4">
          <div className="flex flex-1 flex-col items-start gap-8 self-stretch px-[3.75rem] py-[2.5rem]">
            <div className="flex flex-col items-start gap-5">
              <CategoryTag post={post} size="large" />
              <h2 className="mb-2 font-sans-bold text-[30px] leading-[36px] text-text-primary transition-all duration-300">
                {post.title}
              </h2>
            </div>
            <Author post={post} />
            <p className="text-base leading-6 text-text-primary">{post.excerpt}</p>
            <ReadMore />
          </div>
          <div className="flex w-full max-w-full flex-1 flex-col items-start self-stretch">
            <img src={post.image} alt={post.imageAlt || ''} className="h-48 w-full flex-1 self-stretch object-cover md:h-[400px]" />
          </div>
        </a>
      </div>
      <div className="bg-blogFeature group flex flex-col items-start gap-8 self-stretch overflow-hidden rounded-3xl bg-white pb-8 lg:hidden">
        <a href={href} className="flex w-full flex-col items-center gap-4">
          <div className="flex max-h-[28rem] w-full flex-col items-start self-stretch overflow-hidden">
            <img src={post.image} alt={post.imageAlt || ''} className="w-full flex-1 self-stretch object-cover" />
          </div>
          <div className="flex flex-col items-start gap-6 self-stretch px-6">
            <CategoryTag post={post} size="large" />
            <div className="flex flex-col items-start gap-6">
              <h2 className="font-sans-bold text-[24px] leading-[32px] text-text-primary">{post.title}</h2>
              <Author post={post} />
              <p className="text-base leading-6 text-text-primary">{post.excerpt}</p>
            </div>
            <ReadMore />
          </div>
        </a>
      </div>
    </div>
  )
}
