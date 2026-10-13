import { useEffect, useMemo } from 'react'
import posts from '../data/blogPosts.json'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import FinalCta from '../components/FinalCta.jsx'
import SiteFooter from '../components/SiteFooter.jsx'
import NotFound from './NotFound.jsx'
import ArticleTopBar from '../components/article/ArticleTopBar.jsx'
import ArticleHeader from '../components/article/ArticleHeader.jsx'
import { ArticleTocDesktop, ArticleTocMobile } from '../components/article/ArticleToc.jsx'
import ArticleBody from '../components/article/ArticleBody.jsx'
import SourcesAccordion from '../components/article/SourcesAccordion.jsx'
import ShareButtons from '../components/article/ShareButtons.jsx'
import RelatedPosts from '../components/article/RelatedPosts.jsx'
import { buildPlaceholderBody } from '../components/article/placeholderContent.js'

// Blog spec §3: /blog/<category>/<slug>. No AnnouncementBar (§0.3). Body is placeholder content (content policy).
// Layout note: the original has separate `hidden lg:flex` / `lg:hidden` trees for the body; here the body row
// and its inner row are `display:contents` below 992 so a single body (unique heading ids) serves both layouts.

function useArticleMeta(post) {
  useEffect(() => {
    if (!post) return
    const prevTitle = document.title
    document.title = post.seoTitle || `${post.title} | Riley`
    let meta = document.querySelector('meta[name="description"]')
    const created = !meta
    if (created) {
      meta = document.createElement('meta')
      meta.name = 'description'
      document.head.appendChild(meta)
    }
    const prevDesc = meta.content
    meta.content = post.excerpt || ''
    return () => {
      document.title = prevTitle
      if (created) meta.remove()
      else meta.content = prevDesc
    }
  }, [post])
}

export default function BlogArticlePage({ params = [] }) {
  const [category, slug] = params
  const post = posts.find((p) => p.category === category && p.slug === slug)
  const content = useMemo(() => (post ? buildPlaceholderBody(post) : null), [post])
  useArticleMeta(post)

  if (!post) return <NotFound />

  const shareUrl = `https://www.rileyapp.com/blog/${post.category}/${post.slug}`
  const tocProps = { headings: content.headings, shareUrl, title: post.title }

  return (
    <>
      <SiteHeader />
      <article className="my-4 flex w-full justify-center lg:my-16">
        <div className="flex w-full max-w-[90rem] flex-col items-center gap-[7.5rem]">
          <div className="flex flex-col items-center gap-8 self-stretch lg:gap-20">
            <ArticleTopBar />
            <div className="flex flex-col items-center justify-center gap-[2.75rem] self-stretch px-5 lg:gap-[5.5rem] lg:px-0">
              <ArticleHeader post={post} shareUrl={shareUrl} />
              <div className="contents lg:flex lg:items-center lg:justify-center lg:self-stretch lg:max-xl:px-[2.75rem] xl:px-[5.5rem]">
                {/* <992: TOC box + prose stack with no gap (original lg:hidden tree); ≥992: TOC aside | prose row, gap 88 */}
                <div className="flex flex-col items-start self-stretch lg:flex-1 lg:flex-row lg:gap-[5.5rem] lg:self-auto">
                  <ArticleTocDesktop {...tocProps} />
                  <ArticleTocMobile {...tocProps} />
                  <div className="flex w-full max-w-[991px] flex-col items-start justify-center gap-10 self-stretch lg:max-w-[1280px] lg:flex-1 lg:gap-0 lg:self-auto">
                    <ArticleBody blocks={content.blocks} />
                    <SourcesAccordion sources={content.sources} />
                    <ShareButtons variant="bottom" url={shareUrl} title={post.title} />
                  </div>
                </div>
              </div>
              <RelatedPosts />
            </div>
            <FinalCta />
            {/* On the original the footer sits inside the article's gap-80 column (80 below FinalCta, article mb 64 after it). */}
            <SiteFooter />
          </div>
        </div>
      </article>
    </>
  )
}
