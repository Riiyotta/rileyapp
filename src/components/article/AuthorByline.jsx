// Blog spec §3.3: avatar 82 wide (natural aspect: 82x82 or 82x80.3), label / name link / title, all 16/24 #0a0a0a.
export default function AuthorByline({ label, name, title, image, href }) {
  return (
    <div className="flex items-center gap-4 self-stretch">
      {image && <img src={image} alt={name} width="82" className="h-auto w-[82px] shrink-0 rounded-full" />}
      <div className="flex flex-col items-start gap-1 text-base leading-6 text-ink">
        <p>{label}</p>
        <a href={href} className="self-stretch hover:underline">{name}</a>
        {title && <p>{title}</p>}
      </div>
    </div>
  )
}
