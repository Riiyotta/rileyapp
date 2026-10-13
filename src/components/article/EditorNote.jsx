// Blog spec §3.6 editorNote. `bg-brand-100` is undefined on the live CSS, so the box is transparent.
export default function EditorNote({ paragraphs = [] }) {
  return (
    <div className="my-4 flex flex-col items-start gap-6 self-stretch rounded-[14px] p-8 lg:flex-row lg:p-12">
      <div className="flex shrink-0 items-start self-stretch">
        <img src="/assets/blog/icons/editor-mascot.svg" alt="" width="71" height="64" className="my-8" />
      </div>
      <div className="flex flex-1 flex-col items-start gap-4">
        <h3 className="ab-note-h3">Editor's Note</h3>
        <div>
          {paragraphs.map((t, i) => (
            <p key={i} className="ab-p">{t}</p>
          ))}
        </div>
      </div>
    </div>
  )
}
