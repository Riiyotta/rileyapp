import Button from '../shared/Button.jsx'

// §9.2 ComparisonTable ("Why Riley Stands Out"); ≤960px rotated-header rules live in styles/lower.css
const COLUMNS = ['Riley', 'Google Search', 'Reddit', 'ChatGPT', 'Claude', 'Other Tracking Apps', 'Podcasts, Books, & Blogs']

// 1 = filled check, 0 = empty check; column order as COLUMNS
const ROWS = [
  ['24/7 Instant Answers', [1, 1, 1, 1, 1, 0, 0]],
  ['Expert-Vetted, Science Backed Support', [1, 0, 0, 0, 0, 0, 1]],
  ['Guidance Tailored to You & Your Family', [1, 0, 0, 0, 0, 0, 0]],
  ['Proactively Turns Tracking Into Tips', [1, 0, 0, 0, 0, 0, 0]],
  ['All-In-One Tracking & Support', [1, 0, 0, 0, 0, 1, 0]],
]

const CELL = 'mobile-h4 lg:desktop-h4 border-l border-black bg-white px-6 py-3 text-center shadow-sm'

function Check({ filled }) {
  return filled ? (
    <img src="/assets/icons/table-check-filled.svg" alt="Yes" width="29" height="29" className="mx-auto max-w-none" />
  ) : (
    <img src="/assets/icons/table-check-empty.svg" alt="No" width="31" height="30" className="mx-auto max-w-none" />
  )
}

export default function ComparisonTable() {
  return (
    <section className="why-riley-stands-out text-text-primary mx-auto w-full max-w-[90rem] rounded-3xl bg-white px-2 py-4 max-md:px-5 lg:p-12" aria-labelledby="why-riley-title">
      <header className="mt-4 flex w-full flex-col items-center gap-3 self-stretch text-center lg:gap-8">
        <p className="lg:desktop-body">Designed with Real Parents in Mind</p>
        <h2 id="why-riley-title" className="mobile-h2 lg:desktop-h3 font-serif">Why Riley Stands Out</h2>
        <div className="lower-prose max-w-[25rem]">
          <div>
            <p>See how Riley outshines other parenting tools with <strong>intelligent features</strong> and <strong>tailored advice</strong>. It’s the <strong>one-stop-shop</strong> for all your parenting needs!</p>
          </div>
        </div>
      </header>
      <div className="mx-auto mt-6 w-full max-w-6xl lg:mt-12">
        <div className="overflow-x-auto rounded-2xl bg-latte-150 p-6 px-3 lg:p-6">
          <table className="w-full border-separate border-spacing-y-4 text-left">
            <thead>
              <tr className="text-center">
                <th className="px-4 font-bold">Feature/Benefit</th>
                {COLUMNS.map((c) => (
                  <th key={c} className="px-4 font-normal"><span>{c}</span></th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ROWS.map(([label, marks]) => (
                <tr key={label}>
                  <td className={`${CELL} rounded-l-2xl border-none !text-left`}>{label}</td>
                  {marks.map((m, i) => (
                    <td key={i} className={`${CELL} ${i === marks.length - 1 ? 'rounded-r-2xl' : ''}`}>
                      <Check filled={m === 1} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="mx-auto mt-12 flex w-full max-w-[15rem]">
        <Button>Join Riley—early, easy, free</Button>
      </div>
    </section>
  )
}
