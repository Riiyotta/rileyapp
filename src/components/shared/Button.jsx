import { useState } from 'react'

// Primary purple CTA. Original sets colors via inline style on mouse events.
const COLORS = { base: '#5934C5', hover: '#7A55FD', active: '#5A20E1' }

// size="lg" (pricing CTA, marketing spec §1.4): 18/28 text, 384x60 at ≥640, 16/24 and 56 tall below.
const SIZES = {
  md: 'text-base leading-6',
  lg: 'mx-auto min-h-[56px] max-w-[24rem] text-base sm:text-lg',
}

// `colors` (optional): { base, hover, active } merged over COLORS, e.g. the article PromoUnit (#7B63F5 / #5A20E1).
export default function Button({ children, href, className = '', style, size = 'md', icon = null, colors, ...rest }) {
  const palette = colors ? { ...COLORS, ...colors } : COLORS
  // Original keeps two flags: hovered / pressed; color = pressed ? active : hovered ? hover : base
  const [hovered, setHovered] = useState(false)
  const [pressed, setPressed] = useState(false)
  const state = pressed ? 'active' : hovered ? 'hover' : 'base'
  const Tag = href ? 'a' : 'button'
  return (
    <Tag
      href={href}
      className={`button-primary font-sans-bold inline-flex w-full items-center justify-center gap-3.5 whitespace-nowrap rounded-[2rem] px-8 py-4 ${SIZES[size]} transition-all duration-300 cursor-pointer ${className}`}
      style={{ backgroundColor: palette[state], color: '#FFF', ...style }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => {
        setHovered(false)
        setPressed(false)
      }}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onTouchStart={() => setPressed(true)}
      onTouchEnd={() => setPressed(false)}
      {...rest}
    >
      <span className="flex max-w-full items-center justify-center gap-2 px-5">
        {children}
        {icon}
      </span>
    </Tag>
  )
}
