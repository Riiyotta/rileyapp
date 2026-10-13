import { useState } from 'react'
import SuperpowerModal from './upper/SuperpowerModal.jsx'
import { SUPERPOWERS } from './upper/superpowersData.js'

// §4 Superpowers (+ §4.2 modal). Card hover: §14 M12.
export default function Superpowers() {
  const [active, setActive] = useState(null)

  const onKeyDown = (e, i) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      setActive(i)
    }
  }

  return (
    <section className="text-text-primary relative mx-auto flex w-full max-w-[90rem] flex-col items-center justify-center px-4 py-4 max-md:px-5 lg:px-11 2xl:px-4">
      <div className="flex w-full flex-col items-center gap-10 rounded-3xl bg-violet-100 px-4 pt-[60px] pb-[7.5rem] max-md:max-w-full max-md:px-5 max-md:pb-24 lg:gap-12 lg:px-56 lg:pt-20">
        <h2 className="mobile-h2 lg:desktop-h3 text-text-primary max-w-[33.5rem] text-center font-serif max-md:max-w-full">
          What Parenting Superpower Do You Need Today?
        </h2>
        <div className="grid w-full gap-9 lg:grid-cols-2 lg:gap-9">
          {SUPERPOWERS.map((item, i) => (
            <article
              key={item.text}
              role="button"
              tabIndex={0}
              onClick={() => setActive(i)}
              onKeyDown={(e) => onKeyDown(e, i)}
              className="flex w-full cursor-auto items-center justify-between gap-10 rounded-3xl bg-white px-5 py-4 shadow transition hover:bg-gray-50"
            >
              <div className="flex items-center gap-5">
                <img alt="" width="40" height="40" className="aspect-square w-10 shrink-0 object-contain" src={item.icon} />
                <span className="text-text-primary lg:desktop-h4 mobile-h4 font-serif">{item.text}</span>
              </div>
              <img src="/assets/icons/card-arrow.svg" alt="" width="13" height="12" className="min-w-0 object-contain" />
            </article>
          ))}
        </div>
      </div>
      <img alt="Riley" width="177" height="179" className="absolute -bottom-20 left-12" src="/assets/mascot.svg" />
      <SuperpowerModal modal={active === null ? null : SUPERPOWERS[active].modal} onClose={() => setActive(null)} />
    </section>
  )
}
