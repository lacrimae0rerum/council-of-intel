"""Local server port selection."""

from __future__ import annotations

import socket


def choose_port(preferred_port: int, fallback_range: tuple[int, int]) -> int:
    """Return the first free port from preferred, then fallback range."""
    candidates = [preferred_port, *range(fallback_range[0], fallback_range[1] + 1)]
    for port in candidates:
        if _is_free(port):
            return port
    start = min(candidates)
    end = max(candidates)
    raise RuntimeError(
        f"Probé puertos {start}-{end}, todos ocupados. Cambia `server.port_range_fallback` "
        "en config.yaml o cierra el proceso que los ocupa."
    )


def _is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True
