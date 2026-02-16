import { useEffect, useState, useCallback } from 'react'
import { getTeams, getPlayers } from '../api/endpoints'
import type { Team, Player } from '../api/endpoints'
import { PlayersFilters } from './players/PlayersFilters'
import { PlayersTable } from './players/PlayersTable'
import { PlayersPagination } from './players/PlayersPagination'
import { PlayersLoading } from './players/PlayersLoading'
import { PlayersError } from './players/PlayersError'

const LIMIT = 20
const NAME_DEBOUNCE_MS = 300

export function Players() {
  const [teams, setTeams] = useState<Team[]>([])
  const [players, setPlayers] = useState<Player[]>([])
  const [total, setTotal] = useState(0)
  const [name, setName] = useState('')
  const [nameDebounced, setNameDebounced] = useState('')
  const [position, setPosition] = useState('')
  const [teamId, setTeamId] = useState('')
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Debounce name input
  useEffect(() => {
    const t = setTimeout(() => setNameDebounced(name), NAME_DEBOUNCE_MS)
    return () => clearTimeout(t)
  }, [name])

  // Load teams once (for dropdown)
  useEffect(() => {
    getTeams().then(setTeams).catch(() => setTeams([]))
  }, [])

  // Fetch players when filters or pagination change
  useEffect(() => {
    setLoading(true)
    setError(null)
    getPlayers({
      name: nameDebounced || undefined,
      position: position || undefined,
      team_id: teamId ? Number(teamId) : undefined,
      limit: LIMIT,
      offset,
    })
      .then(({ data, total: t }) => {
        setPlayers(data)
        setTotal(t)
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [nameDebounced, position, teamId, offset])

  const goPrev = useCallback(() => {
    setOffset((o) => Math.max(0, o - LIMIT))
  }, [])

  const goNext = useCallback(() => {
    setOffset((o) => o + LIMIT)
  }, [])

  useEffect(() => {
    setOffset(0)
  }, [nameDebounced, position, teamId])

  if (error && players.length === 0) return <PlayersError message={error} />

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-900 mb-6">Players</h1>
      <PlayersFilters
        name={name}
        onNameChange={setName}
        position={position}
        onPositionChange={setPosition}
        teamId={teamId}
        onTeamChange={setTeamId}
        teams={teams}
      />
      {loading && players.length === 0 ? (
        <PlayersLoading />
      ) : (
        <>
          <PlayersTable players={players} />
          <PlayersPagination
            offset={offset}
            limit={LIMIT}
            total={total}
            onPrev={goPrev}
            onNext={goNext}
          />
          {error && players.length > 0 && (
            <p className="mt-2 text-amber-600 text-sm">{error}</p>
          )}
        </>
      )}
    </div>
  )
}
