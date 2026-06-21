import type {
  AppConfig,
  PersonalitySummary,
  SessionCreatePayload,
  SessionStatusPayload,
  SessionSummary,
} from './domain'

const API_PREFIX = '/api'

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_PREFIX}${path}`, {
    headers: { 'Content-Type': 'application/json', ...init?.headers },
    ...init,
  })
  if (!response.ok) {
    const body = await response.text()
    throw new Error(body || `HTTP ${response.status}`)
  }
  return (await response.json()) as T
}

export async function fetchConfig(): Promise<AppConfig> {
  return requestJson<AppConfig>('/config')
}

export async function fetchPersonalities(): Promise<PersonalitySummary[]> {
  const payload = await requestJson<{ personalities: PersonalitySummary[] }>('/personalities')
  return payload.personalities
}

export async function fetchSessions(): Promise<SessionSummary[]> {
  const payload = await requestJson<{ sessions: SessionSummary[] }>('/sessions')
  return payload.sessions
}

export async function createSession(payload: SessionCreatePayload): Promise<string> {
  const response = await requestJson<{ session_id: string }>('/sessions', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  return response.session_id
}

export async function fetchStatus(sessionId: string): Promise<SessionStatusPayload> {
  return requestJson<SessionStatusPayload>(`/sessions/${sessionId}/status`)
}

export async function cancelSession(sessionId: string): Promise<void> {
  await requestJson(`/sessions/${sessionId}/cancel`, { method: 'POST' })
}

export async function exportMarkdown(sessionId: string): Promise<string> {
  const response = await fetch(`${API_PREFIX}/sessions/${sessionId}/export-md`)
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.text()
}

export async function fetchLogs(sessionId: string): Promise<unknown[]> {
  const payload = await requestJson<{ logs: unknown[] }>(`/sessions/${sessionId}/logs`)
  return payload.logs
}
