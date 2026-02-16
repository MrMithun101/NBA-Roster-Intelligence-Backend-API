interface PlayersErrorProps {
  message: string
}

export function PlayersError({ message }: PlayersErrorProps) {
  return <p className="text-red-600">{message}</p>
}
