"""يستمع لـ Arduino على COM5 ويشغّل فيديو (صوت + صورة) على شاشة البروجكتور."""

from __future__ import annotations

import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import serial

PORT = "COM5"
BAUD = 9600

# شاشة البروجكتور في Windows (0 = الرئيسية، 1 = الثانية عادةً HDMI)
PROJECTOR_SCREEN = 1

# 0 = تشغيل الملف كاملاً؛ أو حد أقصى بالثواني (مثلاً 60)
PLAY_DURATION_SEC = 0

PC_DIR = Path(__file__).resolve().parent
VIDEO_DIR = PC_DIR / "videos"

# فيديو واحد لكل زر — الصوت والصورة من نفس الملف
VIDEO_FILES = {
    "1": VIDEO_DIR / "realmadrid.mp4",
    "2": VIDEO_DIR / "barca.mp4",
}

BUTTON_LABELS = {
    "1": "Pin 4 — Real Madrid",
    "2": "Pin 8 — Barca",
}

_lock = threading.Lock()
_play_generation = 0
_current_process: subprocess.Popen | None = None
_active_btn: str | None = None

_CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _mpv_exe() -> str | None:
    for name in ("mpv", "mpv.exe"):
        found = shutil.which(name)
        if found:
            return found
    for path in (
        Path(r"C:\Program Files\mpv\mpv.exe"),
        Path(r"C:\Program Files (x86)\mpv\mpv.exe"),
    ):
        if path.is_file():
            return str(path)
    return None


def _vlc_exe() -> str | None:
    for path in (
        Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe"),
        Path(r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"),
    ):
        if path.is_file():
            return str(path)
    return shutil.which("vlc")


def _player_command(path: Path) -> list[str]:
    mpv = _mpv_exe()
    if mpv:
        cmd = [
            mpv,
            f"--screen={PROJECTOR_SCREEN}",
            "--fs",
            "--keep-open=no",
            "--no-terminal",
            "--really-quiet",
            str(path),
        ]
        if PLAY_DURATION_SEC > 0:
            cmd.insert(-1, f"--length={PLAY_DURATION_SEC}")
        return cmd

    vlc = _vlc_exe()
    if vlc:
        cmd = [
            vlc,
            "--fullscreen",
            f"--qt-fullscreen-screen={PROJECTOR_SCREEN}",
            "--play-and-exit",
            "--no-video-title-show",
            "--intf",
            "dummy",
            str(path),
        ]
        if PLAY_DURATION_SEC > 0:
            cmd.insert(1, f"--stop-time={PLAY_DURATION_SEC}")
        return cmd

    raise FileNotFoundError(
        "لم يُعثر على mpv أو VLC. ثبّت أحدهما:\n"
        "  mpv: https://mpv.io/installation/\n"
        "  VLC: https://www.videolan.org/vlc/"
    )


def _stop_current() -> None:
    global _current_process
    proc = _current_process
    if proc is None:
        return
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
    _current_process = None


def _wait_process(proc: subprocess.Popen, generation: int) -> None:
    global _current_process, _active_btn
    try:
        while proc.poll() is None:
            with _lock:
                if generation != _play_generation:
                    proc.terminate()
                    return
            time.sleep(0.1)
    finally:
        with _lock:
            if generation == _play_generation:
                if _current_process is proc:
                    _current_process = None
                _active_btn = None


def play(btn_id: str) -> None:
    global _play_generation, _current_process, _active_btn

    path = VIDEO_FILES.get(btn_id)
    if not path or not path.exists():
        print(f"ملف الفيديو غير موجود: {path}")
        return

    with _lock:
        if _active_btn == btn_id:
            return
        _stop_current()
        _play_generation += 1
        generation = _play_generation

    try:
        cmd = _player_command(path)
    except FileNotFoundError as e:
        print(e)
        return

    label = BUTTON_LABELS.get(btn_id, btn_id)
    duration_note = (
        f" (حد أقصى {PLAY_DURATION_SEC} ث)" if PLAY_DURATION_SEC > 0 else ""
    )
    print(f"زر {btn_id} — {label}{duration_note}")
    print(f"  شاشة {PROJECTOR_SCREEN}: {path.name}")

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=PC_DIR,
            creationflags=_CREATE_NO_WINDOW,
        )
    except OSError as e:
        print(f"فشل التشغيل: {e}")
        return

    with _lock:
        if generation != _play_generation:
            proc.terminate()
            return
        _current_process = proc
        _active_btn = btn_id

    threading.Thread(
        target=_wait_process,
        args=(proc, generation),
        daemon=True,
    ).start()


def main() -> None:
    missing = [p for p in VIDEO_FILES.values() if not p.exists()]
    if missing:
        print(f"ملفات فيديو ناقصة في: {VIDEO_DIR}")
        for p in missing:
            print(f"  - {p.name}")
        sys.exit(1)

    if _mpv_exe():
        player = "mpv"
    elif _vlc_exe():
        player = "vlc"
    else:
        try:
            _player_command(VIDEO_FILES["1"])
        except FileNotFoundError as e:
            print(e)
        sys.exit(1)

    print(f"مشغّل الوسائط: {player}")
    print(f"شاشة البروجكتور (PROJECTOR_SCREEN): {PROJECTOR_SCREEN}")
    print("  إن ظهر الفيديو على الشاشة الخاطئة: غيّر PROJECTOR_SCREEN إلى 0 أو 2")
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
            print("جاهز — الأزرار المفعلة (فيديو بصوت على البروجكتور):")
            for btn_id, label in BUTTON_LABELS.items():
                print(f"  {btn_id}: {label} → {VIDEO_FILES[btn_id].name}")
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line in VIDEO_FILES:
                    play(line)
    except KeyboardInterrupt:
        with _lock:
            _stop_current()
        print("\nتم الإيقاف.")


if __name__ == "__main__":
    main()
