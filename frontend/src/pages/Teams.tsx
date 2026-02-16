import { useEffect, useState } from 'react'
import { getTeams } from '../api/endpoints'
import type { Team } from '../api/endpoints'
import { TeamsLoading } from './teams/TeamsLoading'
import { TeamsError } from './teams/TeamsError'
import { TeamsList } from './teams/TeamsList'

export function Teams() {
  const [teams, setTeams] = useState<Team[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getTeams()
      .then(setTeams)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <TeamsLoading />
  if (error) return <TeamsError message={error} />

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Teams</h1>
      <p className="text-slate-600 mb-8">Browse NBA teams and their rosters</p>
      <TeamsList teams={teams} />
    </div>
  )
}
