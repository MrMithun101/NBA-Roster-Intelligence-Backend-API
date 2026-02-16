import axios, { AxiosError } from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10_000,
})

/** Turn axios errors into readable messages. */
function toReadableError(err: unknown): string {
  if (err instanceof AxiosError) {
    if (err.code === 'ERR_NETWORK') {
      return 'Network error. Is the API server running?'
    }
    if (err.response?.status === 404) {
      return 'Not found.'
    }
    if (err.response?.status && err.response.status >= 500) {
      return 'Server error. Please try again later.'
    }
    return err.response?.data?.detail ?? err.message
  }
  return err instanceof Error ? err.message : 'An unexpected error occurred.'
}

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    throw new Error(toReadableError(err))
  }
)
