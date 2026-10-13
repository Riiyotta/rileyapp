import AnnouncementBar from '../components/AnnouncementBar.jsx'
import SiteHeader from '../components/upper/SiteHeader.jsx'
import PricingHero from '../components/pricing/PricingHero.jsx'
import Testimonials from '../components/Testimonials.jsx'
import GradientBand from '../components/GradientBand.jsx'
import FaqClouds from '../components/FaqClouds.jsx'
import FinalCta from '../components/FinalCta.jsx'
import SiteFooter from '../components/SiteFooter.jsx'

// Marketing spec §1.2: everything after the AnnouncementBar sits in one page wrapper.
export default function PricingPage() {
  return (
    <>
      <AnnouncementBar />
      <div className="relative flex flex-col items-start overflow-hidden">
        <SiteHeader />
        <PricingHero />
        <Testimonials />
        <GradientBand showFeatureCards={false} />
        <FaqClouds />
        <FinalCta />
        <SiteFooter />
      </div>
    </>
  )
}
