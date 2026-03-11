import { TeamListItem } from './TeamListItem'
import type { Team } from '../../api/endpoints'

interface TeamsListProps {
  teams: Team[]
}

export function TeamsList({ teams }: TeamsListProps) {
  return (
    <ul className="grid gap-3 sm:grid-cols-2">
      {teams.map((team) => (
        <TeamListItem key={team.id} team={team} />
      ))}
    </ul>
  )
}
