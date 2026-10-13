import Button from './shared/Button.jsx'
import SiteHeader from './upper/SiteHeader.jsx'
import HeroParallaxClouds from './upper/HeroParallaxClouds.jsx'
import Marquee from './upper/Marquee.jsx'

// §2 Hero: SiteHeader, HeroParallaxClouds, HeroContent, PressMarquee
const PRESS = [
  { src: '/assets/nbc.png', alt: 'NBC logo' },
  { src: '/assets/axios.png', alt: 'Axios logo' },
  { src: '/assets/bump-logo.png', alt: 'Bump logo' },
  { src: '/assets/finsmes.png', alt: 'Finsmes logo' },
  { src: '/assets/tc.png', alt: 'TC logo' },
  { src: '/assets/glamour.png', alt: 'Glamour logo' },
]

function HeroContent() {
  return (
    <div className="relative z-50 mx-auto flex w-full max-w-[80rem] flex-col items-center px-8 py-8 pb-[10rem] max-md:gap-12 lg:flex-row lg:py-[5rem]">
      <div className="flex flex-1 flex-col items-center gap-10 max-md:gap-6 max-md:px-4 lg:order-1 lg:items-start xl:min-w-[45rem]">
        <div className="relative flex flex-col items-center gap-6 max-md:gap-4 lg:min-w-[33.5rem] lg:items-start">
          <div className="relative mx-0 flex flex-col items-center justify-center gap-6 lg:inline-flex lg:items-start lg:gap-0">
            <img alt="Riley Mascot" width="77" height="84" className="flex w-[5.8rem] lg:hidden" src="/assets/HeroRiley.svg" />
            {/* font-size/line-height come from the unlayered h1 rule in index.css (64/72 ≥992, 40/48 below) */}
            <h1 className="text-text-primary text-center font-serif lg:text-left">
              <span className="block">
                Panic Scrolling Stops Here. Meet
                <span className="inline-flex items-baseline gap-3">
                  <img
                    alt=""
                    aria-hidden="true"
                    width="320"
                    height="320"
                    className="ml-3 hidden w-[4.5rem] translate-y-[0.25em] lg:inline-block"
                    src="/assets/HeroRiley.svg"
                  />
                  <span>Riley.</span>
                </span>
              </span>
            </h1>
          </div>
          <p className="text-text-primary mobile-body lg:desktop-body max-w-[31.25rem] text-center font-sans lg:text-left">
            Get instant, pediatrician-backed parenting support the moment you need it. Riley has{' '}
            <span className="font-sans-bold">award-winning, 24/7 advice tailored to your family</span> with smart
            tracking and guidance. Parent confidently, with{' '}
            <span className="font-sans-bold">the only parenting app you'll ever need.</span>
          </p>
        </div>
        <div className="mx-0 mb-28 flex w-full flex-col items-center justify-center gap-4 self-stretch lg:mb-0 lg:items-start">
          {/* Destination UNVERIFIED (§0.6) */}
          <Button data-button-id="hero-cta" className="max-w-[14rem] lg:mb-0">
            Get Started For Free
          </Button>
          <div className="flex items-center justify-center gap-2.5">
            <p className="text-text-primary text-[1rem] leading-6">Available on:</p>
            <img src="/assets/icons/apple-logo.svg" alt="" aria-hidden="true" width="14" height="16" />
          </div>
        </div>
      </div>
      <div className="relative -z-[15] -mt-12 flex justify-center overflow-visible md:-mt-8 lg:order-2">
        <img
          alt=""
          width="1000"
          height="1000"
          className="mx-0 max-w-[25rem] [scale:2.5] self-center md:max-w-[40rem] lg:[translate:-4rem] lg:[scale:2]"
          src="/assets/HeroIllo.84fc0736.svg"
        />
      </div>
    </div>
  )
}

function PressMarquee() {
  return (
    <div className="flex w-full pb-16">
      <div className="relative flex w-full flex-col items-center justify-center overflow-hidden bg-violet-100">
        <div className="upper-press-mask w-full">
          <Marquee className="[--duration:20s]">
            {PRESS.map((item) => (
              <div key={item.alt} className="mx-8 flex h-16 w-32 items-center justify-center">
                <img alt={item.alt} width="128" height="24" className="h-auto max-h-6 w-full object-contain" src={item.src} />
              </div>
            ))}
          </Marquee>
        </div>
      </div>
    </div>
  )
}

export default function Hero() {
  return (
    <div className="relative w-full overflow-hidden">
      <HeroParallaxClouds />
      <header className="relative mx-auto w-full">
        <SiteHeader />
        <HeroContent />
        <PressMarquee />
      </header>
    </div>
  )
}
