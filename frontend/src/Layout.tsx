import { Outlet, Link } from 'react-router-dom'

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-4xl px-4 py-3">
          <div className="flex gap-6">
            <Link
              to="/teams"
              className="text-slate-600 hover:text-slate-900 font-medium"
            >
              Teams
            </Link>
            <Link
              to="/players"
              className="text-slate-600 hover:text-slate-900 font-medium"
            >
              Players
            </Link>
          </div>
        </div>
      </nav>
      <main className="mx-auto max-w-4xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
