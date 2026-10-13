// Blog spec §2.6. Plain links to /blog?page=N; disabled ends get href="#" + aria-disabled.
const pill = 'flex items-center gap-2 rounded-[6.25rem] border border-[#e5e5e5] px-4 py-2 text-base leading-6 text-ink'
const off = 'pointer-events-none opacity-50'

export default function BlogPagination({ page = 1, totalPages = 1, basePath = '/blog' }) {
  const hasPrev = page > 1
  const hasNext = page < totalPages
  return (
    <div className="mb-[3rem] flex items-center justify-center gap-4 self-stretch">
      <a
        href={hasPrev ? `${basePath}?page=${page - 1}` : '#'}
        aria-disabled={hasPrev ? undefined : 'true'}
        className={`${pill} ${hasPrev ? '' : off}`}
      >
        <img src="/assets/blog/icons/pagination-prev.svg" alt="" width="8" height="11" />
        <span>Prev</span>
      </a>
      <div className="flex items-center gap-2 text-base leading-6 text-ink">
        <span>Page</span>
        <button type="button" className="border-b border-transparent px-1 transition-colors duration-200">
          {page}
        </button>
        <span>of {totalPages}</span>
      </div>
      <a
        href={hasNext ? `${basePath}?page=${page + 1}` : '#'}
        aria-disabled={hasNext ? undefined : 'true'}
        className={`${pill} ${hasNext ? '' : off}`}
      >
        <span>Next</span>
        <img src="/assets/blog/icons/pagination-next.svg" alt="" width="7" height="11" />
      </a>
    </div>
  )
}
