"""يستمع لـ Arduino على COM5 ويشغّل ملف صوت عند ضغط الزر."""

import sys
import threading
import time
from pathlib import Path

import serial
from playsound3 import playsound

PORT = "COM5"
BAUD = 9600
PLAY_DURATION_SEC = 60

PC_DIR = Path(__file__).resolve().parent

SOUND_FILES = {
    "1": PC_DIR / "madrid.mp3",      # Pin 4
    "2": PC_DIR / "jordan.mp3",      # Pin 8
    "3": PC_DIR / "wehdat.mp3",      # Pin 9
    "4": PC_DIR / "faisaly.mp3",     # Pin 10
    "5": PC_DIR / "baracalona.mp3",  # Pin 11
}

BUTTON_LABELS = {
    "1": "Pin 4 — madrid",
    "2": "Pin 8 — jordan",
    "3": "Pin 9 — wehdat",
    "4": "Pin 10 — faisaly",
    "5": "Pin 11 — baracalona",
}

_lock = threading.Lock()
_play_generation = 0
_current_sound = None
_active_btn = None


def _stop_current() -> None:
    global _current_sound
    if _current_sound is not None:
        try:
            _current_sound.stop()
        except Exception:
            pass
        _current_sound = None


def _play_file(path: Path, generation: int, btn_id: str) -> None:
    global _current_sound, _active_btn
    sound = None
    try:
        sound = playsound(str(path), block=False)
        with _lock:
            if generation != _play_generation:
                sound.stop()
                return
            _current_sound = sound
            _active_btn = btn_id

        end = time.monotonic() + PLAY_DURATION_SEC
        while time.monotonic() < end:
            with _lock:
                if generation != _play_generation:
                    sound.stop()
                    return
            time.sleep(0.05)

        sound.stop()
    finally:
        with _lock:
            if generation == _play_generation:
                _current_sound = None
                _active_btn = None


def play(btn_id: str) -> None:
    global _play_generation, _active_btn

    path = SOUND_FILES.get(btn_id)
    if not path or not path.exists():
        print(f"ملف الصوت غير موجود: {path}")
        return

    with _lock:
        if _active_btn == btn_id:
            return
        _stop_current()
        _play_generation += 1
        generation = _play_generation

    label = BUTTON_LABELS.get(btn_id, btn_id)
    print(f"زر {btn_id} — {label} ({PLAY_DURATION_SEC} ث)")
    threading.Thread(
        target=_play_file,
        args=(path, generation, btn_id),
        daemon=True,
    ).start()


def main() -> None:
    missing = [p for p in SOUND_FILES.values() if not p.exists()]
    if missing:
        print("ملفات ناقصة:")
        for p in missing:
            print(f"  - {p.name}")
        sys.exit(1)

    print(f"الاتصال بـ {PORT}...")
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except serial.SerialException as e:
        print(f"فشل الاتصال: {e}")
        print("تأكد: Arduino موصول، COM5 صحيح، Serial Monitor مغلق.")
        sys.exit(1)

    try:
        with ser:
            time.sleep(2)
            print("جاهز — 5 أزرار (زر جديد يوقف السابق):")
            for btn_id, label in BUTTON_LABELS.items():
                print(f"  {btn_id}: {label}")
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line in SOUND_FILES:
                    play(line)
    except KeyboardInterrupt:
        with _lock:
            _stop_current()
        print("\nتم الإيقاف.")


if __name__ == "__main__":
    main()
