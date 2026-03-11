import { apiClient } from './client'

export interface Team {
  id: number
  name: string
  abbreviation: string
}

export interface Player {
  id: number
  first_name: string
  last_name: string
  position: string
}

interface TeamsResponse {
  data: Team[]
}

interface TeamResponse {
  data: Team
}

interface RosterResponse {
  data: Player[]
  season: number
  team_id: number
}

interface PlayersResponse {
  data: Player[]
  total: number
  limit: number
  offset: number
}

export async function getTeams(): Promise<Team[]> {
  const res = await apiClient.get<TeamsResponse>('/teams')
  return res.data?.data ?? []
}

export async function getTeam(teamId: number): Promise<Team> {
  const res = await apiClient.get<TeamResponse>(`/teams/${teamId}`)
  if (!res.data?.data) {
    throw new Error('Team not found.')
  }
  return res.data.data
}

export async function getRoster(
  teamId: number,
  season: number
): Promise<Player[]> {
  const res = await apiClient.get<RosterResponse>(
    `/teams/${teamId}/roster`,
    { params: { season } }
  )
  return res.data?.data ?? []
}

export interface GetPlayersParams {
  team_id?: number
  position?: string
  name?: string
  limit?: number
  offset?: number
}

export async function getPlayers(
  params: GetPlayersParams = {}
): Promise<{ data: Player[]; total: number }> {
  const res = await apiClient.get<PlayersResponse>('/players', { params })
  return {
    data: res.data?.data ?? [],
    total: res.data?.total ?? 0,
  }
}
