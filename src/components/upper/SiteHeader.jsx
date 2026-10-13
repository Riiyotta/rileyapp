import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import Button from '../shared/Button.jsx'

// §2.2 SiteHeader, §2.3 mobile menu, motion §14 M1/M1b/M2/M11/M14
const ONELINK = 'https://rileyapp.onelink.me/JNxh/nativeappstorebutton'
const BLOG_HREF = 'https://rileyapp.com/blog'

// M1b: delayChildren .1s + staggerChildren .2s
const navDelay = (i) => ({ animationDelay: `${0.1 + i * 0.2}s` })

export default function SiteHeader() {
  const headerRef = useRef(null)
  const [scrolled, setScrolled] = useState(false)
  const [spacerHeight, setSpacerHeight] = useState(0)
  const [menuOpen, setMenuOpen] = useState(false)

  // M2: fixed once window.scrollY > 54
  useEffect(() => {
    const onScroll = () => {
      const next = window.scrollY > 54
      if (next && headerRef.current) setSpacerHeight(headerRef.current.offsetHeight)
      setScrolled(next)
    }
    onScroll()
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // body scroll lock while the menu is open
  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : 'unset'
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [menuOpen])

  const openMenu = () => setMenuOpen(true)
  const closeMenu = () => setMenuOpen(false)
  const toggleMenu = () => (menuOpen ? closeMenu() : openMenu())

  const position = scrolled ? 'fixed top-0 right-0 left-0 translate-y-0 shadow-md' : 'relative'
  const layer = menuOpen
    ? 'z-[1002] backdrop-blur-xl'
    : scrolled
      ? 'z-[100] backdrop-blur-md'
      : 'z-[100] bg-transparent'

  return (
    <>
      {scrolled && <div style={{ height: spacerHeight }} aria-hidden="true" />}
      <header
        ref={headerRef}
        className={`upper-header-in flex w-full items-center px-4 py-3 transition-all duration-300 md:mx-auto md:px-[3.75rem] ${position} ${layer}`}
      >
        <div className="flex w-full items-center justify-between md:mx-auto md:max-w-[90rem]">
          <a className="relative h-[52px] w-[90px] shrink-0" href="https://rileyapp.com/">
            <img alt="Riley logo" width="79" height="52" src="/assets/wordmark.svg" />
          </a>

          <nav className="upper-nav-in hidden flex-1 items-center justify-between lg:flex lg:pl-12">
            <div className="flex flex-1 items-center justify-end gap-12">
              <div className="upper-nav-item" style={navDelay(0)}>
                <a
                  className="font-sans-bold relative flex items-center gap-2 text-lg leading-6 text-purple-100 transition-opacity hover:opacity-80"
                  href={BLOG_HREF}
                >
                  Blog
                </a>
              </div>
              <div className="upper-nav-item" style={navDelay(1)}>
                {/* Opens a changelog modal on the original (out of scope, §16) */}
                <button
                  type="button"
                  className="font-sans-bold cursor-default text-lg leading-6 text-purple-100 transition-opacity hover:opacity-80"
                >
                  What's New?
                </button>
              </div>
            </div>
            <span className="upper-nav-item mx-8 h-6 w-px bg-gray-300" style={navDelay(2)} />
            <div className="upper-nav-item" style={navDelay(3)}>
              <Button href={ONELINK} data-button-id="header-nav-cta" className="header-nav-cta">
                Get Started For Free
              </Button>
            </div>
          </nav>

          <div className="flex gap-5">
            <Button href={ONELINK} className="max-w-[100px] px-3 py-2 lg:hidden">
              Try For $0
            </Button>
            <button
              type="button"
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={menuOpen}
              className="text-text-primary relative z-[1003] cursor-default text-2xl lg:hidden"
              onClick={toggleMenu}
            >
              {menuOpen ? (
                <img src="/assets/icons/menu-close.svg" alt="" width="23" height="24" />
              ) : (
                <img src="/assets/icons/menu-hamburger.svg" alt="" width="28" height="23" />
              )}
            </button>
          </div>
        </div>
      </header>

      {menuOpen &&
        createPortal(
          <>
            <div className="fixed inset-0 backdrop-blur-[8px]" style={{ zIndex: 1000 }} onClick={closeMenu} />
            <div
              className="upper-menu-enter fixed inset-0 backdrop-blur-xl"
              style={{ zIndex: 1001 }}
            >
              <div className="text-text-primary flex h-full flex-col px-5 pt-24 pb-[3.75rem]">
                <div className="flex w-full flex-col items-center gap-8">
                  <div className="font-sans-semibold w-full text-center text-xl">
                    {/* Blog sub-categories come from /api/get-blog-categories at runtime (UNVERIFIED, §16);
                        with no categories the original renders a plain link. */}
                    <a
                      href={BLOG_HREF}
                      className="flex items-center justify-center gap-2 transition-opacity hover:opacity-80"
                      onClick={closeMenu}
                    >
                      Blog
                    </a>
                  </div>
                  <div className="font-sans-semibold w-full text-center text-xl">
                    <button type="button" className="transition-opacity hover:opacity-80" onClick={closeMenu}>
                      What's New?
                    </button>
                  </div>
                </div>
                <div className="mt-auto w-full p-4 text-center">
                  <Button href={ONELINK} className="w-full max-w-xs">
                    Get Started For Free
                  </Button>
                </div>
              </div>
            </div>
          </>,
          document.body,
        )}
    </>
  )
}
