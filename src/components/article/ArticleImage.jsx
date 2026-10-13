// Blog spec §3.6 image: wrapper my-8 (first: 0 0 32), img 800 wide at natural ratio, radius 10, left-aligned.
export default function ArticleImage({ src, alt = '' }) {
  return (
    <div className="my-8 first:mt-0">
      <img src={src} alt={alt} width="800" className="ab-img w-[800px]" loading="lazy" />
    </div>
  )
}
