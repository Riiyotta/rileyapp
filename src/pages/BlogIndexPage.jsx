import { useEffect } from 'react'
import posts from '../data/blogPosts.json'
import AnnouncementBar from '../components/AnnouncementBar.jsx'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import FinalCta from '../components/FinalCta.jsx'
import SiteFooter from '../components/SiteFooter.jsx'
import BlogIndexHero from '../components/blog/BlogIndexHero.jsx'
import BlogSearch from '../components/blog/BlogSearch.jsx'
import BlogCategoryTabs from '../components/blog/BlogCategoryTabs.jsx'
import BlogFeaturedCard from '../components/blog/BlogFeaturedCard.jsx'
import BlogPostCard from '../components/blog/BlogPostCard.jsx'
import BlogPagination from '../components/blog/BlogPagination.jsx'
import { getCategory } from '../components/blog/categories.js'
import { useSearchParam } from '../components/blog/useSearchParam.js'

const PAGE_SIZE = 6
const bySlug = Object.fromEntries(posts.map((p) => [p.slug, p]))

// Blog spec §2.7: fixed featured set per listing (banner + cards, card order = placement order).
const FEATURED = {
  blog: { hero: 'why-we-built-riley', cards: ['introducing-golden-window', 'welcome-dr-lilly-jay'] },
  sleep: { hero: '1-month-old-sleep-guide', cards: ['what-is-newborn-day-night-confusion', 'when-do-babies-start-sleeping-through-the-night'] },
  development: { hero: 'how-to-play-with-your-newborn', cards: ['when-do-babies-start-crawling', 'understanding-baby-growth-charts'] },
  feeding: { hero: 'night-feedings-when-and-how-to-wean', cards: ['6-month-old-feeding-schedule', 'baby-feeding-schedules'] },
  news: { hero: 'why-we-built-riley', cards: ['welcome-dr-lilly-jay', 'introducing-golden-window'] },
  health: null,
  pregnancy: null,
}

// The paginated /blog list leaves out the three blog-featured posts (banner + 2 placement cards): measured on the
// original, ?page=36/37 are shifted accordingly and the last page holds 2 posts (218 listed → 37 pages).
const BLOG_FEATURED = new Set([FEATURED.blog.hero, ...FEATURED.blog.cards])
const allPosts = [...posts].sort((a, b) => a.order - b.order).filter((p) => !BLOG_FEATURED.has(p.slug))

// /blog, /blog?page=N and (via `category`) /blog/<category>. Spec §1.1, §1.2, §2.
export default function BlogIndexPage({ category = null }) {
  const pageParam = useSearchParam('page')
  const isCategory = Boolean(category)

  const totalPages = isCategory ? 1 : Math.ceil(allPosts.length / PAGE_SIZE)
  const parsed = parseInt(pageParam, 10)
  const page = isCategory ? 1 : Number.isFinite(parsed) && parsed >= 1 ? parsed : 1

  const featured = FEATURED[category || 'blog']
  const hero = featured ? bySlug[featured.hero] : null
  const placementCards = featured ? featured.cards.map((s) => bySlug[s]) : []
  const pagePosts = isCategory ? [] : allPosts.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)
  const cards = [
    ...placementCards.map((post) => ({ post, authorLink: true })),
    ...pagePosts.map((post) => ({ post, authorLink: false })),
  ]

  useEffect(() => {
    document.title = isCategory ? `${getCategory(category).title} - Blog | Riley` : 'Riley Articles | Riley'
  }, [category, isCategory])

  const content = (
    <div className="mb-8 flex w-full flex-col items-center justify-center gap-8 px-4 md:px-8 lg:px-16">
      <div className="mt-[5rem] flex w-full max-w-[90rem] flex-col items-center gap-4 md:gap-[5rem]">
        <BlogIndexHero />
        <BlogSearch />
        <div className="w-full">
          <BlogCategoryTabs active={category || 'all'} />
          <div className="grid grid-cols-1 gap-8">
            {hero && <BlogFeaturedCard post={hero} />}
            {cards.length > 0 && (
              <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
                {cards.map(({ post, authorLink }, i) => (
                  <div key={post.slug} className={i === 0 ? 'col-span-1 lg:col-span-2' : 'col-span-1'}>
                    <BlogPostCard post={post} variant={i === 0 ? 'wide' : 'normal'} authorLink={authorLink} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
  const pagination = <BlogPagination page={page} totalPages={totalPages} />

  // Category pages use a different wrapper on the original (measured): one `mb-[4rem] flex flex-col items-center
  // self-stretch` column holding header, content, pagination, FinalCta AND footer, with no gap-[5rem] between content
  // and pagination; the 64px bottom margin therefore lands after the footer.
  if (isCategory) {
    return (
      <div className="relative flex flex-col items-start overflow-hidden">
        <div className="mb-[4rem] flex flex-col items-center self-stretch">
          <SiteHeader />
          {content}
          {pagination}
          <FinalCta />
          <SiteFooter />
        </div>
      </div>
    )
  }

  return (
    <>
      <AnnouncementBar />
      <div className="relative flex flex-col items-start overflow-hidden">
        <SiteHeader />
        <div className="mb-[4rem] flex flex-col items-center gap-[5rem] self-stretch">
          {content}
          {pagination}
        </div>
        <FinalCta />
        <SiteFooter />
      </div>
    </>
  )
}
