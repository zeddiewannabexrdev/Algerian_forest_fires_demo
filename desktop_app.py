import os
import sys
import time
import socket
import threading
import subprocess
import urllib.request
import signal

# Redirect stdout/stderr to devnull if None (crucial for PyInstaller windowed execution)
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
    except Exception:
        pass

# Monkeypatch signal handling to allow Streamlit to run safely inside background threads
_orig_signal = signal.signal
def _safe_signal(sig, handler):
    try:
        return _orig_signal(sig, handler)
    except Exception:
        return None
signal.signal = _safe_signal

try:
    import streamlit.web.bootstrap as bootstrap
    bootstrap._set_up_signal_handler = lambda server: None
except Exception:
    pass


def find_free_port() -> int:
    """Finds an available local port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def is_server_ready(url: str, timeout: float = 1.0) -> bool:
    """Checks if the local Streamlit server is answering HTTP requests."""
    for endpoint in [f"{url}/_stcore/health", url]:
        try:
            with urllib.request.urlopen(endpoint, timeout=timeout) as resp:
                if resp.status in (200, 404):
                    return True
        except Exception:
            pass
    return False


def get_base_dir() -> str:
    """Returns the base directory whether running in source or PyInstaller frozen bundle."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
    return os.path.dirname(os.path.abspath(__file__))


def run_streamlit_server(port: int):
    """Executes the Streamlit server in headless mode."""
    try:
        import streamlit.web.cli as stcli

        base_dir = get_base_dir()
        script_path = os.path.join(base_dir, "app.py")

        sys.argv = [
            "streamlit",
            "run",
            script_path,
            "--server.port", str(port),
            "--server.headless", "true",
            "--global.developmentMode", "false",
            "--server.runOnSave", "false"
        ]
        stcli.main()
    except Exception as e:
        with open("stream_server_error.log", "w", encoding="utf-8") as f:
            f.write(f"Streamlit server error: {e}\n")


def main():
    port = find_free_port()
    url = f"http://localhost:{port}"

    print("=====================================================================")
    print(" Forest Fire Analytics Workstation v1.0.0 (Windows x64)")
    print("=====================================================================")
    print(f"[*] Starting Forest Fire Analytics server on port {port}...")

    # Start Streamlit server on a non-daemon background thread so it stays alive
    server_thread = threading.Thread(target=run_streamlit_server, args=(port,), daemon=False)
    server_thread.start()

    # Wait until the Streamlit server is ready (up to 30 seconds)
    server_ok = False
    for _ in range(60):
        if is_server_ready(url):
            server_ok = True
            break
        time.sleep(0.5)

    if not server_ok:
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                "Không thể khởi động máy chủ Streamlit cục bộ. Vui lòng kiểm tra lại môi trường.",
                "Lỗi Khởi Động",
                0x10
            )
        except Exception:
            pass
        return

    print(f"[*] Server ready. Opening desktop workstation interface...")

    # Find Microsoft Edge or Google Chrome executable for native desktop window mode (--app)
    browsers = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    ]
    browser_exe = next((p for p in browsers if os.path.exists(p)), None)

    # Launch standalone window mode
    if browser_exe:
        subprocess.Popen([browser_exe, f"--app={url}"])
    else:
        import webbrowser
        webbrowser.open(url)

    # Keep main process alive while the server is active
    server_thread.join()


if __name__ == "__main__":
    main()
