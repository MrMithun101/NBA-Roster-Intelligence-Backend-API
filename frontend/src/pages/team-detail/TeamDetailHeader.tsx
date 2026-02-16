import type { Team } from '../../api/endpoints'

interface TeamDetailHeaderProps {
  team: Team
}

export function TeamDetailHeader({ team }: TeamDetailHeaderProps) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-semibold text-slate-900">{team.name}</h1>
      <p className="text-slate-600">{team.abbreviation}</p>
    </div>
  )
}
