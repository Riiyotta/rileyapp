import { useEffect, useState } from 'react'
import Button from './shared/Button.jsx'

// §11 BlogTeaser
const CATEGORIES = [
  { title: 'Development', slug: 'development', bg: 'bg-pill-development' },
  { title: 'Feeding', slug: 'feeding', bg: 'bg-pill-neutral' },
  { title: 'Health', slug: 'health', bg: 'bg-pill-health' },
  { title: 'News', slug: 'news', bg: 'bg-pill-neutral' },
  { title: 'Pregnancy', slug: 'pregnancy', bg: 'bg-pill-neutral' },
  { title: 'Sleep', slug: 'sleep', bg: 'bg-pill-sleep' },
]

const POSTS = [
  {
    title: 'Baby Witching Hour: What It Is, When and Why It Happens, and How to Manage It',
    href: 'https://rileyapp.com/blog/sleep/baby-witching-hour',
    img: '/assets/3dd009c0c3295127b2b277b3920acb6868836cd9-5760x3840.jpeg',
    alt: 'Baby Witching Hour: What It Is, When and Why It Happens, and How to Manage It',
  },
  {
    title: '1 Month Old Sleep Guide: Bedtime and Nap Schedules',
    href: 'https://rileyapp.com/blog/sleep/1-month-old-sleep-guide',
    img: '/assets/6ec23763ba2e30df4af542e28148a465ef27d13a-5744x3829.jpeg',
    alt: 'Tired young mom holds her one month old baby',
  },
  {
    title: '16 Month Old Sleep Schedule: How Much Should a 16 Month Old Sleep?',
    href: 'https://rileyapp.com/blog/sleep/16-month-old-sleep-schedule',
    img: '/assets/8fe3a7b3af79c135ea300f1877f1dc795502b3a0-1600x1066.jpeg',
    alt: 'A 16 month old baby sleeping.',
  },
]

const MOBILE_QUERY = '(max-width: 639px)'

function useIsMobile() {
  const [matches, setMatches] = useState(() => typeof window !== 'undefined' && window.matchMedia(MOBILE_QUERY).matches)
  useEffect(() => {
    const mql = window.matchMedia(MOBILE_QUERY)
    const onChange = () => setMatches(mql.matches)
    onChange()
    mql.addEventListener('change', onChange)
    return () => mql.removeEventListener('change', onChange)
  }, [])
  return matches
}

function PostCard({ post }) {
  return (
    <article className="flex w-full max-w-[18rem] flex-col items-center gap-7">
      <a className="group w-full" href={post.href}>
        <div className="relative aspect-[3/4] w-full overflow-hidden rounded-[35px] lg:aspect-auto lg:h-[22rem]">
          <img
            alt={post.alt}
            decoding="async"
            sizes="(max-width: 639px) 45vw, 270px"
            className="absolute inset-0 h-full w-full object-cover transition-[transform,translate,scale,rotate] duration-300 group-hover:[scale:1.05]"
            src={post.img}
          />
        </div>
        <h4 className="text-text-primary mt-4 text-center font-serif text-[0.875rem] leading-[1.1375rem] underline lg:text-[1.25rem] lg:leading-[1.625rem]">
          {post.title}
        </h4>
      </a>
    </article>
  )
}

export default function BlogTeaser() {
  const isMobile = useIsMobile()

  return (
    <section className="mx-auto flex w-full max-w-[90rem] flex-col items-center justify-center gap-8 self-stretch rounded-3xl bg-white px-4 py-8 lg:px-9 lg:py-[100px]">
      <header className="flex w-full flex-col items-center gap-4 self-stretch lg:gap-9">
        <h4 className="lg:desktop-body text-text-primary text-center">Insightful Reads for Modern Parents</h4>
        <h2 className="lg:desktop-h3 mobile-h2 text-text-primary text-center font-serif">Explore the Riley Blog</h2>
      </header>
      <nav aria-label="Blog categories" className="blog-nav w-full overflow-x-auto px-2 py-4 sm:overflow-visible">
        <ul className="mobile-body flex w-max items-center justify-center gap-4 sm:mx-auto sm:w-auto">
          {CATEGORIES.map((c) => (
            <li key={c.slug}>
              <a
                className={`font-sans-bold whitespace-nowrap rounded-[40px] px-4 py-1.5 text-sm font-bold leading-5 text-slate-800 transition-opacity hover:opacity-80 ${c.bg}`}
                href={`https://rileyapp.com/blog/${c.slug}`}
              >
                {c.title}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      {isMobile ? (
        <section className="blog-scroller mt-8 w-full overflow-x-auto">
          <div className="flex snap-x snap-mandatory gap-2 pr-4">
            {POSTS.map((post) => (
              <div key={post.href} className="shrink-0 grow-0 snap-start" style={{ flexBasis: 'calc(50% - 4px)' }}>
                <PostCard post={post} />
              </div>
            ))}
          </div>
        </section>
      ) : (
        <section className="mt-8 flex w-full flex-wrap justify-center gap-6">
          {POSTS.map((post) => (
            <PostCard key={post.href} post={post} />
          ))}
        </section>
      )}
      <div className="mt-8 flex flex-col items-center gap-20">
        <Button href="https://rileyapp.onelink.me/JNxh/nativeappstorebutton" id="blog-explorer-cta">Explore the blog</Button>
      </div>
    </section>
  )
}
