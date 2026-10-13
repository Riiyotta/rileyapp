// Blog spec §2.2. h1 size (64/72 >=992, 40/48 <992) and Recoleta come from the global unlayered h1 rules.
export default function BlogIndexHero() {
  return (
    <div className="flex items-center justify-between self-stretch">
      <img src="/assets/blog/icons/blogmascot.svg" alt="Riley Mascot" width="138" height="136" className="hidden md:flex" />
      <div className="flex max-w-[36rem] flex-1 flex-col items-center justify-center gap-10">
        <div className="flex flex-col items-start gap-4 self-stretch">
          <h1 className="self-stretch text-center text-text-primary">Riley Articles</h1>
          <h3 className="self-stretch text-center font-sans-regular text-[20px] leading-[28px] text-text-primary">
            Helpful articles with all the information you need to raise happy, healthy children!
          </h3>
        </div>
      </div>
      <img src="/assets/blog/icons/books.svg" alt="Book icon" width="114" height="136" className="hidden md:flex" />
    </div>
  )
}
