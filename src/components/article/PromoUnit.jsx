import Button from '../shared/Button.jsx'

// Blog spec §3.7. Card gradient = original `bg-greenGradient`. Button: base #7B63F5 (inline on the original),
// mousedown #5A20E1, hover UNVERIFIED (kept at base). Click target UNVERIFIED (no href in the original DOM).
const PROMO_COLORS = { base: '#7B63F5', hover: '#7B63F5', active: '#5A20E1' }

export default function PromoUnit({ text }) {
  return (
    <div className="relative mx-auto mb-16 flex w-full max-w-[90rem] items-center justify-center self-stretch px-5 xl:mt-20 xl:px-[6.25rem]">
      <div
        className="flex w-full flex-1 flex-col items-center gap-6 rounded-3xl px-5 py-8 xl:gap-4 xl:px-0"
        style={{ background: 'linear-gradient(253.62deg, #FFDF78 5.6%, #D2F2D2 72.1%)' }}
      >
        {/* w-full added so the inner column reaches its 638px max regardless of copy length (measured 638 @1440) */}
        <div className="mx-auto flex w-full max-w-[638px] flex-col items-center gap-8 xl:gap-6">
          <p className="my-5 text-center text-base leading-7 text-gray-700">{text}</p>
          <Button colors={PROMO_COLORS} className="!leading-7" data-button-id="final-cta" type="button">
            Get Started
          </Button>
        </div>
      </div>
    </div>
  )
}
