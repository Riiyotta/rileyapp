import AnnouncementBar from '../components/AnnouncementBar.jsx'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import SiteFooter from '../components/SiteFooter.jsx'

// Blog spec §5: /tos, /privacy, /cookies. On the live site the Termly embed script is blocked by the site's own
// CSP, so <main> renders empty (0px): AnnouncementBar + SiteHeader + empty main + SiteFooter. Replicated as
// rendered — no embed script is loaded and no policy text is included.
const POLICY_UUIDS = {
  tos: '1b687b5a-20d7-48f3-be50-cae504edce40',
  privacy: '8c6a0cc4-5004-4ad9-a563-ee70e8d1d3a6',
  cookies: 'eb7f04dc-b468-448d-8d88-24933fb4f3cb',
}

export default function LegalPage({ kind = 'tos' }) {
  return (
    <>
      <AnnouncementBar />
      <SiteHeader />
      <main>
        <div name="termly-embed" data-id={POLICY_UUIDS[kind]} />
      </main>
      <SiteFooter />
    </>
  )
}
