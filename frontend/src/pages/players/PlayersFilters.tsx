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
    <div className="mb-6 flex flex-wrap gap-4 items-end">
      <div>
        <label className="block text-sm text-slate-600 mb-1">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => onNameChange(e.target.value)}
          placeholder="Search by name..."
          className="rounded border border-slate-300 px-3 py-1.5 text-sm w-48"
        />
      </div>
      <div>
        <label className="block text-sm text-slate-600 mb-1">Position</label>
        <select
          value={position}
          onChange={(e) => onPositionChange(e.target.value)}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm"
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
        <label className="block text-sm text-slate-600 mb-1">Team</label>
        <select
          value={teamId}
          onChange={(e) => onTeamChange(e.target.value)}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm min-w-[180px]"
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
  )
}
