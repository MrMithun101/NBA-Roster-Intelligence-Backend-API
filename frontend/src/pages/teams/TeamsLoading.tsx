export function TeamsLoading() {
  return (
    <div className="flex items-center gap-3 py-12">
      <div className="h-2 w-2 rounded-full bg-[var(--color-nba-orange)] animate-pulse" />
      <div className="h-2 w-2 rounded-full bg-[var(--color-nba-orange)] animate-pulse" style={{ animationDelay: '150ms' }} />
      <div className="h-2 w-2 rounded-full bg-[var(--color-nba-orange)] animate-pulse" style={{ animationDelay: '300ms' }} />
      <span className="text-slate-500 ml-2">Loading teams...</span>
    </div>
  )
}
