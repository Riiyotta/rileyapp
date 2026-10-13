import { useEffect, useRef, useState } from 'react'
import MaskIcon from './MaskIcon.jsx'

// Blog spec §3.8. variant: 'top' (header row) | 'toc' (aside / mobile TOC) | 'bottom' (bordered row under sources).
// Social targets on the original are <button>s with unverified click actions; here they are plain share links.
const COPIED_MS = 2000 // original reverts within ≤2.8s (UNVERIFIED); spec says use 2000

function CopyLinkButton({ compact, leading = 'leading-6' }) {
  const [copied, setCopied] = useState(false)
  const timer = useRef(null)
  useEffect(() => () => clearTimeout(timer.current), [])
  const onClick = () => {
    navigator.clipboard?.writeText(window.location.href).catch(() => {})
    setCopied(true)
    clearTimeout(timer.current)
    timer.current = setTimeout(() => setCopied(false), COPIED_MS)
  }
  // original (Tailwind v4) space-x-2 = margin-inline-end on every child but the last; mirrored with mr-2
  const pad = compact ? 'gap-1.5 px-3 py-2' : 'px-4 py-2'
  return (
    <button
      type="button"
      onClick={onClick}
      className={`mr-2 flex items-center rounded-full border border-[#e5e7eb] bg-white font-sans text-base ${leading} text-text-primary hover:bg-gray-300 ${pad}`}
    >
      {copied ? (
        <MaskIcon src="/assets/blog/icons/check.svg" size={16} color="#2e2a42" className={compact ? '' : 'mr-2'} />
      ) : (
        // Behaves like the original inline <svg>: counts its full 21px toward min-content (max-w-none: preflight's
        // img max-width:100% would make it count as 0), yet may flex-shrink (it narrows to 14px in the squeezed
        // bottom row at 390, where the group then holds its 252.4px min-content width).
        <img src="/assets/blog/icons/copy-link.svg" alt="" width="21" height="23" className={`min-w-0 max-w-none ${compact ? '' : 'mr-2'}`} />
      )}
      <span>{copied ? 'Copied!' : 'Copy link'}</span>
    </button>
  )
}

function ButtonGroup({ url, title, compact, leading }) {
  const enc = encodeURIComponent
  const socials = [
    { label: 'Share on Facebook', src: '/assets/blog/icons/share-facebook.svg', w: 34, href: `https://www.facebook.com/sharer/sharer.php?u=${enc(url)}` },
    { label: 'Share on X', src: '/assets/blog/icons/share-x.svg', w: 34, href: `https://twitter.com/intent/tweet?url=${enc(url)}&text=${enc(title)}` },
    { label: 'Share on Instagram', src: '/assets/blog/icons/share-instagram.svg', w: 35, href: 'https://www.instagram.com/' },
  ]
  return (
    <div className="flex items-center gap-2">
      <CopyLinkButton compact={compact} leading={leading} />
      {socials.map((s, i) => (
        <a
          key={s.label}
          href={s.href}
          target="_blank"
          rel="noopener noreferrer"
          aria-label={s.label}
          className={`shrink-0 hover:bg-opacity-80 ${i < socials.length - 1 ? 'mr-2' : ''}`}
        >
          <img src={s.src} alt="" width={s.w} height="34" className="max-w-none" />
        </a>
      ))}
    </div>
  )
}

export default function ShareButtons({ variant = 'top', url, title = '' }) {
  if (variant === 'bottom') {
    return (
      <div className="flex items-center justify-between self-stretch border border-text-primary py-8 sm:max-md:flex-col sm:max-md:gap-8 lg:border-x-0">
        <p className="my-5 text-base leading-7 text-text-primary">Share this article:</p>
        {/* bottom row inherits the prose 28px line-height: copy button 131.5x46 */}
        <ButtonGroup url={url} title={title} leading="leading-7" />
      </div>
    )
  }
  return <ButtonGroup url={url} title={title} compact={variant === 'toc'} />
}
