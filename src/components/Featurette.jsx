import Button from './shared/Button.jsx'
import RiveChat from './upper/RiveChat.jsx'
import useEmblaLoop from './shared/useEmblaLoop.js'

// §5 Featurette. Carousel = §14 M6 (embla {loop:true}, no autoplay, prev/next + drag).
const SLIDES = [
  {
    src: '/assets/animations/chat_module_meg.riv',
    artboard: 'chat_module_meg',
    stateMachine: 'meg_chat_SM',
    image: '/assets/meg.png',
    alt: 'Feeding help',
  },
  {
    src: '/assets/animations/chat_module_seb.riv',
    artboard: 'chat_module_seb',
    stateMachine: 'seb_chat_SM',
    image: '/assets/seb-and-daughter.png',
    alt: 'Seb & daughter testimonial',
  },
  {
    src: '/assets/animations/chat_module_naina.riv',
    artboard: 'chat_module_naina',
    stateMachine: 'naina_chat_SM',
    image: '/assets/naina.png',
    alt: 'Milestone celebration',
  },
]
// M6: embla {loop:true} motion model ported in useEmblaLoop (duration 25, friction .68, 60Hz integrator).
// The original's embla (watchDrag: true) ignores data-embla-skip-drag, so drags start anywhere incl. the Rive canvas.

export default function Featurette() {
  const { containerRef, slideRef, next, prev, viewportProps } = useEmblaLoop(SLIDES.length)

  return (
    <section className="px-11 py-20 max-md:px-5">
      <section className="relative mx-auto flex w-full max-w-[90rem] flex-col items-center gap-8 overflow-hidden pt-8 lg:px-20 lg:py-10 2xl:px-4">
        <h2 className="lg:desktop-h3 mobile-h2 text-text-primary text-center font-serif">
          Here's How <i>Real</i> Users
          <br />
          Talk to Riley:
        </h2>
        <div className="relative flex flex-col items-center overflow-hidden rounded-[30px] bg-tangerine pt-8">
          <img
            alt="Decorative clouds"
            width="1440"
            height="740"
            className="absolute left-0 top-0 h-full w-full scale-125"
            src="/assets/background-clouds.svg"
          />
          <div {...viewportProps} className="w-full flex-1 touch-pan-y select-none">
            <div ref={containerRef} className="flex h-full" style={{ transform: 'translate3d(0px, 0px, 0px)' }}>
              {SLIDES.map((s, i) => (
                <div
                  key={s.alt}
                  className="flex w-full flex-none flex-col items-center justify-center gap-6 px-4 lg:flex-row lg:gap-10"
                  ref={slideRef(i)}
                >
                  <div className="relative order-2 mx-auto aspect-[0.85] w-full max-w-[511px] lg:order-1 lg:mx-0">
                    <img
                      alt="Phone shell"
                      draggable="false"
                      className="pointer-events-none select-none object-contain"
                      src="/assets/phonebg.svg"
                      style={{ position: 'absolute', height: '100%', width: '100%', inset: '8px 0px 0px' }}
                    />
                    <div
                      className="absolute -left-7 -top-0 flex h-full w-full items-end justify-center lg:-left-11"
                      data-embla-skip-drag="true"
                    >
                      <RiveChat src={s.src} artboard={s.artboard} stateMachine={s.stateMachine} />
                    </div>
                  </div>
                  <div className="order-1 lg:order-2">
                    <img
                      alt={s.alt}
                      width="490"
                      height="551"
                      draggable="false"
                      className="my-auto aspect-[0.89] w-[491px] object-contain max-md:max-w-full"
                      src={s.image}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="mx-auto flex w-full items-center justify-center gap-8">
          <button type="button" aria-label="Previous slide" onClick={prev} className="cursor-default rounded-full bg-white/30 p-2 backdrop-blur">
            <img src="/assets/icons/featurette-prev.svg" alt="" width="13" height="13" />
          </button>
          <button type="button" aria-label="Next slide" onClick={next} className="cursor-default rounded-full bg-white/30 p-2 backdrop-blur">
            <img src="/assets/icons/featurette-next.svg" alt="" width="13" height="13" className="rotate-180" />
          </button>
        </div>
      </section>
      <div className="mx-auto mt-8 flex w-full max-w-[14rem] flex-col items-center">
        {/* Destination UNVERIFIED (§0.6) */}
        <Button data-button-id="home-product-feature-cta">Talk to Riley</Button>
      </div>
    </section>
  )
}
