import { BLOG_TABS } from './categories.js'

// Blog spec §2.4. active: 'all' or a category slug. The active underline is bg-brand-500,
// which is undefined (transparent) on the live site, so it renders as a transparent 2px bar.
export default function BlogCategoryTabs({ active = 'all' }) {
  return (
    <div className="mb-8 flex justify-center">
      <nav className="w-full">
        <ul className="flex items-center gap-4 overflow-x-auto whitespace-nowrap border-b border-[#e5e7eb] md:justify-center">
          {BLOG_TABS.map((t) => {
            const isActive = t.key === active
            return (
              <li key={t.key} className="relative flex flex-shrink-0 items-center justify-center py-2">
                <a
                  href={t.href}
                  className={`px-4 py-2 text-lg leading-7 transition-all duration-300 ${
                    isActive ? 'font-sans-bold text-text-primary' : 'font-sans-regular text-[#6a7282]'
                  }`}
                >
                  {t.label}
                </a>
                {isActive && <div className="absolute bottom-0 left-0 h-0.5 w-full bg-transparent" />}
              </li>
            )
          })}
        </ul>
      </nav>
    </div>
  )
}
