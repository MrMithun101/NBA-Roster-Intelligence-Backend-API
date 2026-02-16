import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getTeams } from '../api/endpoints'
import type { Team } from '../api/endpoints'

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

  if (loading) return <p className="text-slate-500">Loading teams...</p>
  if (error) return <p className="text-red-600">{error}</p>

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-900 mb-6">Teams</h1>
      <ul className="space-y-2">
        {teams.map((team) => (
          <li key={team.id}>
            <Link
              to={`/teams/${team.id}`}
              className="block px-4 py-3 rounded-lg border border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50 text-slate-900"
            >
              <span className="font-medium">{team.name}</span>
              <span className="text-slate-500 ml-2">({team.abbreviation})</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
