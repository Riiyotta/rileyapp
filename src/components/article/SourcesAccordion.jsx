import { useState } from 'react'

// Blog spec §3.9. Collapsed: sources kept in an sr-only div (for #source-N anchors). Toggle is instant.
function SourceList({ sources }) {
  return sources.map((s) => (
    <div key={s.n} id={`source-${s.n}`} className="flex w-full flex-col">
      <p className="text-large my-0 text-base leading-7 text-text-primary">
        <span className="mr-2 font-sans-bold">{s.n}.</span>
        {s.citation}
        <a href={s.url} target="_blank" rel="noopener noreferrer" className="text-gray-900 underline hover:underline">
          {s.url}
        </a>
      </p>
    </div>
  ))
}

export default function SourcesAccordion({ sources = [] }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mb-10 flex w-full flex-col items-center justify-center">
      <div className="flex w-full flex-col items-start justify-center gap-2 self-stretch rounded-2xl bg-white px-6 py-10">
        <div className="flex w-full cursor-pointer items-center justify-between gap-5" onClick={() => setOpen((o) => !o)}>
          <h5 className="px-1 text-base leading-7 text-text-primary">{`${sources.length}  sources cited`}</h5>
          <div className="flex h-6 w-6 shrink-0 items-center justify-center">
            {open ? (
              <img src="/assets/blog/icons/sources-minus.svg" alt="" width="18" height="3" />
            ) : (
              <img src="/assets/blog/icons/sources-plus.svg" alt="" width="24" height="25" />
            )}
          </div>
        </div>
        {open ? (
          <div className="mt-6 flex w-full flex-col gap-8">
            <SourceList sources={sources} />
          </div>
        ) : (
          <div className="sr-only">
            <SourceList sources={sources} />
          </div>
        )}
      </div>
    </div>
  )
}
