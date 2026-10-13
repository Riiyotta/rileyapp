import { onHashLinkClick } from './hashLink.js'
import ShareButtons from './ShareButtons.jsx'

// Blog spec §3.5. Desktop: sticky 256px aside (top 80; inner nav sticky top 20). Mobile: bordered inline box.
// The progress fill's bg (`bg-brand-500`) is undefined on live, so it is transparent; its scroll-driven height
// is left at 0 here (motion hand-off).
function TocList({ headings }) {
  return (
    <ul className="flex flex-1 flex-col items-start gap-2">
      {headings.map((h) => (
        <li key={h.id} className="transition-all duration-300">
          <a href={`#${h.id}`} onClick={onHashLinkClick} className="text-base leading-6 text-ink hover:underline">
            {h.text}
          </a>
        </li>
      ))}
    </ul>
  )
}

export function ArticleTocDesktop({ headings, shareUrl, title }) {
  return (
    <div className="sticky top-20 hidden h-screen w-64 flex-shrink-0 overflow-y-auto lg:block">
      <nav className="relative flex w-full flex-col items-center justify-start gap-10 lg:sticky lg:top-5 lg:max-w-[16rem] lg:items-start lg:border-none lg:p-0">
        <div className="flex items-start gap-4 self-stretch lg:gap-5">
          <div className="relative w-1 self-stretch bg-[#D9D9D9]">
            <div className="absolute left-0 top-0 w-full bg-transparent transition-all duration-300" style={{ height: 0 }} data-toc-progress />
          </div>
          <TocList headings={headings} />
        </div>
        <div className="flex w-full items-center gap-2">
          <ShareButtons variant="toc" url={shareUrl} title={title} />
        </div>
      </nav>
    </div>
  )
}

export function ArticleTocMobile({ headings, shareUrl, title }) {
  return (
    <div className="flex flex-col items-center justify-center gap-10 self-stretch py-8 lg:hidden">
      <nav className="relative flex w-full flex-col items-center justify-start gap-10 border border-text-primary py-8">
        <div className="flex flex-col items-start gap-4 self-stretch">
          <span className="text-base leading-6 text-text-primary">In this article:</span>
          <TocList headings={headings} />
        </div>
        <div className="flex w-full items-center gap-2">
          <ShareButtons variant="toc" url={shareUrl} title={title} />
        </div>
      </nav>
    </div>
  )
}

export default function ArticleToc({ variant = 'desktop', ...props }) {
  return variant === 'mobile' ? <ArticleTocMobile {...props} /> : <ArticleTocDesktop {...props} />
}
