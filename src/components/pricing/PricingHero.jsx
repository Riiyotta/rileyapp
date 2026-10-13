import Button from '../shared/Button.jsx'
import HeroParallaxClouds from '../upper/HeroParallaxClouds.jsx'
import PlanCard from './PlanCard.jsx'

// Marketing spec §3 PricingHero. CTA destination: original lands on the App Store via JS (§3.6, redirect
// UNVERIFIED); the homepage onelink is used as the equivalent.
const ONELINK = 'https://rileyapp.onelink.me/JNxh/nativeappstorebutton'

const FEATURES = [
  'Unlimited Children & Tracking',
  '3+ Caregivers with their own logins',
  'Unlimited Chats',
  'Tracking Insights',
  'Seamless Sharing',
  'Advanced Memory & Customization',
]

// Inlined from /assets/pages/pricing/apple-small.svg (fill=currentColor → text-text-primary)
function AppleSmall() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4 text-text-primary" aria-hidden="true">
      <path d="M18.71 19.5C17.88 20.74 17 21.95 15.66 21.97C14.32 21.99 13.89 21.18 12.37 21.18C10.84 21.18 10.37 21.95 9.1 21.99C7.79 22.03 6.8 20.68 5.96 19.47C4.25 17 2.94 12.45 4.7 9.39C5.57 7.87 7.13 6.91 8.82 6.88C10.1 6.86 11.32 7.75 12.11 7.75C12.89 7.75 14.37 6.68 15.92 6.84C16.57 6.87 18.39 7.1 19.56 8.82C19.47 8.88 17.39 10.19 17.41 12.63C17.44 15.65 20.06 16.66 20.09 16.67C20.06 16.74 19.67 18.11 18.71 19.5ZM13 3.5C13.73 2.67 14.94 2.04 15.94 2C16.07 3.17 15.6 4.35 14.9 5.19C14.21 6.04 13.07 6.7 11.95 6.61C11.8 5.46 12.36 4.26 13 3.5Z" />
    </svg>
  )
}

// Inlined from /assets/pages/pricing/button-arrow.svg (fill=currentColor → white)
function ButtonArrow() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="17" viewBox="0 0 16 17" fill="none" aria-hidden="true">
      <path
        d="M9.00098 3.64331C9.18353 3.6434 9.35821 3.71637 9.4873 3.84546L13.9873 8.34546C14.0514 8.40942 14.103 8.48543 14.1377 8.56909C14.1722 8.65262 14.1896 8.74237 14.1895 8.83276C14.1893 8.92326 14.1715 9.0129 14.1367 9.09644C14.1193 9.13832 14.0975 9.17811 14.0723 9.21558L13.9863 9.32007L9.48633 13.8201C9.35717 13.9491 9.18162 14.0212 8.99902 14.0212L8.86426 14.0085C8.73202 13.9821 8.60952 13.9168 8.5127 13.8201C8.38353 13.6909 8.31055 13.5154 8.31055 13.3328C8.31055 13.1958 8.35186 13.0633 8.42676 12.9509L8.5127 12.8455L11.7314 9.62769L11.8389 9.52124H2.5C2.31766 9.52124 2.1426 9.44802 2.01367 9.31909C1.88502 9.19028 1.8126 9.0158 1.8125 8.83374C1.8125 8.65149 1.88486 8.47633 2.01367 8.34741C2.11038 8.25071 2.23307 8.18535 2.36523 8.15894L2.5 8.14624H11.8379L11.7314 8.03882L8.51367 4.81909C8.3845 4.68992 8.31152 4.51447 8.31152 4.33179L8.3252 4.19702C8.35166 4.06472 8.41689 3.9423 8.51367 3.84546C8.64285 3.71628 8.8183 3.64331 9.00098 3.64331Z"
        fill="currentColor"
        stroke="currentColor"
        strokeWidth="0.125"
      />
    </svg>
  )
}

const PLANS = [
  {
    name: 'Riley Plus+',
    description: 'For families who parent as a team',
    avatars: ['/assets/purple1.svg', '/assets/purple2.svg', '/assets/purple3.svg'],
    tagline: 'Try it free for 7 days',
    features: FEATURES.map((label) => ({ label, included: true })),
    price: (
      <>
        <p className="mb-2 font-sans-regular text-sm text-text-primary/70">Starting at</p>
        <div className="font-serif text-[28px] text-text-primary sm:text-[32px]">
          $9.99 <span className="text-[14px] text-text-primary/70 sm:text-[16px]">/ month</span>
        </div>
        <p className="font-sans-regular text-sm text-text-primary/70">Billed monthly, quarterly or annually</p>
        <p className="font-sans-semibold text-sm text-sea-green-100">Your first 7 days are free</p>
      </>
    ),
  },
  {
    name: 'Riley Basic',
    description: 'For solo parenting or simpler setups',
    avatars: ['/assets/purple1.svg'],
    tagline: 'Always free',
    features: FEATURES.map((label, i) => ({ label, included: i === 0 })),
    price: (
      <>
        <div className="mb-2 font-serif text-[28px] text-text-primary sm:text-[32px]">Free</div>
        <p className="flex items-center gap-2 font-sans-regular text-sm text-text-primary/70">
          Available on:
          <AppleSmall />
        </p>
      </>
    ),
  },
]

export default function PricingHero() {
  return (
    <section className="relative isolate w-full overflow-x-hidden">
      <div className="absolute inset-0 -z-40 bg-pricing-radial" />
      <HeroParallaxClouds withBg={false} className="pointer-events-none absolute inset-0 -z-20 opacity-70" />
      <div className="relative z-10">
        <div className="py-8 sm:py-12 lg:py-16">
          <div className="mb-8 flex flex-col items-center gap-2 px-4 sm:mb-12">
            <p className="mobile-h4 text-center font-sans-regular text-text-primary lg:text-[1.25rem]">Parenting Made Simple</p>
          </div>
          <div className="mx-auto w-full max-w-[80rem] px-4 sm:px-6 lg:px-14">
            <div className="mb-8 text-center sm:mb-12">
              {/* size comes from the unlayered h1 rule in index.css (64/72 ≥992, 40/48 below); original `mobile-h1 lg:desktop-h1` dropped because in v3 the class would out-specify the h1 rule */}
              <h1 className="mb-4 font-serif text-text-primary">
                Expert Guidance,
                <br />
                Tailored To Your Family
              </h1>
            </div>
            <div className="mx-auto mb-8 grid max-w-[56rem] gap-6 sm:mb-12 sm:gap-8 md:grid-cols-2">
              {PLANS.map((plan) => (
                <PlanCard key={plan.name} {...plan} />
              ))}
            </div>
            <div className="px-4 text-center sm:px-0">
              <Button href={ONELINK} size="lg" icon={<ButtonArrow />} data-button-id="pricing-cta">
                Get Started For Free
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
