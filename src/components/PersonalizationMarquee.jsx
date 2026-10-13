import Marquee from './upper/Marquee.jsx'

// §3 PersonalizationMarquee (motion §14 M5: 50s linear infinite reverse, no mask)
const FAMILIES = [
  { src: '/assets/softie-family.svg', alt: 'Softie logo', w: 168, h: 194 },
  { src: '/assets/spark-family.svg', alt: 'Spark logo', w: 168, h: 132 },
  { src: '/assets/uplifter-family.svg', alt: 'Uplifter logo', w: 168, h: 110 },
  { src: '/assets/riley-family.svg', alt: 'Riley logo', w: 168, h: 132 },
  { src: '/assets/worrier-family.svg', alt: 'Worrier logo', w: 168, h: 153 },
  { src: '/assets/guide-family.svg', alt: 'Guide logo', w: 168, h: 123 },
]

export default function PersonalizationMarquee() {
  return (
    <section className="flex flex-col items-center self-stretch pb-12 lg:pb-0">
      <div className="flex w-full flex-col items-center gap-8 overflow-hidden max-md:max-w-full lg:gap-12 lg:py-20">
        {/* Below 992 the desktop-h3 size (40/48) stays but the family is Cadiz; serif applies ≥992 via .desktop-h3 */}
        <h2 className="desktop-h3 text-text-primary self-stretch px-12 text-center text-[40px] leading-[48px] max-md:max-w-full lg:px-0">
          Parenting isn't one-size-fits-all. <br />
          Your support shouldn't be, either.
        </h2>
        <div className="relative flex w-full flex-col items-center justify-center overflow-hidden">
          <div className="w-full">
            <Marquee gapClass="gap-[3rem]" className="[--duration:50s]" rowClassName="[animation-direction:reverse]">
              {FAMILIES.map((f) => (
                <div key={f.alt} className="flex h-[10.5rem] w-auto items-center justify-center">
                  <img alt={f.alt} width={f.w} height={f.h} className="h-[10.25rem] w-full object-contain" src={f.src} />
                </div>
              ))}
            </Marquee>
          </div>
        </div>
        <h4 className="px-12 text-center text-xl leading-8 text-slate-800 max-md:max-w-full lg:w-[458px] lg:px-0">
          Riley learns and remembers what matters: your baby's growth stage, tracking logs, and past wins to give guidance
          that fits your family.
          <br />
          <span className="font-sans-bold mt-8 lg:mt-0">Support that thinks, adapts, and grows with you.</span>
        </h4>
      </div>
    </section>
  )
}
