import type { Mode, PersonalitySummary, SeatSelection, SessionStatusPayload } from './domain'

const DEFAULT_PERSONALITY_IDS_BY_MODE: Record<Mode, string[]> = {
  sats: ['ach-analyst', 'red-team', 'devils-advocate'],
  council: ['kent', 'heuer', 'feynman'],
}

export function personalitiesForMode(
  personalities: PersonalitySummary[],
  mode: Mode,
): PersonalitySummary[] {
  const allowedFamilies = mode === 'sats' ? new Set(['A']) : new Set(['B', 'C'])
  return personalities.filter((personality) => allowedFamilies.has(personality.family))
}

export function nextSeatForPersonality(
  seats: SeatSelection[],
  personality: PersonalitySummary,
  mode: Mode,
): SeatSelection[] {
  if (seatAdditionError(seats, personality, mode)) {
    return seats
  }
  const nextSeat = {
    personality_id: personality.id,
    model: personality.recommended_model,
  }
  return [...seats, nextSeat]
}

export function seatAdditionError(
  seats: SeatSelection[],
  personality: PersonalitySummary,
  mode: Mode,
): string | null {
  if (
    seats.some(
      (seat) => seat.personality_id === personality.id && seat.model === personality.recommended_model,
    )
  ) {
    return `Seat duplicado: ${personality.id} ya esta con ${personality.recommended_model}.`
  }
  if (mode === 'council' && seats.some((seat) => seat.model === personality.recommended_model)) {
    return `Council exige modelos unicos: ${personality.recommended_model} ya esta asignado.`
  }
  return null
}

export function removeSeat(seats: SeatSelection[], personalityId: string): SeatSelection[] {
  return seats.filter((seat) => seat.personality_id !== personalityId)
}

export function seatsCompatibleWithMode(
  seats: SeatSelection[],
  personalities: PersonalitySummary[],
  mode: Mode,
): SeatSelection[] {
  const allowedIds = new Set(
    personalitiesForMode(personalities, mode).map((personality) => personality.id),
  )
  return seats.filter((seat) => allowedIds.has(seat.personality_id))
}

export function defaultSeatsForMode(
  personalities: PersonalitySummary[],
  mode: Mode,
): SeatSelection[] {
  const byId = new Map(personalities.map((personality) => [personality.id, personality]))
  return DEFAULT_PERSONALITY_IDS_BY_MODE[mode]
    .map((personalityId) => byId.get(personalityId))
    .filter((personality): personality is PersonalitySummary => Boolean(personality))
    .reduce<SeatSelection[]>(
      (seats, personality) => nextSeatForPersonality(seats, personality, mode),
      [],
    )
}

export function isTerminalStatus(status: SessionStatusPayload | null): boolean {
  return (
    status?.status === 'completed' ||
    status?.status === 'cancelled_by_user' ||
    status?.status === 'aborted_insufficient_seats'
  )
}

export function statusTone(state: string): 'neutral' | 'accent' | 'success' | 'danger' {
  if (state === 'running') return 'accent'
  if (state === 'completed') return 'success'
  if (state === 'failed' || state === 'cancelled_by_user' || state.startsWith('aborted')) {
    return 'danger'
  }
  return 'neutral'
}

export function queryPreview(query: string, maxWords = 8): string {
  const words = query.trim().split(/\s+/).filter(Boolean)
  if (words.length === 0) return 'sin consulta'
  const preview = words.slice(0, maxWords).join(' ')
  return words.length > maxWords ? `${preview}...` : preview
}

export function sessionDateLabel(isoDate: string): string {
  return isoDate.replace('T', ' ').slice(0, 16)
}

export function markdownFilename(sessionId: string): string {
  return `council-of-intel-${sessionId.slice(0, 8)}.md`
}
