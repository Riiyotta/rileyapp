// §13 SiteFooter
const COLS = [
  [
    ['Blog', 'https://rileyapp.com/blog'],
    ['Pricing', 'https://rileyapp.com/pricing'],
    ['Editorial Process', 'https://rileyapp.com/editorial-process'],
  ],
  [
    ['Privacy Policy', 'https://rileyapp.com/privacy'],
    ['Terms of Service', 'https://rileyapp.com/tos'],
    ['Support', 'https://rileyapp.com/support'],
  ],
]

function Divider() {
  return <img src="/assets/icons/footer-divider.svg" alt="" width="1" height="142" className="hidden lg:flex" />
}

export default function SiteFooter() {
  return (
    <footer className="z-30 mx-auto flex w-full max-w-[90rem] flex-col items-center justify-center gap-16 self-stretch overflow-hidden px-8 py-12 lg:gap-12 lg:px-[3.75rem] lg:py-[5.5rem]">
      <div className="flex w-full flex-col items-center justify-between gap-8 self-stretch md:flex-row md:flex-wrap md:justify-between lg:max-w-[1440px] lg:flex-nowrap">
        <div className="w-full lg:w-auto">
          <section className="flex w-full flex-1 flex-col items-center justify-center gap-6 self-stretch lg:flex lg:max-w-[28.75rem] lg:items-end">
            <div className="flex flex-col items-center justify-center gap-4 self-stretch lg:items-end">
              <p className="text-text-primary text-center font-serif text-[1.25rem] leading-[1.625rem] lg:text-left">Stay in the loop with Riley's newsletter.</p>
            </div>
            <form
              className="text-text-primary flex w-full max-w-[28.75rem] items-center justify-between rounded-[2rem] border border-solid border-white bg-white pl-6"
              onSubmit={(e) => e.preventDefault()}
            >
              <input placeholder="Email" className="font-sans text-text-primary flex-grow bg-transparent text-base leading-6 outline-none" aria-label="Enter your email" required type="email" />
              <button type="submit" id="footer-newsletter-submit" className="font-sans-regular desktop-body flex cursor-default items-center justify-center gap-3.5 whitespace-nowrap rounded-[78.641px] bg-purple-100 px-6 py-4 text-white disabled:opacity-60">
                <span>Sign up</span>
              </button>
            </form>
          </section>
        </div>
        <Divider />
        <div className="w-full md:w-[calc(50%-2.75rem)] lg:w-auto">
          <nav className="flex flex-1 items-center justify-start md:justify-end lg:justify-between">
            <div className="flex gap-x-16">
              {COLS.map((col, i) => (
                <div key={i} className="flex flex-col gap-y-6">
                  {col.map(([label, href]) => (
                    <a key={href} className="whitespace-nowrap" href={href}>
                      <span className="font-sans-semibold whitespace-nowrap text-[1rem] text-purple-100">{label}</span>
                    </a>
                  ))}
                </div>
              ))}
            </div>
          </nav>
        </div>
        <Divider />
        <div className="flex w-full md:w-[calc(50%-2.75rem)] lg:w-auto">
          <div className="flex w-full flex-1 items-center justify-center gap-8 self-stretch md:justify-start lg:justify-center lg:gap-6">
            <div className="flex w-full max-w-[16.5rem] flex-1 flex-col items-start justify-center gap-8 self-stretch lg:gap-6">
              <div className="flex flex-col items-center justify-center gap-4 self-stretch lg:items-start">
                <p className="desktop-h4 text-text-primary text-center lg:text-left">Get the App</p>
                <a href="https://rileyapp.onelink.me/JNxh/ln83navr">
                  <img src="/assets/icons/app-store-badge.svg" alt="Download on the App Store" width="153" height="52" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="flex w-full flex-col items-center gap-8">
        <img src="/assets/icons/footer-logo.svg" alt="Riley" width="118" height="76" />
        <p className="text-text-primary font-sans-regular text-[0.875rem] leading-[1.225rem]">© 2025 Riley</p>
      </div>
    </footer>
  )
}
