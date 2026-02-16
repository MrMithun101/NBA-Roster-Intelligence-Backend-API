import type { Player } from '../../api/endpoints'

interface PlayersTableProps {
  players: Player[]
}

export function PlayersTable({ players }: PlayersTableProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white overflow-hidden shadow-sm">
      <table className="min-w-full">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200">
            <th className="px-5 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
              Player
            </th>
            <th className="px-5 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
              Position
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {players.map((p) => (
            <tr key={p.id} className="hover:bg-slate-50/80 transition-colors">
              <td className="px-5 py-4 text-sm font-medium text-slate-900">
                {p.first_name} {p.last_name}
              </td>
              <td className="px-5 py-4">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 text-xs font-medium">
                  {p.position}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
