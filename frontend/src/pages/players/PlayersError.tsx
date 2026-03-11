interface PlayersErrorProps {
  message: string
}

export function PlayersError({ message }: PlayersErrorProps) {
  return (
    <div className="rounded-xl bg-red-50 border border-red-200 px-5 py-4">
      <p className="text-red-800 font-medium">{message}</p>
      <p className="text-red-600 text-sm mt-1">Please check your connection and try again.</p>
    </div>
  )
}
