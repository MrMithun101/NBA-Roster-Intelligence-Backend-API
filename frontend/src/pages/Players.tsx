import { useEffect, useState } from 'react'
import { getPlayers } from '../api/endpoints'
import type { Player } from '../api/endpoints'

const DEFAULT_LIMIT = 20

export function Players() {
  const [players, setPlayers] = useState<Player[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [offset, setOffset] = useState(0)

  useEffect(() => {
    getPlayers({ limit: DEFAULT_LIMIT, offset })
      .then(({ data, total: t }) => {
        setPlayers(data)
        setTotal(t)
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [offset])

  if (loading && players.length === 0)
    return <p className="text-slate-500">Loading players...</p>
  if (error) return <p className="text-red-600">{error}</p>

  const totalPages = Math.ceil(total / DEFAULT_LIMIT)
  const currentPage = Math.floor(offset / DEFAULT_LIMIT) + 1

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-900 mb-6">Players</h1>
      <ul className="space-y-2">
        {players.map((p) => (
          <li
            key={p.id}
            className="px-4 py-3 rounded-lg border border-slate-200 bg-white"
          >
            {p.first_name} {p.last_name}
            <span className="ml-2 text-slate-500 text-sm">{p.position}</span>
          </li>
        ))}
      </ul>
      {totalPages > 1 && (
        <div className="mt-6 flex gap-2 items-center">
          <button
            onClick={() => setOffset(Math.max(0, offset - DEFAULT_LIMIT))}
            disabled={offset === 0}
            className="px-4 py-2 rounded border border-slate-300 text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
          >
            Previous
          </button>
          <span className="text-slate-600 text-sm">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setOffset(offset + DEFAULT_LIMIT)}
            disabled={offset + DEFAULT_LIMIT >= total}
            className="px-4 py-2 rounded border border-slate-300 text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}
