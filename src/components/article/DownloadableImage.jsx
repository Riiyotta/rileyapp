import MaskIcon from './MaskIcon.jsx'

// Blog spec §3.6 downloadableImage. Button 60x60 (p-4) ≥992 / 44x44 (p-2) below, top/right 8.
// Hover: `hover:bg-brand-400` is a no-op on live while the icon turns white, so the icon disappears on hover.
export default function DownloadableImage({ src, alt = '' }) {
  const filename = src.split('/').pop()
  return (
    <div className="relative mb-4 max-w-full">
      <div className="flex w-full flex-col">
        <img src={src} alt={alt} className="my-8 h-auto w-full" loading="lazy" />
      </div>
      <a
        href={src}
        download={filename}
        aria-label="Download image"
        className="group absolute right-2 top-2 rounded-full bg-white p-2 shadow-md transition-all duration-300 lg:p-4"
      >
        <MaskIcon src="/assets/blog/icons/download.svg" size={28} color="currentColor" className="block text-text-primary group-hover:text-white" />
      </a>
    </div>
  )
}
