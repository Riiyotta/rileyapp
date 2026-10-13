import Button from './shared/Button.jsx'

// §7 How Riley Works
const ITEMS = [
  {
    img: '/assets/worrier-family.svg',
    title: 'Built on science\nthat matters',
    body: 'When answering your questions, Riley draws from the latest child development research, expert-reviewed sources that are vetted by our Clinical Advisory Board.',
  },
  {
    img: '/assets/guide-family.svg',
    title: 'Powered by tech that learns\nand grows with you',
    body: 'Once you start using Riley, it doesn’t just log or respond to you, it safely remembers. From tracking to what’s worked in the past, Riley learns from you to offer relevant guidance.  ',
  },
  {
    img: '/assets/spark-family.svg',
    title: 'Clarity without ignoring\nyour individuality',
    body: "Every family is different, Riley gets that! You'll receive clear, science-backed guidance that respects your individual parenting style and real-life context.",
  },
]

export default function HowRileyWorks() {
  return (
    <section className="text-text-primary bg-latte-100 flex w-full flex-col items-center p-20 max-md:px-5 2xl:px-4">
      <div className="mx-auto flex max-w-[90rem] flex-col gap-[60px] self-stretch">
        <h2 className="lg:desktop-h2 mobile-h1 text-center font-serif">How Riley Works</h2>
        <div className="flex w-full flex-col items-start justify-center gap-[60px] max-md:max-w-full lg:flex-row lg:justify-between lg:gap-0">
          {ITEMS.map((item) => (
            <article key={item.img} className="flex min-w-60 flex-1 basis-0 flex-col items-center gap-8 px-12 max-md:max-w-full">
              <div className="relative flex h-[8.75rem] w-full items-center justify-center">
                <img alt={item.title} width="214" height="135" decoding="async" className="object-contain" src={item.img} />
              </div>
              <div className="flex w-full flex-col items-center gap-4 text-center lg:gap-8">
                <h3 className="lg:desktop-h4 mobile-h3 text-text-primary whitespace-pre-line">{item.title}</h3>
                <p className="lg:desktop-body mobile-body text-text-primary w-full">{item.body}</p>
              </div>
            </article>
          ))}
        </div>
        <div className="mx-auto flex w-full max-w-[14rem]">
          <Button data-button-id="how-riley-works-cta">Get Started For Free</Button>
        </div>
      </div>
    </section>
  )
}
