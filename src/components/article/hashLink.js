// The app router intercepts same-origin <a> clicks (pushState, no anchor scroll). In-page anchors (TOC entries,
// citation superscripts) call this to get the browser's native instant jump + hash update, as on the original.
export function onHashLinkClick(e) {
  const href = e.currentTarget.getAttribute('href')
  if (!href || !href.startsWith('#')) return
  e.preventDefault()
  window.location.hash = href.slice(1)
}
