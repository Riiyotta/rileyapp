import { useRive, Layout, Fit, Alignment, RuntimeLoader } from '@rive-app/react-canvas'
import riveWasmUrl from '@rive-app/canvas/rive.wasm?url'

// Serve the Rive runtime locally instead of from the unpkg CDN default.
RuntimeLoader.setWasmUrl(riveWasmUrl)

// §5 / §14 M6b — autoplays the slide's state machine; fit Cover, align Center.
export default function RiveChat({ src, artboard, stateMachine }) {
  const { RiveComponent } = useRive({
    src,
    artboard,
    stateMachine,
    autoplay: true,
    layout: new Layout({ fit: Fit.Cover, alignment: Alignment.Center }),
  })
  return (
    <RiveComponent
      className="pointer-events-auto relative z-10 h-full w-full"
      role="img"
      aria-label="Interactive Rive animation"
    />
  )
}
