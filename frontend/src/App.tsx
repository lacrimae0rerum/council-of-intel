import {
  CheckCircle2,
  Circle,
  FileText,
  Loader2,
  Play,
  ScrollText,
  SquareX,
  Trash2,
} from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { useDrag, useDrop } from 'react-dnd'

import {
  cancelSession,
  createSession,
  exportMarkdown,
  fetchConfig,
  fetchLogs,
  fetchPersonalities,
  fetchSessions,
  fetchStatus,
} from './api'
import {
  defaultSeatsForMode,
  isTerminalStatus,
  markdownFilename,
  nextSeatForPersonality,
  personalitiesForMode,
  queryPreview,
  removeSeat,
  seatAdditionError,
  sessionDateLabel,
  statusTone,
} from './appLogic'
import type {
  AppConfig,
  Mode,
  PersonalitySummary,
  SeatSelection,
  SessionStatusPayload,
  SessionSummary,
} from './domain'

const DRAG_TYPE = 'personality'
const EMPTY_SEATS_BY_MODE: Record<Mode, SeatSelection[]> = { sats: [], council: [] }
type ResultView = 'markdown' | 'logs'

export function App() {
  const [config, setConfig] = useState<AppConfig | null>(null)
  const [personalities, setPersonalities] = useState<PersonalitySummary[]>([])
  const [query, setQuery] = useState('Evalua esta intrusión CTI')
  const [mode, setMode] = useState<Mode>('sats')
  const [seatsByMode, setSeatsByMode] =
    useState<Record<Mode, SeatSelection[]>>(EMPTY_SEATS_BY_MODE)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [status, setStatus] = useState<SessionStatusPayload | null>(null)
  const [markdown, setMarkdown] = useState('')
  const [logs, setLogs] = useState<unknown[]>([])
  const [resultView, setResultView] = useState<ResultView>('markdown')
  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    let mounted = true
    async function loadBootstrap() {
      const failures: string[] = []

      const nextPersonalities = await fetchPersonalities().catch((unknownError: unknown) => {
        failures.push(`personalidades: ${String(unknownError)}`)
        return []
      })
      if (!mounted) return
      setPersonalities(nextPersonalities)
      if (nextPersonalities.length > 0) {
        setSeatsByMode({
          sats: defaultSeatsForMode(nextPersonalities, 'sats'),
          council: defaultSeatsForMode(nextPersonalities, 'council'),
        })
      }

      const nextConfig = await fetchConfig().catch((unknownError: unknown) => {
        failures.push(`config: ${String(unknownError)}`)
        return null
      })
      if (!mounted) return
      if (nextConfig) {
        setConfig(nextConfig)
        setMode(nextConfig.defaults.mode)
      }

      const nextSessions = await fetchSessions().catch((unknownError: unknown) => {
        failures.push(`sesiones: ${String(unknownError)}`)
        return []
      })
      if (!mounted) return
      setSessions(nextSessions)

      if (failures.length > 0) {
        setError(`Bootstrap parcial: ${failures.join(' | ')}`)
      }
    }
    void loadBootstrap()
    return () => {
      mounted = false
    }
  }, [])

  useEffect(() => {
    if (!sessionId || isTerminalStatus(status)) return
    const timer = window.setInterval(() => {
      void fetchStatus(sessionId)
        .then((nextStatus) => {
          setStatus(nextStatus)
          if (isTerminalStatus(nextStatus)) {
            void exportMarkdown(sessionId).then((nextMarkdown) => {
              setMarkdown(nextMarkdown)
              setResultView('markdown')
            })
            void fetchLogs(sessionId).then(setLogs)
            void fetchSessions().then(setSessions)
          }
        })
        .catch((unknownError) => setError(String(unknownError)))
    }, 1500)
    return () => window.clearInterval(timer)
  }, [sessionId, status])

  const availablePersonalities = useMemo(
    () => personalitiesForMode(personalities, mode),
    [mode, personalities],
  )
  const seats = seatsByMode[mode]

  const chairman = config?.defaults.chairman_personality ?? 'mclaughlin'

  const launch = useCallback(async () => {
    setBusy(true)
    setError('')
    setMarkdown('')
    setLogs([])
    try {
      const id = await createSession({
        query,
        mode,
        chairman_personality: chairman,
        seats,
      })
      setSessionId(id)
      setStatus(await fetchStatus(id))
    } catch (unknownError) {
      setError(String(unknownError))
    } finally {
      setBusy(false)
    }
  }, [chairman, mode, query, seats])

  const cancel = useCallback(async () => {
    if (!sessionId) return
    setBusy(true)
    try {
      await cancelSession(sessionId)
      setStatus(await fetchStatus(sessionId))
      setMarkdown(await exportMarkdown(sessionId))
      setLogs(await fetchLogs(sessionId))
      setResultView('markdown')
    } catch (unknownError) {
      setError(String(unknownError))
    } finally {
      setBusy(false)
    }
  }, [sessionId])

  const addSeat = useCallback(
    (personality: PersonalitySummary) => {
      const validationError = seatAdditionError(seatsByMode[mode], personality, mode)
      if (validationError) {
        setError(validationError)
        return
      }
      setError('')
      setSeatsByMode((current) => ({
        ...current,
        [mode]: nextSeatForPersonality(current[mode], personality, mode),
      }))
    },
    [mode, seatsByMode],
  )

  const onModeChange = useCallback((nextMode: Mode) => {
    setMode(nextMode)
  }, [])

  const downloadMarkdown = useCallback(async () => {
    if (!sessionId) return
    try {
      const nextMarkdown = await exportMarkdown(sessionId)
      setMarkdown(nextMarkdown)
      setResultView('markdown')
      triggerMarkdownDownload(nextMarkdown, markdownFilename(sessionId))
    } catch (unknownError) {
      setError(String(unknownError))
    }
  }, [sessionId])

  const openLogs = useCallback(async () => {
    if (!sessionId) return
    try {
      setLogs(await fetchLogs(sessionId))
      setResultView('logs')
    } catch (unknownError) {
      setError(String(unknownError))
    }
  }, [sessionId])

  return (
    <main className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <div className="mx-auto grid max-w-[1800px] grid-cols-1 gap-px p-3 lg:grid-cols-[340px_minmax(0,1fr)_420px]">
        <aside className="panel">
          <HeaderBlock title="council-of-intel" subtitle="one-shot intelligence council" />
          <ModeSwitch mode={mode} onChange={onModeChange} />
          <section className="mt-4">
            <h2 className="section-title">Personalidades</h2>
            <div className="personality-list">
              {availablePersonalities.map((personality) => (
                <PersonalityItem
                  key={`${mode}-${personality.id}`}
                  personality={personality}
                  onAdd={addSeat}
                />
              ))}
              {personalities.length === 0 && (
                <p className="empty-state">No llegaron personalidades desde /api/personalities.</p>
              )}
              {personalities.length > 0 && availablePersonalities.length === 0 && (
                <p className="empty-state">
                  Hay {personalities.length} personalidades, pero ninguna encaja con el modo {mode}.
                </p>
              )}
            </div>
          </section>
        </aside>

        <section className="panel">
          <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_360px]">
            <div>
              <label className="section-title" htmlFor="query">
                Pregunta de inteligencia
              </label>
              <textarea
                id="query"
                className="query-box"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
            <SeatDropZone
              key={mode}
              seats={seats}
              onDropPersonality={addSeat}
              onRemove={(personalityId) => {
                setSeatsByMode((current) => ({
                  ...current,
                  [mode]: removeSeat(current[mode], personalityId),
                }))
              }}
            />
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            <button className="command primary" disabled={busy || seats.length < 3} onClick={launch}>
              <Play size={16} />
              Lanzar sesión
            </button>
            <button className="command danger" disabled={!sessionId || busy} onClick={cancel}>
              <SquareX size={16} />
              Cancelar
            </button>
            <button
              className="command"
              disabled={!sessionId}
              onClick={() => void downloadMarkdown()}
            >
              <FileText size={16} />
              Exportar Markdown
            </button>
            <button
              className="command"
              disabled={!sessionId}
              onClick={() => void openLogs()}
            >
              <ScrollText size={16} />
              Logs
            </button>
          </div>

          {error && (
            <div className="mt-4 border border-[var(--danger)] p-3 text-sm text-[var(--danger)]">
              {error}
            </div>
          )}

          <StatusPanel status={status} />
          <ResultPanel view={resultView} markdown={markdown} logs={logs} />
        </section>

        <aside className="panel">
          <h2 className="section-title">Sesiones</h2>
          <div className="session-list">
            {sessions.map((session) => (
              <button
                className="session-row"
                key={session.session_id}
                onClick={() => {
                  setSessionId(session.session_id)
                  void fetchStatus(session.session_id).then(setStatus)
                  void exportMarkdown(session.session_id).then((nextMarkdown) => {
                    setMarkdown(nextMarkdown)
                    setResultView('markdown')
                  })
                  void fetchLogs(session.session_id).then(setLogs)
                }}
              >
                <span>{session.status}</span>
                <strong>{sessionDateLabel(session.created_at)}</strong>
                <small>{queryPreview(session.query)}</small>
              </button>
            ))}
          </div>
          <h2 className="section-title mt-5">Logs</h2>
          <pre className="logs">{logs.map((entry) => JSON.stringify(entry)).join('\n')}</pre>
        </aside>
      </div>
    </main>
  )
}

function triggerMarkdownDownload(markdown: string, filename: string) {
  const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.append(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

function HeaderBlock({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <header className="border-b border-[color:var(--line)] pb-4">
      <h1 className="text-xl font-semibold text-[var(--anthropic)]">{title}</h1>
      <p className="mt-1 text-xs uppercase tracking-[0.18em] text-[color:var(--muted)]">
        {subtitle}
      </p>
    </header>
  )
}

function ModeSwitch({ mode, onChange }: { mode: Mode; onChange: (mode: Mode) => void }) {
  return (
    <div className="mt-4 grid grid-cols-2 border border-[color:var(--line)]">
      {(['sats', 'council'] as const).map((item) => (
        <button
          className={item === mode ? 'segmented active' : 'segmented'}
          key={item}
          onClick={() => onChange(item)}
        >
          {item.toUpperCase()}
        </button>
      ))}
    </div>
  )
}

function PersonalityItem({
  personality,
  onAdd,
}: {
  personality: PersonalitySummary
  onAdd: (personality: PersonalitySummary) => void
}) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: DRAG_TYPE,
    item: personality,
    collect: (monitor) => ({ isDragging: monitor.isDragging() }),
  }), [personality])
  return (
    <button
      ref={(node) => {
        drag(node)
      }}
      className="personality-item"
      style={{ opacity: isDragging ? 0.45 : 1 }}
      onClick={() => onAdd(personality)}
    >
      <span>{personality.id}</span>
      <small>{personality.recommended_model}</small>
    </button>
  )
}

function SeatDropZone({
  seats,
  onDropPersonality,
  onRemove,
}: {
  seats: SeatSelection[]
  onDropPersonality: (personality: PersonalitySummary) => void
  onRemove: (personalityId: string) => void
}) {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: DRAG_TYPE,
    drop: (personality: PersonalitySummary) => onDropPersonality(personality),
    collect: (monitor) => ({ isOver: monitor.isOver() }),
  }), [onDropPersonality])
  return (
    <div
      ref={(node) => {
        drop(node)
      }}
      className={isOver ? 'seat-zone over' : 'seat-zone'}
    >
      <h2 className="section-title">Seats</h2>
      {seats.map((seat) => (
        <div className="seat-row" key={`${seat.personality_id}-${seat.model}`}>
          <div>
            <strong>{seat.personality_id}</strong>
            <small>{seat.model}</small>
          </div>
          <button className="icon-button" onClick={() => onRemove(seat.personality_id)}>
            <Trash2 size={15} />
          </button>
        </div>
      ))}
      <p className="mt-3 text-xs text-[color:var(--muted)]">
        Arrastra personalidades aquí o haz click para añadir. Mínimo 3 seats.
      </p>
    </div>
  )
}

function StatusPanel({ status }: { status: SessionStatusPayload | null }) {
  if (!status) {
    return <div className="status-panel mt-4">Sin sesión activa.</div>
  }
  const tone = statusTone(status.status)
  return (
    <section className={`status-panel mt-4 tone-${tone}`}>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          {status.status === 'running' ? <Loader2 className="spin" size={18} /> : <CheckCircle2 size={18} />}
          <strong>{status.status}</strong>
        </div>
        <span>
          {status.cost_so_far_eur.toFixed(2)}€ · {status.elapsed_seconds}s
        </span>
      </div>
      <div className="round-track">
        {[0, 1, 2, 3, 4].map((round) => (
          <span key={round}>
            {status.rounds_completed.includes(round) ? '✓' : status.current_round === round ? '⣾' : '○'} R{round}
          </span>
        ))}
      </div>
      <div className="seat-progress">
        {status.seats_progress.map((seat) => (
          <span className={`seat-chip tone-${statusTone(seat.state)}`} key={seat.seat_idx}>
            {seat.state === 'running' ? <Loader2 className="spin" size={14} /> : <Circle size={14} />}
            {seat.personality}
          </span>
        ))}
      </div>
    </section>
  )
}

function ResultPanel({
  view,
  markdown,
  logs,
}: {
  view: ResultView
  markdown: string
  logs: unknown[]
}) {
  if (view === 'logs') {
    const renderedLogs = logs.map((entry) => JSON.stringify(entry, null, 2)).join('\n')
    return (
      <section className="markdown-panel mt-4">
        <h2 className="section-title">Logs</h2>
        <pre>{renderedLogs || 'Sin logs para esta sesion.'}</pre>
      </section>
    )
  }

  return (
    <section className="markdown-panel mt-4">
      <h2 className="section-title">Stage Final</h2>
      <pre>{markdown || 'El resultado aparecerá aquí cuando la sesión termine.'}</pre>
    </section>
  )
}
