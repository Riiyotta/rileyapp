// §1 AnnouncementBar — hidden below 992px.
export default function AnnouncementBar() {
  return (
    <div>
      <aside
        role="complementary"
        aria-label="Promotional message"
        className="hidden w-full items-center justify-center bg-violet-100 px-0 py-3 text-center text-base leading-8 tracking-normal text-text-primary lg:flex"
      >
        <div className="font-sans-regular max-w-none text-center text-[1rem] leading-[1.9rem] tracking-[-0.01rem] text-gray-700">
          <p className="m-0">
            <a target="_self" href="https://rileyapp.com/pricing" className="font-medium text-gray-900 underline">
              Try Riley risk free with our 7-day free trial!
            </a>
          </p>
        </div>
      </aside>
    </div>
  )
}
