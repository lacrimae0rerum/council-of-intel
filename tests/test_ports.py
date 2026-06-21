import socket

from council_of_intel.api.ports import choose_port


def test_choose_port_uses_preferred_when_free() -> None:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        free_port = sock.getsockname()[1]

    assert choose_port(free_port, (free_port + 1, free_port + 2)) == free_port


def test_choose_port_falls_back_when_preferred_is_busy() -> None:
    with socket.socket() as busy:
        busy.bind(("127.0.0.1", 0))
        preferred = busy.getsockname()[1]
        fallback = preferred + 1

        assert choose_port(preferred, (fallback, fallback)) == fallback


def test_choose_port_raises_when_all_ports_busy() -> None:
    sockets = []
    try:
        first = socket.socket()
        first.bind(("127.0.0.1", 0))
        preferred = first.getsockname()[1]
        sockets.append(first)
        second = socket.socket()
        second.bind(("127.0.0.1", 0))
        fallback = second.getsockname()[1]
        sockets.append(second)

        try:
            choose_port(preferred, (fallback, fallback))
        except RuntimeError as exc:
            assert "todos ocupados" in str(exc)
        else:
            raise AssertionError("choose_port should fail when every port is busy")
    finally:
        for sock in sockets:
            sock.close()
