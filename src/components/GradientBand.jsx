import FeatureCards from './lower/FeatureCards.jsx'
import ComparisonTable from './lower/ComparisonTable.jsx'

// §9 GradientBand wrapper
export default function GradientBand({ showFeatureCards = true }) {
  return (
    <div className="flex flex-col items-center gap-12 self-stretch bg-features-gradient px-4 py-11 lg:px-8">
      {showFeatureCards && <FeatureCards />}
      <ComparisonTable />
    </div>
  )
}
