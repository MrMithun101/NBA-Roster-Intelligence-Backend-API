import type { Team } from '../../api/endpoints'

interface TeamDetailHeaderProps {
  team: Team
}

export function TeamDetailHeader({ team }: TeamDetailHeaderProps) {
  return (
    <div className="mb-8">
      <div className="inline-block px-4 py-1.5 rounded-full bg-[var(--color-nba-orange)]/15 text-[var(--color-nba-orange)] font-semibold text-sm mb-3">
        {team.abbreviation}
      </div>
      <h1 className="text-3xl font-bold text-slate-900">{team.name}</h1>
    </div>
  )
}
