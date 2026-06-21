export type Mode = 'sats' | 'council'
export type SeatState = 'pending' | 'running' | 'completed' | 'failed'
export type SessionStatus =
  | 'pending'
  | 'running'
  | 'completed'
  | 'cancelled_by_user'
  | 'aborted_insufficient_seats'

export interface PersonalitySummary {
  id: string
  name: string
  family: 'A' | 'B' | 'C' | 'D'
  polarity: string
  recommended_model: string
  sat_layer: string
  can_be_chairman: boolean
  description: string
}

export interface SeatSelection {
  personality_id: string
  model: string
}

export interface SessionCreatePayload {
  query: string
  mode: Mode
  chairman_personality: string
  seats: SeatSelection[]
}

export interface SeatProgress {
  seat_idx: number
  personality: string
  state: SeatState
  error?: string
}

export interface SessionStatusPayload {
  session_id: string
  status: SessionStatus
  current_round: number | null
  rounds_completed: number[]
  seats_progress: SeatProgress[]
  cost_so_far_eur: number
  elapsed_seconds: number
  last_event_ts: string
}

export interface SessionSummary {
  session_id: string
  query: string
  mode: Mode
  status: SessionStatus
  created_at: string
  updated_at: string
  cost_eur: number
  current_round: number | null
}

export interface AppConfig {
  allowed_models: string[]
  defaults: {
    mode: Mode
    chairman_personality: string
  }
}

export interface AppState {
  query: string
  mode: Mode
  seats: SeatSelection[]
  chairmanPersonality: string
  activeSessionId: string | null
  status: SessionStatusPayload | null
  finalMarkdown: string
  logs: unknown[]
  sessions: SessionSummary[]
}
