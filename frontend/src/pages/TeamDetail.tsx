import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

const API_BASE = '/api'

interface Team {
  id: number
  name: string
  abbreviation: string
}

interface Player {
  id: number
  first_name: string
  last_name: string
  position: string
}

interface RosterResponse {
  data: Player[]
  season: number
  team_id: number
}

export function TeamDetail() {
  const { teamId } = useParams()
  const [team, setTeam] = useState<Team | null>(null)
  const [roster, setRoster] = useState<Player[]>([])
  const [season, setSeason] = useState(2025)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!teamId) return
    Promise.all([
      fetch(`${API_BASE}/teams/${teamId}`).then((r) => r.json()),
      fetch(`${API_BASE}/teams/${teamId}/roster?season=${season}`).then((r) =>
        r.json()
      ),
    ])
      .then(([teamRes, rosterRes]) => {
        setTeam(teamRes.data ?? null)
        setRoster((rosterRes as RosterResponse).data ?? [])
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [teamId, season])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error) return <p className="text-red-600">{error}</p>
  if (!team) return <p className="text-slate-500">Team not found.</p>

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-900 mb-2">
        {team.name}
      </h1>
      <p className="text-slate-600 mb-6">{team.abbreviation}</p>
      <div className="mb-6">
        <label className="text-sm text-slate-600 mr-2">Season:</label>
        <select
          value={season}
          onChange={(e) => setSeason(Number(e.target.value))}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm"
        >
          <option value={2025}>2024-25</option>
          <option value={2024}>2023-24</option>
        </select>
      </div>
      <h2 className="text-lg font-medium text-slate-800 mb-3">Roster</h2>
      <ul className="space-y-2">
        {roster.map((p) => (
          <li
            key={p.id}
            className="px-4 py-3 rounded-lg border border-slate-200 bg-white"
          >
            {p.first_name} {p.last_name}
            <span className="ml-2 text-slate-500 text-sm">{p.position}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
