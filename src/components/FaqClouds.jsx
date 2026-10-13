import { useEffect, useRef, useState } from 'react'
import Button from './shared/Button.jsx'

// §10 FaqClouds. Positions, open/blur states and cloud motion (M8, M8b, M9) are in styles/lower.css.
const FAQS = [
  {
    portrait: '/assets/4.png',
    q: 'How do I know I can trust Riley?',
    a: "Riley's advice is grounded in the latest pediatric research and expert knowledge. We work closely with pediatricians, child development specialists, and parenting experts to ensure our information is accurate and up-to-date. Plus, Riley learns from your experiences, becoming more personalized and helpful over time.",
  },
  {
    portrait: '/assets/5.png',
    q: 'How is Riley different from ChatGPT or other parenting apps?',
    a: 'Riley isn’t just another chatbot. It learns from your baby’s age, symptoms, tracking history, and anything that\'s worked for your family in the past. Delivering expert-vetted advice that fits your family, not just “most families.”',
    trailingEmptyP: true,
  },
  {
    portrait: '/assets/3.png',
    q: 'What can’t I ask Riley?',
    a: 'Riley gives science-backed, personalized parenting support - but it’s not a doctor, therapist, or emergency service. It’s here for guidance on sleep, feeds, development, routines, and real-life questions - not for diagnosing medical conditions. ',
  },
  {
    portrait: '/assets/2.png',
    q: 'Are you going to keep my kids’ data private?',
    a: "Your family's privacy is our top priority. We use bank-level encryption to protect your data, and we never share your information with third parties. Riley's personalized advice is generated just for you, based on the information you choose to share. You're always in control of your data, and you can delete it at any time. Riley was built to support your parenting - not to profit from your info.",
  },
  {
    portrait: '/assets/6.png',
    q: 'Do I need to track everything for Riley to work?',
    a: 'Nope. Tracking helps tailor the experience, but Riley gives helpful, relevant support even if you skip a day - or a week.',
    trailingEmptyP: true,
  },
]

const CLOUDS = [
  { src: '/assets/icons/faq-cloud-1.svg', w: 452, h: 276 },
  { src: '/assets/icons/faq-cloud-2.svg', w: 326, h: 199 },
  { src: '/assets/icons/faq-cloud-3.svg', w: 244, h: 149 },
  { src: '/assets/icons/faq-cloud-4.svg', w: 383, h: 167 },
  { src: '/assets/icons/faq-cloud-5.svg', w: 401, h: 246 },
]

export default function FaqClouds() {
  const [openIndex, setOpenIndex] = useState(null)
  const [clearSkies, setClearSkies] = useState(false)
  const bgRef = useRef(null)

  // M8b: once 20% of the clouds layer is visible, wait 1s then move clouds to the edges (fires once).
  useEffect(() => {
    const el = bgRef.current
    if (!el) return
    let timer
    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          io.disconnect()
          timer = setTimeout(() => setClearSkies(true), 1000)
        }
      },
      { threshold: 0.2 },
    )
    io.observe(el)
    return () => { io.disconnect(); clearTimeout(timer) }
  }, [])

  const onToggle = (i) => (e) => {
    const isOpen = e.currentTarget.open
    setOpenIndex((cur) => (isOpen ? i : cur === i ? null : cur))
  }

  return (
    <section className={`faq-clouds flex min-h-[900px] w-full ${openIndex !== null ? 'blurred' : ''}`} aria-labelledby="faq-clouds-title">
      <div className="relative flex w-full">
        <div className="mx-auto flex w-full max-w-[90rem] items-center justify-center">
          <h2 id="faq-clouds-title" className="desktop-h2 mx-auto max-w-[50rem] text-center text-ink">We’re Here to Make Things Clear</h2>
        </div>
        <div className="absolute h-full w-full">
          {FAQS.map((f, i) => (
            <details key={f.q} className="faq-clouds-item max-w-xs cursor-pointer rounded-3xl bg-white p-4 shadow-md" onToggle={onToggle(i)}>
              <summary className="flex list-none items-center gap-4 font-bold">
                <img alt="FAQ portrait" className="h-10 w-10 rounded-full object-cover" src={f.portrait} />
                <span>{f.q}</span>
                <img className="faq-plus" src="/assets/icons/faq-plus.svg" alt="" width="19" height="19" />
              </summary>
              <div className="lower-prose mt-2 max-w-none px-3">
                <div>
                  <p><span className="text-black">{f.a}</span></p>
                  {f.trailingEmptyP && <p />}
                </div>
                <div className="flex items-center gap-2">
                  <Button href="/pricing" className="!leading-7">Learn More</Button>
                  <img alt="Riley mascot" width="102" height="83" decoding="async" className="mb-2 mt-0 h-[5rem] w-auto" src="/assets/riley-up.svg" />
                </div>
              </div>
            </details>
          ))}
        </div>
      </div>
      <div ref={bgRef} className={`faq-clouds-bg ${clearSkies ? 'clear-skies' : ''}`} aria-hidden="true">
        {CLOUDS.map((c) => (
          <img key={c.src} src={c.src} alt="" width={c.w} height={c.h} />
        ))}
      </div>
    </section>
  )
}
