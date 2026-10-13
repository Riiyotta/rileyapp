import { createPortal } from 'react-dom'
import Button from '../shared/Button.jsx'
import { MASCOTS } from './superpowersData.js'

const ONELINK = 'https://rileyapp.onelink.me/JNxh/nativeappstorebutton'

// §4.2 SuperpowerModal — portal into <body>, no entry animation.
export default function SuperpowerModal({ modal, onClose }) {
  if (!modal) return null
  const mascot = MASCOTS[modal.mascot]
  const titleId = `superpower-${modal.mascot}-title`

  return createPortal(
    <>
      <div aria-hidden="true" onClick={onClose} className="fixed inset-0 top-0 z-40 bg-black/40" />
      <div className="fixed inset-x-0 bottom-0 z-[1100] flex max-h-[100dvh] items-start justify-center overflow-y-auto rounded-3xl p-4 pb-0 shadow-2xl lg:inset-0 lg:items-center">
        <section
          role="dialog"
          aria-modal="true"
          aria-labelledby={titleId}
          className={`relative flex w-full max-w-[32rem] flex-col gap-4 rounded-3xl shadow-2xl lg:max-w-[90vw] lg:gap-12 lg:px-[100px] ${mascot.gradient}`}
        >
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="text-ink absolute top-6 right-6 z-10 text-3xl leading-none"
          >
            ×
          </button>
          <div className="relative flex flex-1 flex-col items-center gap-6 px-4">
            <img className="mt-6 h-[87px] w-[87px] object-contain" src={mascot.svg} alt="" width="87" height="87" />
            <header className="flex shrink-0 flex-col items-center gap-4 px-4 lg:px-12">
              <h2
                id={titleId}
                className="lg:desktop-h3 mobile-h3 text-text-primary mx-auto max-w-xs text-center font-serif lg:mt-0 lg:max-w-none"
              >
                {modal.title}
              </h2>
              <p className="lg:desktop-body mobile-body text-text-primary/80 max-w-xl text-center">{modal.subtitle}</p>
            </header>
            <div className="flex flex-col gap-6 lg:flex-row">
              {modal.features.map((f) => (
                <div key={f.title} className="flex flex-col lg:flex-row">
                  <article className="relative flex flex-1 flex-col items-center gap-2.5 rounded-3xl bg-white px-8 py-5 lg:min-h-[17rem] lg:min-w-[17rem]">
                    <div className="relative flex-1 self-stretch">
                      {f.icon && (
                        <img
                          src={`/assets/modal/icons/${f.icon}.svg`}
                          alt=""
                          width="32"
                          height="32"
                          className="absolute right-0 top-0 aspect-square h-auto w-[2rem] object-contain"
                        />
                      )}
                      <div className="flex flex-col gap-3 lg:gap-6">
                        <h3 className="lg:desktop-h4 mobile-h3 text-text-primary pr-12 font-serif leading-9">{f.title}</h3>
                        <p className="text-text-primary pr-12 text-[1rem] leading-6">{f.description}</p>
                      </div>
                    </div>
                  </article>
                </div>
              ))}
            </div>
          </div>
          <footer className="sticky bottom-0 z-10 shrink-0 items-center justify-center bg-white p-4 lg:bg-transparent lg:p-6">
            <div className="mx-auto flex max-w-[14rem]">
              <Button href={ONELINK} data-button-id="parenting-help-modal-cta" className="w-full">
                Get Started For Free
              </Button>
            </div>
          </footer>
        </section>
      </div>
    </>,
    document.body,
  )
}
