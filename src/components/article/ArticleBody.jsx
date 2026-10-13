import { slugify } from './placeholderContent.js'
import { onHashLinkClick } from './hashLink.js'
import PromoUnit from './PromoUnit.jsx'
import EditorNote from './EditorNote.jsx'
import ArticleImage from './ArticleImage.jsx'
import DownloadableImage from './DownloadableImage.jsx'

// Blog spec §3.6 block renderers. Typography/spacing lives in src/styles/article.css (`ab-*`).
// <992 the original's blocks are direct children of the gap-40 prose column (no mb-8 wrapper), hence gap-10 here.

export function CitationSup({ n }) {
  return (
    <sup className="ab-sup">
      <a href={`#source-${n}`} onClick={onHashLinkClick} className="hover:underline">
        [ {n} ]
      </a>
    </sup>
  )
}

export function InlineLink({ href, external, children }) {
  return (
    <a href={href} className="ab-link hover:underline" {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})}>
      {children}
    </a>
  )
}

function Spans({ spans = [] }) {
  return spans.map((s, i) => {
    if (typeof s === 'string') return s
    switch (s.mark) {
      case 'strong':
        return <strong key={i} className="ab-strong">{s.text}</strong>
      case 'em':
        return <em key={i} className="ab-em">{s.text}</em>
      case 'link':
        return <InlineLink key={i} href={s.href} external={s.external}>{s.text}</InlineLink>
      case 'cite':
        return <CitationSup key={i} n={s.n} />
      default:
        return s.text
    }
  })
}

export function Paragraph({ spans }) {
  return <p className="ab-p"><Spans spans={spans} /></p>
}

export function H2({ text }) {
  return <h2 id={slugify(text)} className="ab-h2">{text}</h2>
}

export function H3({ text }) {
  return <h3 className="ab-h3">{text}</h3>
}

export function BulletList({ items }) {
  return (
    <ul className="ab-ul">
      {items.map((item, i) => (
        <li key={i} className="ab-li">
          <Spans spans={item.spans} />
          {item.children && <BulletList items={item.children} />}
        </li>
      ))}
    </ul>
  )
}

function Block({ block }) {
  switch (block.type) {
    case 'p':
      return <Paragraph spans={block.spans} />
    case 'h2':
      return <H2 text={block.text} />
    case 'h3':
      return <H3 text={block.text} />
    case 'ul':
      return <BulletList items={block.items} />
    case 'promo':
      return <PromoUnit text={block.text} />
    case 'editorNote':
      return <EditorNote paragraphs={block.paragraphs} />
    case 'image':
      return <ArticleImage src={block.src} alt={block.alt} />
    case 'downloadableImage':
      return <DownloadableImage src={block.src} alt={block.alt} />
    default:
      return null
  }
}

export default function ArticleBody({ blocks = [] }) {
  return (
    <div className="ab-body flex flex-col gap-10 lg:mb-8 lg:gap-0">
      {blocks.map((b, i) => (
        <Block key={i} block={b} />
      ))}
    </div>
  )
}
