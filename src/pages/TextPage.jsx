import { Fragment } from 'react'
import AnnouncementBar from '../components/AnnouncementBar.jsx'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import SiteFooter from '../components/SiteFooter.jsx'

// Blog spec §4: /editorial-process. Section has NO horizontal padding (original quirk: text runs edge to edge).
// No FinalCta. Heading structure is the real one; all copy is placeholder (content policy).
const SECTIONS = [
  { title: 'Content Development', bullets: 3, labelled: true },
  { title: 'Review and Editing', bullets: 3, labelled: true },
  { title: 'Clinical Advisory Board Review', bullets: 3, labelled: true },
  { title: 'Final Approval and Publication', bullets: 2, labelled: true },
  { title: 'Ongoing Maintenance', bullets: 2, labelled: true },
  { title: 'Editorial Standards', bullets: 7, labelled: false },
]

export default function TextPage() {
  return (
    <>
      <AnnouncementBar />
      <SiteHeader />
      <main>
        <section className="tp-prose mx-auto mt-8 max-w-[90rem] text-text-primary">
          <h2>
            <span><strong>Riley's Editorial Process</strong></span>
          </h2>
          <p className="tp-intro">
            <span>Placeholder introduction — the full editorial process page is on rileyapp.com.</span>
          </p>
          {SECTIONS.map((s) => (
            <Fragment key={s.title}>
              <h3><span>{s.title}</span></h3>
              <ul>
                {Array.from({ length: s.bullets }, (_, i) => (
                  <li key={i}>
                    <p>
                      {s.labelled && <strong>Placeholder label {i + 1}:</strong>}
                      {s.labelled ? ' ' : ''}
                      <span>Placeholder sentence for this step of the process.</span>
                    </p>
                  </li>
                ))}
              </ul>
            </Fragment>
          ))}
          <p className="tp-closing">
            <span>Placeholder closing paragraph — questions can be sent through </span>
            <a href="https://rileyapp.com/support"><u>our support form</u></a>
            <span>. </span>
            <a href="https://rileyapp.com/editorial-process" target="_blank" rel="noopener noreferrer">
              Read the full page on rileyapp.com
            </a>
            <span>.</span>
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  )
}
