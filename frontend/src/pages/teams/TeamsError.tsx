interface TeamsErrorProps {
  message: string
}

export function TeamsError({ message }: TeamsErrorProps) {
  return <p className="text-red-600">{message}</p>
}
