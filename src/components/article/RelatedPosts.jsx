// Blog spec §3.9 RelatedPosts. The carousel renders EMPTY (0px) on the live site at every width, and a second,
// identical wrapper (author's other posts) is also empty (0 tall). Replicated as rendered: both wrappers are direct
// children of the article content column, so its 88px (44 <992) gap also applies before the empty second one.
// "See All >" has no href/action on the original.
export default function RelatedPosts() {
  return (
    <>
      <div className="w-full items-center justify-center lg:max-2xl:px-12 2xl:px-[6.25rem]">
        <div className="flex flex-col items-center justify-center gap-10 self-stretch sm:px-5">
          <div className="flex flex-col items-start gap-[3.75rem] self-stretch">
            <div className="flex w-full flex-col items-center justify-center gap-6 lg:flex-row">
              <img src="/assets/blog/icons/3dglasses.svg" alt="" width="112" height="63.1" className="h-[63.1px] w-[112px]" />
              <div className="flex flex-1 flex-col items-start gap-3">
                <h3 className="h3-small font-sans-bold text-base leading-6 text-text-primary">You'll also love these posts:</h3>
                <p className="text-base leading-6" />
              </div>
            </div>
            <div className="w-full overflow-hidden">
              <div className="flex gap-8 overflow-x-auto scroll-smooth" />
            </div>
            <div className="flex w-full items-center justify-center gap-6">
              <button type="button" className="ml-2 rounded-full border border-[#e5e5e5] px-4 py-2 font-sans-bold text-base leading-6 text-ink">
                See All &gt;
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="w-full items-center justify-center lg:max-2xl:px-12 2xl:px-[6.25rem]" />
    </>
  )
}
