import { useState } from 'react'

// Blog spec §0.6: react-cookie-consent markup/inline styles as rendered on the original.
// Fixed at left 60% / width 40% at every viewport (at 390 the 300px-basis text overflows; kept as-is).
const COOKIE = 'CookieConsent'
const hasCookie = () => document.cookie.split('; ').some((c) => c.startsWith(`${COOKIE}=`))

export default function CookieConsent() {
  const [visible, setVisible] = useState(() => !hasCookie())
  if (!visible) return null
  const accept = () => {
    document.cookie = `${COOKIE}=true; max-age=${365 * 24 * 60 * 60}; path=/`
    setVisible(false)
  }
  return (
    <div
      className="CookieConsent"
      style={{
        position: 'fixed',
        left: '60%',
        bottom: 0,
        width: '40%',
        zIndex: 9999,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '1rem',
        background: 'rgba(255,255,255,.9)',
        backdropFilter: 'blur(6px)',
        WebkitBackdropFilter: 'blur(6px)',
        color: '#2e2a42',
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        padding: '.75rem 1rem',
        fontSize: '.875rem',
        lineHeight: 1.5,
        boxShadow: '0 4px 16px rgba(0,0,0,.06)',
      }}
    >
      <div style={{ flex: '1 0 300px', margin: 0 }}>
        By using this site, you accept cookies for analytics.&nbsp;
        <a className="underline" href="/privacy">
          Learn more
        </a>
      </div>
      <div>
        <button
          id="rcc-confirm-button"
          aria-label="Accept cookies"
          onClick={accept}
          style={{
            background: '#5934c5',
            color: '#fff',
            border: 0,
            borderRadius: 24,
            padding: '.5rem 2rem',
            margin: 15,
            fontWeight: 600,
            fontSize: 14,
            whiteSpace: 'nowrap',
            cursor: 'pointer',
            flex: '0 0 auto',
          }}
        >
          OK
        </button>
      </div>
    </div>
  )
}
