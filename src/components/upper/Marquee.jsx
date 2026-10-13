// Shared marquee (§2.5 / §3, motion §14 M4/M5): container holds 4 identical rows
// that each translate by -(100% + --gap) over --duration, linear, infinite.
// `gapClass` lets a caller override the container gap (§3 computes 48px while rows keep var(--gap)).
export default function Marquee({ className = '', rowClassName = '', gapClass = '[gap:var(--gap)]', repeat = 4, children }) {
  return (
    <div className={`group flex overflow-hidden p-2 [--gap:1rem] ${gapClass} flex-row ${className}`}>
      {Array.from({ length: repeat }, (_, i) => (
        <div
          key={i}
          aria-hidden={i > 0 ? 'true' : undefined}
          className={`flex shrink-0 justify-around [gap:var(--gap)] upper-animate-marquee flex-row ${rowClassName}`}
        >
          {children}
        </div>
      ))}
    </div>
  )
}
