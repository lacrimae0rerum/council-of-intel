import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest

from council_of_intel.api.manager import SessionExecutionRequest
from council_of_intel.api.runner import ProtocolSessionRunner
from council_of_intel.config import load_config
from council_of_intel.openrouter.client import ChatCompletionResult
from council_of_intel.personalities.loader import load_personalities
from council_of_intel.storage.sessions import SessionStore
from council_of_intel.validation import SeatConfig


@pytest.fixture
def runtime_dir() -> Path:
    path = Path("test-artifacts") / f"runner-{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)


class FakeClient:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = outputs

    async def complete_chat(self, request) -> ChatCompletionResult:
        content = self.outputs.pop(0)
        return ChatCompletionResult(
            seat_idx=request.seat_idx,
            model=request.model,
            content=content,
            usage_cost=0.1,
            raw_response={"usage": {"cost": 0.1}},
        )


@pytest.mark.asyncio
async def test_protocol_session_runner_persists_completed_session(runtime_dir: Path) -> None:
    store = SessionStore(runtime_dir / "sessions", runtime_dir / "index.sqlite3")
    config = load_config()
    catalog = load_personalities()
    client = FakeClient(
        [
            "R1 ACH",
            "R1 Red",
            "R1 Devils",
            "Winner: Response A\nEngage B and C.",
            "Winner: Response A\nEngage B and C.",
            "Winner: Response A\nEngage B and C.",
            "Counterfactual.",
            "# Stage Final: Council Answer\nFinal real.",
        ]
    )
    runner = ProtocolSessionRunner(config=config, catalog=catalog, client=client)
    session_id = "runner-test"
    now = datetime.now(UTC)
    request = SessionExecutionRequest(
        session_id=session_id,
        query="Evalua esto",
        mode="sats",
        seats=[
            SeatConfig(personality_id="ach-analyst", model="openai/gpt-5.5"),
            SeatConfig(personality_id="red-team", model="anthropic/claude-sonnet-4.6"),
            SeatConfig(personality_id="devils-advocate", model="google/gemini-3.1-pro-preview"),
        ],
        chairman_personality="mclaughlin",
        store=store,
    )

    await runner.run(request)
    record = store.load(session_id)

    assert record.status == "completed"
    assert record.created_at >= now
    assert record.final_markdown == "# Stage Final: Council Answer\nFinal real."
    assert record.cost_eur == 0.8
