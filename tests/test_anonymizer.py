from council_of_intel.openrouter.anonymizer import SeatResponse, anonymize_responses


def test_anonymizer_hides_model_provider_and_personality_metadata() -> None:
    responses = [
        SeatResponse(0, "ach-analyst", "anthropic/claude-sonnet-4.6", "ACH content"),
        SeatResponse(1, "red-team", "openai/gpt-5.5", "Red content"),
        SeatResponse(2, "kent", "google/gemini-3.1-pro-preview", "Kent content"),
    ]

    anonymized = anonymize_responses(responses, seed=7)

    public_payload = [item.to_public_dict() for item in anonymized.items]
    assert [item["label"] for item in public_payload] == ["Response A", "Response B", "Response C"]
    assert {item["content"] for item in public_payload} == {
        "ACH content",
        "Red content",
        "Kent content",
    }
    assert all("model" not in item for item in public_payload)
    assert all("personality" not in item for item in public_payload)
    assert {entry.seat_idx for entry in anonymized.mapping.values()} == {0, 1, 2}
