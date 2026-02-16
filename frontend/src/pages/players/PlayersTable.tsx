import type { Player } from '../../api/endpoints'

interface PlayersTableProps {
  players: Player[]
}

export function PlayersTable({ players }: PlayersTableProps) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white overflow-hidden">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left text-sm font-medium text-slate-700">
              Player
            </th>
            <th className="px-4 py-3 text-left text-sm font-medium text-slate-700">
              Position
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {players.map((p) => (
            <tr key={p.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 text-sm text-slate-900">
                {p.first_name} {p.last_name}
              </td>
              <td className="px-4 py-3 text-sm text-slate-600">{p.position}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
