// Marketing spec §3.5 PlanCard. Icon SVGs are the extracted inline originals
// (/assets/pages/pricing/plan-check.svg, plan-x.svg) inlined so they keep the original svg box metrics.
function CheckIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" className="mt-0.5 flex-shrink-0" aria-hidden="true">
      <path
        d="M18.1633 6.28833L8.16328 16.2883C8.07618 16.3757 7.97269 16.4451 7.85873 16.4924C7.74478 16.5397 7.6226 16.5641 7.49922 16.5641C7.37583 16.5641 7.25365 16.5397 7.1397 16.4924C7.02574 16.4451 6.92225 16.3757 6.83515 16.2883L2.46015 11.9133C2.37295 11.8261 2.30377 11.7226 2.25658 11.6087C2.20938 11.4947 2.18509 11.3726 2.18509 11.2493C2.18509 11.1259 2.20938 11.0038 2.25658 10.8899C2.30377 10.7759 2.37295 10.6724 2.46015 10.5852C2.54736 10.498 2.65089 10.4288 2.76483 10.3816C2.87877 10.3344 3.00089 10.3101 3.12422 10.3101C3.24754 10.3101 3.36966 10.3344 3.4836 10.3816C3.59754 10.4288 3.70107 10.498 3.78828 10.5852L7.5 14.2969L16.8367 4.96177C17.0128 4.78565 17.2517 4.68671 17.5008 4.68671C17.7498 4.68671 17.9887 4.78565 18.1648 4.96177C18.341 5.13789 18.4399 5.37676 18.4399 5.62583C18.4399 5.8749 18.341 6.11378 18.1648 6.2899L18.1633 6.28833Z"
        fill="#008A56"
      />
    </svg>
  )
}

function CrossIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="21" viewBox="0 0 20 21" fill="none" className="mt-0.5 flex-shrink-0" aria-hidden="true">
      <path
        d="M15.6255 3.83014C15.858 3.83014 16.0813 3.92258 16.2457 4.08698C16.41 4.25137 16.5025 4.47461 16.5025 4.70709C16.5024 4.93938 16.4099 5.16193 16.2457 5.32623L11.2838 10.2891L11.2398 10.3331L11.2838 10.378L16.2437 15.3389C16.4081 15.5033 16.5005 15.7266 16.5005 15.959C16.5005 16.1915 16.4081 16.4148 16.2437 16.5792C16.0794 16.7433 15.8568 16.8359 15.6246 16.836C15.3921 16.836 15.1688 16.7435 15.0045 16.5792L10.0445 11.6172L9.99957 11.5733L9.95563 11.6172L4.99371 16.5772C4.8294 16.7415 4.60691 16.834 4.37457 16.834C4.14208 16.834 3.91885 16.7416 3.75446 16.5772C3.5901 16.4128 3.49762 16.1896 3.49762 15.9571C3.49774 15.7248 3.59022 15.5022 3.75446 15.338L8.71637 10.378L8.76031 10.3331L8.71637 10.2891L3.75641 5.32721C3.59201 5.16281 3.49957 4.93959 3.49957 4.70709C3.49969 4.47476 3.59212 4.25224 3.75641 4.08795C3.92074 3.92367 4.14319 3.83118 4.37555 3.83112C4.60805 3.83112 4.83127 3.92355 4.99567 4.08795L9.95563 9.04987L9.99957 9.09381L10.0445 9.04987L15.0064 4.08698C15.1707 3.92276 15.3932 3.83021 15.6255 3.83014Z"
        fill="#ED614B"
        stroke="#ED614B"
        strokeWidth="0.125"
      />
    </svg>
  )
}

export default function PlanCard({ name, description, avatars, tagline, features, price }) {
  return (
    <div className="rounded-2xl border border-latte-125 bg-white p-6 sm:rounded-3xl sm:p-8">
      <div className="mb-6">
        <h3 className="mb-2 font-serif text-[28px] text-text-primary sm:text-[32px]">{name}</h3>
        <p className="mb-2 font-sans-regular text-sm text-text-primary/70 sm:text-base">
          {description}
          <span className={`ml-2 inline-flex items-center${avatars.length > 1 ? ' gap-0.5' : ''}`}>
            {avatars.map((src, i) => (
              <img key={i} src={src} alt="Riley avatar" width="24" height="24" className="h-5 w-5 sm:h-6 sm:w-6" />
            ))}
          </span>
        </p>
        <p className="font-sans-semibold text-sm text-sea-green-100">{tagline}</p>
      </div>
      <div className="mb-6 sm:mb-8">
        <hr className="mb-4 border-t border-latte-125" />
        <ul className="space-y-2.5 sm:space-y-3">
          {features.map(({ label, included }) => (
            <li key={label} className="flex items-start gap-2.5 sm:gap-3">
              {included ? <CheckIcon /> : <CrossIcon />}
              <span className="font-sans-regular text-sm text-text-primary">{label}</span>
            </li>
          ))}
        </ul>
        <hr className="mt-4 border-t border-latte-125" />
      </div>
      <div className="mb-6">{price}</div>
    </div>
  )
}
