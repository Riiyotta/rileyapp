// §6 ClinicalBoard
const ADVISORS = [
  { img: '/assets/lilly.png', alt: 'Portrait of Dr. Lilly Jay', name: 'Dr. Lilly Jay', role: 'PsyD, PMH-C, Perinatal Health' },
  { img: '/assets/kate.png', alt: 'Portrait of Dr. Kate Roche', name: 'Dr. Kate Roche', role: 'MD, Child Neurology' },
]

export default function ClinicalBoard() {
  return (
    <section className="text-text-primary flex flex-col bg-white px-24 py-16 max-md:px-5">
      <div className="mx-auto flex w-full max-w-[90rem] flex-col items-center gap-16 self-stretch">
        <header className="flex w-full flex-col items-center gap-10 text-center text-xl leading-tight max-md:max-w-full">
          <h3 className="text-text-primary mobile-body lg:desktop-body">Our Clinical Advisory Board</h3>
          <h2 className="text-text-primary mobile-h2 lg:desktop-h3 self-stretch font-serif max-md:max-w-full">
            Designed with Experts, for Real Families
          </h2>
          <p className="text-text-primary lg:desktop-body mobile-body w-full max-w-[30.75rem] max-md:max-w-full">
            <span className="font-sans-bold">Our Clinical Advisory Board </span>includes{' '}
            <span className="font-sans-bold">pediatricians, therapists,</span> and{' '}
            <span className="font-sans-bold">specialists</span>, who help us keep Riley grounded in real,{' '}
            <span className="font-sans-bold">evidence-based support</span>.
          </p>
        </header>
        <div className="mx-auto flex w-full flex-col items-center justify-center gap-12 text-center max-md:max-w-full lg:flex-row">
          {ADVISORS.map((a) => (
            <article key={a.name} className="flex min-w-60 max-w-[22.625rem] flex-col items-center justify-center">
              <img alt={a.alt} width="360" height="360" className="aspect-[0.99] w-[362px] max-w-full object-contain" src={a.img} />
              <div className="mt-8 flex w-[334px] max-w-full flex-col items-center justify-center rounded-none px-9 py-2 max-md:px-5">
                <div className="flex max-w-full flex-col">
                  <h3 className="text-xl leading-tight text-slate-800">{a.name}</h3>
                  <p className="mt-4 self-center text-base leading-snug text-slate-800">{a.role}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
