import BlogSearch from '../blog/BlogSearch.jsx'

// Blog spec §3.2. ≥992: Back link + 400px search; <992: full-width search only.
export default function ArticleTopBar() {
  return (
    <>
      <div className="hidden items-center justify-between gap-4 self-stretch px-[6.25rem] lg:flex">
        <a href="/blog" className="flex items-center gap-4 self-stretch">
          <img src="/assets/blog/icons/back-arrow.svg" alt="" width="18" height="26" />
          <span className="text-base leading-5 text-text-primary">Back</span>
        </a>
        <div className="w-[400px]">
          <BlogSearch />
        </div>
      </div>
      <div className="w-full items-center px-5 lg:hidden">
        <BlogSearch />
      </div>
    </>
  )
}
