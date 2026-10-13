// Renders a local `currentColor` SVG (lucide icons: breadcrumb-chevron, check, download) in a given colour.
// An <img> can't inherit currentColor, so the file is used as a CSS mask over a solid background.
export default function MaskIcon({ src, size, color, className = '', shrink = false }) {
  return (
    <span
      aria-hidden="true"
      className={`inline-block ${shrink ? 'shrink' : 'shrink-0'} ${className}`}
      style={{
        width: size,
        height: size,
        backgroundColor: color,
        WebkitMask: `url("${src}") center / contain no-repeat`,
        mask: `url("${src}") center / contain no-repeat`,
      }}
    />
  )
}
