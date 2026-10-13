import { getCategory } from './categories.js'

// Blog spec §0.2. size="large": 24px icon, Cadiz Bold label (featured banner, §2.5a).
// size="small": 16px icon, Cadiz Regular label (grid cards).
// Pass either `post` (blogPosts.json object) or `category` (+ optional `label`).
export default function CategoryTag({ post, category = post?.category, label, size = 'small', className = '' }) {
  const cat = getCategory(category)
  const text = label ?? post?.subcategory ?? cat.title
  const iconW = size === 'large' ? 24 : 16
  return (
    <div
      className={`flex items-center justify-start gap-1 rounded-full px-4 py-2 ${className}`}
      style={{ backgroundColor: cat.bg }}
    >
      {cat.icon && <img src={cat.icon} alt={`${category} icon`} width={iconW} style={{ width: iconW, height: 'auto' }} />}
      <span className={`${size === 'large' ? 'font-sans-bold' : 'font-sans-regular'} text-base leading-6 text-text-primary`}>
        {text}
      </span>
    </div>
  )
}
