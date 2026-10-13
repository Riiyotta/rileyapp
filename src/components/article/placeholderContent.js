// Placeholder article body (content policy: no copied article text). Block types mirror the Sanity portable-text
// types tallied in Blog spec §3.6 so every renderer is exercised. Spans: string | { text, mark, href, n }.
export const slugify = (s) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')

const PH = 'Placeholder paragraph — the full article is on rileyapp.com.'

export function buildPlaceholderBody(post) {
  const catHref = `https://rileyapp.com/blog/${post.category}`
  const blocks = [
    { type: 'p', spans: [`${PH} This text stands in for the introduction of “${post.title}”.`, { mark: 'cite', n: 1 }] },
    { type: 'promo', text: 'Placeholder promo copy — download Riley now using code RILEYBLOG20 to get 20% off.' },
    { type: 'h2', text: 'Placeholder section one' },
    {
      type: 'p',
      spans: [
        `${PH} It includes `,
        { mark: 'strong', text: 'bold placeholder text' },
        ', ',
        { mark: 'em', text: 'italic placeholder text' },
        ' and an inline link to ',
        { mark: 'link', href: catHref, text: `more ${post.categoryTitle} articles` },
        '.',
      ],
    },
    { type: 'h3', text: 'Placeholder subsection' },
    { type: 'p', spans: [`${PH} A short placeholder lead-in for the list below.`, { mark: 'cite', n: 2 }] },
    {
      type: 'ul',
      items: [
        { spans: [{ mark: 'strong', text: 'Placeholder item:' }, ' first-level bullet text.'] },
        {
          spans: ['Placeholder bullet with nested items.'],
          children: [{ spans: ['Second-level placeholder bullet.'] }, { spans: ['Another second-level placeholder bullet.'] }],
        },
        { spans: ['Final first-level placeholder bullet.'] },
      ],
    },
    { type: 'h2', text: 'Placeholder section two' },
    { type: 'p', spans: [`${PH} Placeholder copy introducing an inline image.`] },
    { type: 'image', src: post.image, alt: post.imageAlt || '' },
    { type: 'editorNote', paragraphs: ['Placeholder editor’s note — the original note, where one exists, is on rileyapp.com.'] },
    { type: 'h2', text: 'Placeholder section three' },
    { type: 'p', spans: [`${PH} Placeholder copy introducing a downloadable image.`, { mark: 'cite', n: 3 }] },
    { type: 'downloadableImage', src: post.image, alt: post.imageAlt || '' },
    { type: 'h2', text: 'Read the original' },
    {
      type: 'p',
      spans: [{ mark: 'link', href: post.url, text: 'Read the full article on rileyapp.com', external: true }, '.'],
    },
  ]
  const headings = blocks.filter((b) => b.type === 'h2').map((b) => ({ text: b.text, id: slugify(b.text) }))
  const sources = [1, 2, 3].map((n) => ({
    n,
    citation: `Placeholder Author (2024). Placeholder source title ${n}. `,
    url: `https://example.com/placeholder-source-${n}`,
  }))
  return { blocks, headings, sources }
}
