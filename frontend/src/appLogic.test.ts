import { describe, expect, it } from 'vitest'

import {
  defaultSeatsForMode,
  isTerminalStatus,
  markdownFilename,
  nextSeatForPersonality,
  personalitiesForMode,
  queryPreview,
  removeSeat,
  seatAdditionError,
  seatsCompatibleWithMode,
  sessionDateLabel,
  statusTone,
} from './appLogic'
import type { PersonalitySummary, SessionStatusPayload } from './domain'

const personalities: PersonalitySummary[] = [
  {
    id: 'ach-analyst',
    name: 'ACH Analyst',
    family: 'A',
    polarity: 'structured',
    recommended_model: 'openai/gpt-5.5',
    sat_layer: 'ach',
    can_be_chairman: false,
    description: 'SAT',
  },
  {
    id: 'red-team',
    name: 'Red Team',
    family: 'A',
    polarity: 'adversarial',
    recommended_model: 'x-ai/grok-4.3',
    sat_layer: 'red_team',
    can_be_chairman: false,
    description: 'SAT',
  },
  {
    id: 'devils-advocate',
    name: "Devil's Advocate",
    family: 'A',
    polarity: 'adversarial',
    recommended_model: 'openai/gpt-chat-latest',
    sat_layer: 'devils',
    can_be_chairman: false,
    description: 'SAT',
  },
  {
    id: 'kent',
    name: 'Kent',
    family: 'B',
    polarity: 'doctrinal',
    recommended_model: 'anthropic/claude-opus-4.7',
    sat_layer: 'none',
    can_be_chairman: false,
    description: 'Council',
  },
  {
    id: 'heuer',
    name: 'Heuer',
    family: 'B',
    polarity: 'doctrinal',
    recommended_model: 'anthropic/claude-sonnet-4.6',
    sat_layer: 'none',
    can_be_chairman: false,
    description: 'Council',
  },
  {
    id: 'feynman',
    name: 'Feynman',
    family: 'C',
    polarity: 'first-principles',
    recommended_model: 'google/gemini-3.1-pro-preview',
    sat_layer: 'none',
    can_be_chairman: false,
    description: 'Council',
  },
]

describe('app logic', () => {
  it('filters personalities by mode family', () => {
    expect(personalitiesForMode(personalities, 'sats').map((item) => item.id)).toEqual([
      'ach-analyst',
      'red-team',
      'devils-advocate',
    ])
    expect(personalitiesForMode(personalities, 'council').map((item) => item.id)).toEqual([
      'kent',
      'heuer',
      'feynman',
    ])
  })

  it('adds and removes seats with recommended model', () => {
    const seats = nextSeatForPersonality([], personalities[0], 'sats')
    expect(seats).toEqual([{ personality_id: 'ach-analyst', model: 'openai/gpt-5.5' }])
    expect(removeSeat(seats, 'ach-analyst')).toEqual([])
  })

  it('blocks exact duplicate seats before the backend rejects them', () => {
    const seats = [{ personality_id: 'ach-analyst', model: 'openai/gpt-5.5' }]

    expect(seatAdditionError(seats, personalities[0], 'sats')).toContain('Seat duplicado')
    expect(nextSeatForPersonality(seats, personalities[0], 'sats')).toBe(seats)
  })

  it('blocks duplicate models in council mode', () => {
    const seats = [{ personality_id: 'heuer', model: 'anthropic/claude-sonnet-4.6' }]
    const socratesLikePersonality = {
      ...personalities[5],
      id: 'socrates',
      recommended_model: 'anthropic/claude-sonnet-4.6',
    }

    expect(seatAdditionError(seats, socratesLikePersonality, 'council')).toContain(
      'modelos unicos',
    )
    expect(nextSeatForPersonality(seats, socratesLikePersonality, 'council')).toBe(seats)
  })

  it('keeps only seats compatible with the selected mode', () => {
    const seats = [
      { personality_id: 'ach-analyst', model: 'openai/gpt-5.5' },
      { personality_id: 'kent', model: 'anthropic/claude-sonnet-4.6' },
      { personality_id: 'unknown', model: 'openai/gpt-5.5' },
    ]

    expect(seatsCompatibleWithMode(seats, personalities, 'sats')).toEqual([
      { personality_id: 'ach-analyst', model: 'openai/gpt-5.5' },
    ])
    expect(seatsCompatibleWithMode(seats, personalities, 'council')).toEqual([
      { personality_id: 'kent', model: 'anthropic/claude-sonnet-4.6' },
    ])
    expect(seatsCompatibleWithMode([], personalities, 'council')).toEqual([])
  })

  it('provides defaults per mode', () => {
    expect(defaultSeatsForMode(personalities, 'sats')).toEqual([
      { personality_id: 'ach-analyst', model: 'openai/gpt-5.5' },
      { personality_id: 'red-team', model: 'x-ai/grok-4.3' },
      { personality_id: 'devils-advocate', model: 'openai/gpt-chat-latest' },
    ])
    expect(
      defaultSeatsForMode(personalities, 'council').map((seat) => seat.personality_id),
    ).toEqual(['kent', 'heuer', 'feynman'])
  })

  it('detects terminal status and visual tone', () => {
    const status = { status: 'completed' } as SessionStatusPayload
    expect(isTerminalStatus(status)).toBe(true)
    expect(statusTone('running')).toBe('accent')
    expect(statusTone('failed')).toBe('danger')
  })

  it('formats compact session rows and markdown filenames', () => {
    expect(queryPreview('uno dos tres cuatro cinco seis siete ocho nueve')).toBe(
      'uno dos tres cuatro cinco seis siete ocho...',
    )
    expect(queryPreview('')).toBe('sin consulta')
    expect(sessionDateLabel('2026-05-09T19:51:33.000Z')).toBe('2026-05-09 19:51')
    expect(markdownFilename('abcdef123456')).toBe('council-of-intel-abcdef12.md')
  })
})
