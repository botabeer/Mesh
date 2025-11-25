
import time, threading

def send_with_delay(send_fn, messages, delays=None):
    """send_fn(message) will be called for each message with optional delays list (seconds)"""
    if delays is None:
        delays = [0.5]*len(messages)
    def _runner():
        for m,d in zip(messages, delays):
            time.sleep(d)
            try:
                send_fn(m)
            except Exception:
                pass
    t=threading.Thread(target=_runner, daemon=True)
    t.start()
    return True
