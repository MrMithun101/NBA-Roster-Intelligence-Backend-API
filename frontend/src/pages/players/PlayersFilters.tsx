import type { Team } from '../../api/endpoints'

const POSITIONS = ['', 'PG', 'SG', 'SF', 'PF', 'C']

interface PlayersFiltersProps {
  name: string
  onNameChange: (v: string) => void
  position: string
  onPositionChange: (v: string) => void
  teamId: string
  onTeamChange: (v: string) => void
  teams: Team[]
}

const inputClass =
  'rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm shadow-sm focus:border-[var(--color-nba-orange)] focus:ring-1 focus:ring-[var(--color-nba-orange)] outline-none transition-colors'

export function PlayersFilters({
  name,
  onNameChange,
  position,
  onPositionChange,
  teamId,
  onTeamChange,
  teams,
}: PlayersFiltersProps) {
  return (
    <div className="mb-6 p-5 rounded-xl bg-white border border-slate-200 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Filters</h3>
      <div className="flex flex-wrap gap-4 items-end">
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => onNameChange(e.target.value)}
            placeholder="Search by name..."
            className={`${inputClass} w-48`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">Position</label>
          <select
            value={position}
            onChange={(e) => onPositionChange(e.target.value)}
            className={inputClass}
          >
            <option value="">All</option>
            {POSITIONS.filter(Boolean).map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">Team</label>
          <select
            value={teamId}
            onChange={(e) => onTeamChange(e.target.value)}
            className={`${inputClass} min-w-[200px]`}
          >
            <option value="">All teams</option>
            {teams.map((t) => (
              <option key={t.id} value={String(t.id)}>
                {t.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  )
}
