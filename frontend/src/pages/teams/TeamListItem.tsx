import { Link } from 'react-router-dom'
import type { Team } from '../../api/endpoints'

interface TeamListItemProps {
  team: Team
}

export function TeamListItem({ team }: TeamListItemProps) {
  return (
    <li>
      <Link
        to={`/teams/${team.id}`}
        className="group block px-5 py-4 rounded-xl bg-white border border-slate-200 shadow-sm hover:shadow-md hover:border-[var(--color-nba-orange)]/30 transition-all duration-200"
      >
        <span className="font-semibold text-slate-900 group-hover:text-[var(--color-nba-orange)] transition-colors">
          {team.name}
        </span>
        <span className="ml-2 text-slate-500 text-sm font-medium">
          {team.abbreviation}
        </span>
      </Link>
    </li>
  )
}
