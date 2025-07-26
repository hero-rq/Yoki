import socket
import logging
from contextlib import contextmanager
from typing import Optional

@contextmanager
def secure_connection(host: str, port: int, timeout: float = 2.0):
    """Safely open and close a socket connection."""
    sock = None
    try:
        logging.info(f"Connecting to {host}:{port}...")
        sock = socket.create_connection((host, port), timeout=timeout)
        yield sock
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        logging.warning(f"Connection error: {e}")
        yield None
    finally:
        if sock:
            sock.close()
            logging.info("Connection safely closed.")

class ResponseAnalyzer:
    """Classify server responses to identify vulnerabilities automatically."""

    PATTERNS = {
        'crash': [b'segmentation fault', b'core dumped', b'access violation'],
        'error': [b'error', b'fail', b'invalid'],
        'success': [b'ok', b'success', b'accepted'],
    }

    @classmethod
    def analyze(cls, response: Optional[bytes], timing: float) -> str:
        if response is None:
            return 'no_response'

        for status, patterns in cls.PATTERNS.items():
            if any(pattern in response.lower() for pattern in patterns):
                return status

        if timing > 5.0:
            return 'slow_response'

        return 'unknown'

# Example usage:
with secure_connection('example.com', 80) as sock:
    if sock:
        sock.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
        response = sock.recv(4096)
        status = ResponseAnalyzer.analyze(response, timing=1.2)
        logging.info(f"Server response status: {status}")
