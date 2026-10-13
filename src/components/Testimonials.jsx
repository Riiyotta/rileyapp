import { forwardRef } from 'react'
import Button from './shared/Button.jsx'
import useEmblaLoop from './shared/useEmblaLoop.js'

// §8 Testimonials — looping carousel (M7). Embla {loop:true} motion ported in useEmblaLoop.
const SLIDES = [
  {
    quote: '“10 days into having our newborn, we’ve already developed the habit of saying “Hm, not sure. Ask Riley” multiple times a day. Not sure what we’d do without having Riley to back our instincts.”',
    avatar: '/assets/purple1.svg',
    name: 'Max L., Dad of Baby R (1 mo)',
  },
  {
    quote: '“Riley offers calm and reassurance while Google makes me spiral. With my second, it feels like we’re starting over and have forgotten everything about the newborn phase but Riley’s here for all my questions”',
    avatar: '/assets/purple2.svg',
    name: 'Meg F., Mom of Baby A (5 mos) and Baby H (2 yrs)',
  },
  {
    quote: '“Compared to every other app, especially chat tools, Riley asks better questions and more relevant follow-ups based on my child’s age and the nuance of the moment - the end result is always more helpful.”',
    avatar: '/assets/purple3.svg',
    name: 'Rebeckah R., Mom of Baby N. (7mo)',
  },
  {
    quote: '“Riley’s tracking and recommendations are smart and proactive.  I love that it’s personalized and remembers details about my family without me having to myself.”',
    avatar: '/assets/purple4.svg',
    name: 'App Store Review',
  },
  {
    quote: '“I was traveling this week and *terrifyingly* my pump broke and I was panicking. Riley pulled through. Having a resource to text with at 1 am? 11/10.”',
    avatar: '/assets/purple5.svg',
    name: 'R, Mom of Baby K. (5mo)',
  },
]

const Slide = forwardRef(function Slide({ slide }, ref) {
  return (
    <figure
      ref={ref}
      className="flex shrink-0 basis-full flex-col items-center gap-8 text-center"
      style={{ flex: '0 0 100%', minWidth: '100%' }}
    >
      <img src="/assets/icons/stars-5.svg" alt="" width="198" height="38" draggable="false" />
      <blockquote className="desktop-h4 text-text-primary mx-auto max-w-3xl max-lg:text-[24px] max-lg:leading-[33.8px]">
        {slide.quote}
      </blockquote>
      <figcaption className="mt-10 flex flex-col items-center gap-4">
        <img alt="" loading="lazy" width="64" height="64" decoding="async" draggable="false" className="h-16 w-16 rounded-full object-cover" src={slide.avatar} />
        <span className="font-sans-semibold text-text-primary text-base">{slide.name}</span>
      </figcaption>
    </figure>
  )
})

export default function Testimonials() {
  const { containerRef, slideRef, next, prev, viewportProps } = useEmblaLoop(SLIDES.length)

  return (
    <section className="w-full bg-latte-150" aria-labelledby="testimonials-title">
      <div className="text-text-primary mx-auto flex w-full max-w-[90rem] flex-col items-center gap-8 self-stretch py-8 max-md:px-5 lg:gap-11 lg:px-[280px] lg:py-20">
        <header className="flex w-full flex-col items-center gap-3 self-stretch text-center lg:gap-8">
          <p className="lg:desktop-body">Real Reviews, Real Families</p>
          <h2 id="testimonials-title" className="mobile-h2 lg:desktop-h3 font-serif">Why Parents Love Riley</h2>
        </header>
        <div className="relative flex flex-col items-center gap-8 self-stretch overflow-hidden rounded-3xl bg-violet-100 px-14 py-9 lg:px-40 lg:py-[60px]">
          <div {...viewportProps} className="testimonials-viewport mt-12 w-full overflow-hidden select-none">
            <div ref={containerRef} className="testimonials-track flex gap-6" style={{ transform: 'translate3d(0px, 0px, 0px)' }}>
              {SLIDES.map((slide, i) => (
                <Slide key={i} ref={slideRef(i)} slide={slide} />
              ))}
            </div>
          </div>
        </div>
        <div className="flex flex-col items-center gap-8">
          <div className="flex flex-row gap-4">
            <button aria-label="Previous testimonial" className="cursor-default rounded-full bg-white/30 p-2 text-xl leading-none backdrop-blur" onClick={prev}>
              <img src="/assets/icons/review-prev.svg" alt="" width="13" height="13" />
            </button>
            <button aria-label="Next testimonial" className="cursor-default rounded-full bg-white/30 p-2 text-xl leading-none backdrop-blur" onClick={next}>
              <img src="/assets/icons/review-next.svg" alt="" width="13" height="13" />
            </button>
          </div>
          <Button data-button-id="home-testimonials-cta">Join the club</Button>
        </div>
      </div>
    </section>
  )
}
