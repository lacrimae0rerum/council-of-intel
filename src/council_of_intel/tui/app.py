"""Textual TUI application."""

from __future__ import annotations

import asyncio

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Label, Markdown, Static, TextArea

from council_of_intel.tui.client import TuiApiClient
from council_of_intel.tui.formatting import default_sats_seats, round_cells, seat_indicator


class CouncilTuiApp(App):
    """Terminal UI for one-shot council sessions."""

    CSS = """
    Screen {
        color: #F5F5F5;
    }
    #title {
        color: #D97757;
        text-style: bold;
    }
    #error {
        color: #D63F3F;
    }
    #status {
        color: #D97757;
    }
    #result {
        height: 1fr;
    }
    Button.primary {
        background: #D97757;
        color: #F5F5F5;
    }
    Button.danger {
        background: #D63F3F;
        color: #F5F5F5;
    }
    """

    BINDINGS = [
        ("q", "cancel_or_quit", "cancelar/salir"),
        ("ctrl+c", "cancel_or_quit", "cancelar/salir"),
        ("l", "load_logs", "logs"),
        ("r", "load_previous", "sesiones"),
    ]

    def __init__(self, api_client: TuiApiClient, polling_interval: float = 1.5) -> None:
        super().__init__()
        self.api_client = api_client
        self.polling_interval = polling_interval
        self.session_id: str | None = None
        self.poll_task: asyncio.Task[None] | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Label("council-of-intel", id="title")
            yield TextArea("Evalua esta intrusión CTI", id="query")
            with Horizontal():
                yield Button("Lanzar sesión", id="launch", classes="primary")
                yield Button("Cancelar", id="cancel", classes="danger")
                yield Button("Sesiones", id="sessions")
                yield Button("Logs", id="logs")
            yield Static("Estado: listo", id="status")
            yield Static("", id="rounds")
            yield Static("", id="seats")
            yield Static("", id="error")
            yield Markdown("", id="result")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "launch":
            await self.launch_session()
        elif event.button.id == "cancel":
            await self.cancel_current_session()
        elif event.button.id == "sessions":
            await self.load_previous_sessions()
        elif event.button.id == "logs":
            await self.load_logs()

    async def launch_session(self) -> None:
        query = self.query_one("#query", TextArea).text.strip()
        self.query_one("#error", Static).update("")
        seats = default_sats_seats(await self.api_client.list_personalities())
        if len(seats) < 3:
            self.query_one("#error", Static).update(
                "No puedo montar los 3 seats SATs por defecto desde /personalities."
            )
            return
        created = await self.api_client.create_session(
            query=query,
            mode="sats",
            chairman_personality="mclaughlin",
            seats=seats,
        )
        self.session_id = created["session_id"]
        self.query_one("#status", Static).update(f"Estado: {created['status']} · {self.session_id}")
        self.poll_task = asyncio.create_task(self.poll_until_terminal())

    async def poll_until_terminal(self) -> None:
        if not self.session_id:
            return
        terminal = {"completed", "cancelled_by_user", "aborted_insufficient_seats"}
        while True:
            try:
                status = await self.api_client.get_status(self.session_id)
            except Exception as exc:
                self.query_one("#error", Static).update(f"Error de conexión: {exc}")
                return
            self.render_status(status)
            if status["status"] in terminal:
                try:
                    markdown = await self.api_client.export_markdown(self.session_id)
                    self.query_one("#result", Markdown).update(markdown)
                except Exception as exc:
                    self.query_one("#error", Static).update(f"Error al exportar resultado: {exc}")
                return
            await asyncio.sleep(self.polling_interval)

    def render_status(self, status: dict) -> None:
        self.query_one("#status", Static).update(
            f"Estado: {status['status']} · Coste: {status['cost_so_far_eur']:.2f}€ · "
            f"Tiempo: {status['elapsed_seconds']}s"
        )
        self.query_one("#rounds", Static).update(
            " · ".join(round_cells(status.get("current_round"), status.get("rounds_completed", [])))
        )
        self.query_one("#seats", Static).update(
            "\n".join(
                f"{seat_indicator(seat['state'])} {seat['personality']} {seat['state']}"
                + (f" ({seat['error']})" if seat.get("error") else "")
                for seat in status.get("seats_progress", [])
            )
        )

    async def cancel_current_session(self) -> None:
        if not self.session_id:
            self.exit()
            return
        cancelled = await self.api_client.cancel_session(self.session_id)
        self.query_one("#status", Static).update(f"Estado: {cancelled['status']}")

    async def action_cancel_or_quit(self) -> None:
        await self.cancel_current_session()

    async def load_logs(self) -> None:
        if not self.session_id:
            self.query_one("#error", Static).update("No hay sesión activa para ver logs.")
            return
        logs = await self.api_client.get_logs(self.session_id)
        self.query_one("#result", Markdown).update(
            "```json\n" + "\n".join(str(entry) for entry in logs) + "\n```"
        )

    async def action_load_logs(self) -> None:
        await self.load_logs()

    async def load_previous_sessions(self) -> None:
        sessions = await self.api_client.list_sessions()
        self.query_one("#result", Markdown).update(
            "\n".join(
                f"- `{session['session_id']}` · {session['status']} · {session['query']}"
                for session in sessions
            )
        )

    async def action_load_previous(self) -> None:
        await self.load_previous_sessions()

    async def on_unmount(self) -> None:
        if self.poll_task and not self.poll_task.done():
            self.poll_task.cancel()
        await self.api_client.close()
