import Button from '../shared/Button.jsx'

// §9.1 FeatureCards
const CARDS = [
  {
    bg: 'bg-apricot',
    img: '/assets/chat.svg',
    title: '24/7 Personalized Support',
    body: (
      <>Real-time, science-backed advice tailored to <strong>your baby's needs</strong> and <strong>your parenting style</strong>—available <strong>whenever</strong> you need it (even at 3am).</>
    ),
  },
  {
    bg: 'bg-violet-100',
    img: '/assets/tracking.svg',
    title: 'Smart, Predictive Tracking',
    body: (
      <>Riley doesn't just store your data, it <strong>learns and grows with you</strong>. Track sleep, feed, diapers, development and more to stay on top of what's next for your baby. </>
    ),
  },
  {
    bg: 'bg-marigold',
    img: '/assets/sparks.svg',
    title: 'Tips Tailored Just for You',
    body: (
      <>No more endless Googling. Riley gives you <strong>helpful tips made just for your family</strong>—so you can parent with a little more ease (and a lot less guesswork).</>
    ),
  },
]

export default function FeatureCards() {
  return (
    <section className="text-text-primary mx-auto flex max-w-[90rem] flex-col items-center gap-6 self-stretch rounded-3xl bg-white px-2 py-4 max-md:px-5 lg:gap-12 lg:p-12">
      <header className="text-text-primary flex flex-col items-center gap-6 self-stretch text-center max-md:max-w-full">
        <h3 className="text-text-primary lg:desktop-body mobile-body"><br />Parenting is hard. Riley makes it easier.</h3>
        <h2 className="lg:desktop-h3 mobile-h2 text-text-primary font-serif max-md:max-w-full">One App for All Your Parenting Needs</h2>
      </header>
      <div className="flex w-full flex-col items-start gap-5 self-stretch text-center max-md:max-w-full lg:flex-row">
        {CARDS.map((card) => (
          <article key={card.title} className={`flex h-full max-h-[25rem] min-w-60 flex-1 basis-0 flex-col gap-7 rounded-3xl px-8 pb-12 pt-8 max-md:px-5 ${card.bg}`}>
            <img alt={card.title} loading="lazy" width="333" height="167" decoding="async" className="h-full w-full self-center lg:h-[10.25rem] lg:w-auto" src={card.img} />
            <div className="flex w-full flex-col items-start gap-4 self-stretch text-center">
              <h4 className="lg:desktop-h4 mobile-h3 text-text-primary w-full text-center">{card.title}</h4>
              <p className="text-text-primary mobile-body">{card.body}</p>
            </div>
          </article>
        ))}
      </div>
      <div className="flex max-w-[14rem]">
        <Button>Get Started For Free</Button>
      </div>
    </section>
  )
}
