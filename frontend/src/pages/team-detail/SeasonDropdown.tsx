const SEASONS = [2025, 2024] as const

interface SeasonDropdownProps {
  value: number
  onChange: (season: number) => void
}

export function SeasonDropdown({ value, onChange }: SeasonDropdownProps) {
  return (
    <div className="mb-6">
      <label className="text-sm text-slate-600 mr-2">Season:</label>
      <select
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="rounded border border-slate-300 px-3 py-1.5 text-sm"
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
