const SEASONS = [2025, 2024] as const

interface SeasonDropdownProps {
  value: number
  onChange: (season: number) => void
}

export function SeasonDropdown({ value, onChange }: SeasonDropdownProps) {
  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-slate-600 mb-2">Season</label>
      <select
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-900 shadow-sm focus:border-[var(--color-nba-orange)] focus:ring-1 focus:ring-[var(--color-nba-orange)] outline-none"
      >
        {SEASONS.map((yr) => (
          <option key={yr} value={yr}>
            {yr === 2025 ? '2024-25' : '2023-24'}
          </option>
        ))}
      </select>
    </div>
  )
}
