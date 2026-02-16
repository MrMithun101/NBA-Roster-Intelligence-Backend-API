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
        className="block px-4 py-3 rounded-lg border border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50 text-slate-900"
      >
        <span className="font-medium">{team.name}</span>
        <span className="text-slate-500 ml-2">({team.abbreviation})</span>
      </Link>
    </li>
  )
}
