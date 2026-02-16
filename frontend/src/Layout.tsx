import { Outlet, Link, useLocation } from 'react-router-dom'

export function Layout() {
  const location = useLocation()

  const navLink = (to: string, label: string) => {
    const isActive = location.pathname === to || location.pathname.startsWith(to + '/')
    return (
      <Link
        to={to}
        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
          isActive
            ? 'bg-[var(--color-nba-orange)] text-white'
            : 'text-slate-300 hover:text-white hover:bg-white/10'
        }`}
      >
        {label}
      </Link>
    )
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <nav className="bg-[var(--color-nba-navy)] shadow-lg">
        <div className="mx-auto max-w-5xl px-4 py-4">
          <div className="flex items-center gap-8">
            <Link to="/teams" className="text-white font-bold text-xl tracking-tight">
              NBA Roster
            </Link>
            <div className="flex gap-2">
              {navLink('/teams', 'Teams')}
              {navLink('/players', 'Players')}
            </div>
          </div>
        </div>
      </nav>
      <main className="mx-auto max-w-5xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
