import Button from './shared/Button.jsx'

// §12 FinalCta
export default function FinalCta() {
  return (
    <section className="relative flex w-full flex-col items-center self-stretch overflow-hidden px-8 py-20 pb-40 lg:px-[20rem] lg:py-[14rem]">
      <img alt="Background decoration" loading="lazy" width="1774" height="826" decoding="async" className="absolute top-0 -z-10" src="/assets/background-clouds(1).svg" />
      <div className="flex w-full flex-col items-center justify-center gap-12 overflow-hidden max-md:max-w-full">
        <h2 className="lg:desktop-h2 mobile-h1 text-text-primary text-center font-serif max-md:max-w-full">
          We are raising a generation <br />of confident parents.
        </h2>
        <div className="flex max-w-[20rem]">
          <Button href="https://rileyapp.onelink.me/JNxh/nativeappstorebutton">Get support that gets you</Button>
        </div>
      </div>
      <div className="absolute bottom-[-72px] left-1/2 z-0 flex h-[12rem] min-h-24 w-[42.5rem] max-w-full -translate-x-2/4 rounded-none lg:bottom-[-56px]">
        <img alt="Mascots" loading="lazy" width="778" height="97" decoding="async" src="/assets/mascots.svg" />
      </div>
    </section>
  )
}
