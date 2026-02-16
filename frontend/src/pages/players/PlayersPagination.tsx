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

  return (
    <div className="mt-6 flex gap-2 items-center">
      <button
        onClick={onPrev}
        disabled={offset === 0}
        className="px-4 py-2 rounded border border-slate-300 text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
      >
        Previous
      </button>
      <span className="text-slate-600 text-sm">
        Page {currentPage} of {totalPages}
      </span>
      <button
        onClick={onNext}
        disabled={offset + limit >= total}
        className="px-4 py-2 rounded border border-slate-300 text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
      >
        Next
      </button>
    </div>
  )
}
