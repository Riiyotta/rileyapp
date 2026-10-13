import { useEffect } from 'react'
import AnnouncementBar from '../components/AnnouncementBar.jsx'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import SiteFooter from '../components/SiteFooter.jsx'

// Marketing spec §2 "peekaboo" 404 template (all 8 dead landing slugs + any unknown path).
// Original link classes `ext-white text-brand-500 hover:text-brand-600` are undefined there, so the link
// inherits #0a0a0a with no hover change. The img's `scale-105` is the v4 `scale` property (not transform).
export default function NotFound() {
  // §2.6: 404 routes carry <meta name="robots" content="noindex">
  useEffect(() => {
    const meta = document.createElement('meta')
    meta.name = 'robots'
    meta.content = 'noindex'
    document.head.appendChild(meta)
    return () => meta.remove()
  }, [])

  return (
    <>
      <AnnouncementBar />
      <SiteHeader />
      <div className="mx-auto flex min-h-[500px] w-full flex-col items-center gap-6 px-6 pt-12 text-center xl:min-h-[850px]">
        <h3 className="font-serif text-4xl font-medium text-text-primary xl:text-6xl">
          Oops! This page is playing peekaboo... and it's REALLY good at it.
        </h3>
        <p className="max-w-[700px] font-serif text-base text-text-primary xl:text-xl">
          Looks like this link went on a nap and forgot to wake up.
        </p>
        <a href="/" className="flex flex-row items-center gap-3">
          Go back <span className="text-lg">›</span>
        </a>
        <img
          src="/assets/shared/background.bc1c0c29.svg"
          alt=""
          width="1440"
          height="561"
          loading="lazy"
          className="-z-[100] w-full"
          style={{ scale: '1.05', color: 'transparent' }}
        />
      </div>
      <SiteFooter />
    </>
  )
}
