interface TeamDetailErrorProps {
  message: string
}

export function TeamDetailError({ message }: TeamDetailErrorProps) {
  return <p className="text-red-600">{message}</p>
}
