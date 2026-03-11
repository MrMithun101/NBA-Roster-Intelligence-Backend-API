interface PlayersPaginationProps {
  offset: number
  limit: number
  total: number
  onPrev: () => void
  onNext: () => void
}

export function PlayersPagination({
  offset,
  limit,
  total,
  onPrev,
  onNext,
}: PlayersPaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / limit))
  const currentPage = Math.floor(offset / limit) + 1

  if (totalPages <= 1 && total <= limit) return null

  const btnClass = (disabled: boolean) =>
    `px-4 py-2.5 rounded-lg font-medium transition-colors ${
      disabled
        ? 'opacity-50 cursor-not-allowed border-slate-200 text-slate-400'
        : 'border-slate-300 text-slate-700 hover:bg-[var(--color-nba-orange)] hover:text-white hover:border-[var(--color-nba-orange)]'
    }`

  return (
    <div className="mt-6 flex gap-4 items-center">
      <button
        onClick={onPrev}
        disabled={offset === 0}
        className={`${btnClass(offset === 0)} border`}
      >
        Previous
      </button>
      <span className="text-slate-600 text-sm font-medium">
        Page {currentPage} of {totalPages}
      </span>
      <button
        onClick={onNext}
        disabled={offset + limit >= total}
        className={`${btnClass(offset + limit >= total)} border`}
      >
        Next
      </button>
    </div>
  )
}
