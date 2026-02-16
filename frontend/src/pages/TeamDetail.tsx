import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getTeam, getRoster } from '../api/endpoints'
import type { Team, Player } from '../api/endpoints'
import { TeamDetailHeader } from './team-detail/TeamDetailHeader'
import { SeasonDropdown } from './team-detail/SeasonDropdown'
import { RosterTable } from './team-detail/RosterTable'
import { TeamDetailLoading } from './team-detail/TeamDetailLoading'
import { TeamDetailError } from './team-detail/TeamDetailError'

export function TeamDetail() {
  const { teamId } = useParams<{ teamId: string }>()
  const [team, setTeam] = useState<Team | null>(null)
  const [roster, setRoster] = useState<Player[]>([])
  const [season, setSeason] = useState(2025)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!teamId) return
    setLoading(true)
    setError(null)
    const id = Number(teamId)
    Promise.all([getTeam(id), getRoster(id, season)])
      .then(([t, r]) => {
        setTeam(t)
        setRoster(r)
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [teamId, season])

  if (loading) return <TeamDetailLoading />
  if (error) return <TeamDetailError message={error} />
  if (!team) return <p className="text-slate-500">Team not found.</p>

  return (
    <div>
      <TeamDetailHeader team={team} />
      <SeasonDropdown value={season} onChange={setSeason} />
      <h2 className="text-lg font-medium text-slate-800 mb-3">Roster</h2>
      <RosterTable players={roster} />
    </div>
  )
}
