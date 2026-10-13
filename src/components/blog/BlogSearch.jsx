import { useMemo, useState } from 'react'
import posts from '../../data/blogPosts.json'
import { postHref } from './categories.js'

// Blog spec §2.3. Live type-ahead; the original queries /api/search-articles, the clone
// filters blogPosts.json by title/excerpt locally. Snippet context width is a clone choice.
const CONTEXT = 60

function snippet(post, q) {
  const lq = q.toLowerCase()
  const src = post.excerpt && post.excerpt.toLowerCase().includes(lq) ? post.excerpt : post.title
  const i = src.toLowerCase().indexOf(lq)
  const start = Math.max(0, i - CONTEXT)
  const end = Math.min(src.length, i + q.length + CONTEXT)
  return (
    <>
      {'... '}
      {src.slice(start, i)}
      <mark>{src.slice(i, i + q.length)}</mark>
      {src.slice(i + q.length, end)}
      {' ...'}
    </>
  )
}

export default function BlogSearch({ className = '', widthClass = 'lg:max-w-md' }) {
  const [query, setQuery] = useState('')
  const q = query.trim()
  const results = useMemo(() => {
    if (!q) return []
    const lq = q.toLowerCase()
    return posts.filter((p) => p.title.toLowerCase().includes(lq) || (p.excerpt || '').toLowerCase().includes(lq))
  }, [q])

  return (
    <div className={`relative w-full ${className}`}>
      <div className={`shadow-2xs relative mx-auto w-full rounded-[5rem] ${widthClass}`}>
        <div className="pointer-events-none absolute inset-y-0 start-0 flex items-center ps-5">
          <img src="/assets/blog/icons/search.svg" alt="" width="16" height="16" className="h-4 w-4" />
        </div>
        <input
          type="search"
          required
          placeholder="Search blog article..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="block w-full rounded-[5rem] border border-gray-300 bg-white p-4 ps-12 font-sans-regular text-sm leading-5 text-gray-900 focus:border-purple-100"
        />
        {q && (
          <div className="blog-search-fade absolute z-20 mt-1 flex max-h-[320px] w-full flex-col overflow-y-scroll rounded-2xl bg-white shadow-[0_20px_25px_-5px_#0000001a,0_8px_10px_-6px_#0000001a]">
            {results.length === 0 ? (
              <div className="flex flex-col items-center justify-center px-4 py-3">No results found</div>
            ) : (
              results.map((p) => (
                <a key={p.slug} href={postHref(p)} className="block border-b border-[#e5e5e5] px-4 py-3">
                  <div className="flex flex-row gap-1">
                    <div className="rounded px-1 text-sm leading-5">{p.categoryTitle}</div>
                    <div className="truncate">{p.title}</div>
                  </div>
                  <div className="text-sm leading-5 text-[#6a7282]">{snippet(p, q)}</div>
                </a>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}
