"""Hardware compatibility checker for Raspberry Pi 5 setup."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


CHECKS: List[Dict[str, Any]] = []


def register_check(func):
    CHECKS.append({"name": func.__name__.replace("check_", "").replace("_", " "), "func": func})
    return func


def run_command(cmd: List[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def which(program: str) -> bool:
    return shutil.which(program) is not None


def bool_icon(ok: bool) -> str:
    return "✅" if ok else "⚠️"


def print_section(title: str) -> None:
    print("\n" + title)
    print("-" * len(title))


@register_check
def check_model() -> Dict[str, Any]:
    model_path = Path("/proc/device-tree/model")
    if not model_path.exists():
        return {
            "status": False,
            "details": "Unable to read /proc/device-tree/model. Is this running on Raspberry Pi OS?",
        }

    model = model_path.read_text(encoding="utf-8", errors="ignore").strip("\0\n ")
    return {
        "status": "Raspberry Pi 5" in model,
        "details": model,
    }


@register_check
def check_os_release() -> Dict[str, Any]:
    os_release: Dict[str, str] = {}
    os_release_path = Path("/etc/os-release")
    if os_release_path.exists():
        for line in os_release_path.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                os_release[key] = value.strip('"')

    pretty_name = os_release.get("PRETTY_NAME", platform.platform())
    supported = "Debian" in pretty_name or "Raspbian" in pretty_name
    return {"status": supported, "details": pretty_name}


@register_check
def check_kernel_version() -> Dict[str, Any]:
    kernel = platform.release()
    supported = kernel.startswith("6.")
    return {"status": supported, "details": kernel}


@register_check
def check_camera_interfaces() -> Dict[str, Any]:
    video_devices = sorted(Path("/dev").glob("video*"))
    media_devices = sorted(Path("/dev").glob("media*"))
    libcamera_cli = which("libcamera-jpeg") or which("libcamera-hello")
    status = bool(video_devices or media_devices) and libcamera_cli
    details = {
        "video": [p.name for p in video_devices],
        "media": [p.name for p in media_devices],
        "libcamera_cli": bool(libcamera_cli),
    }
    return {"status": status, "details": details}


@register_check
def check_camera_python() -> Dict[str, Any]:
    try:
        import picamera2  # type: ignore

        version = getattr(picamera2, "__version__", "unknown")
        return {"status": True, "details": f"picamera2 {version}"}
    except ModuleNotFoundError:
        return {
            "status": False,
            "details": "picamera2 Python module not found. Install with 'sudo apt install python3-picamera2'.",
        }


@register_check
def check_gpio_libraries() -> Dict[str, Any]:
    libraries = {
        "gpiozero": False,
        "RPi.GPIO": False,
        "rpi_lgpio": False,
    }
    try:
        import gpiozero  # type: ignore

        libraries["gpiozero"] = True
    except ModuleNotFoundError:
        pass

    try:
        import RPi.GPIO  # type: ignore

        libraries["RPi.GPIO"] = True
    except ModuleNotFoundError:
        pass

    try:
        import rpi_lgpio  # type: ignore

        libraries["rpi_lgpio"] = True
    except ModuleNotFoundError:
        pass

    status = any(libraries.values())
    return {"status": status, "details": libraries}


@register_check
def check_interfaces_enabled() -> Dict[str, Any]:
    def enabled(path: str) -> bool:
        return Path(path).exists()

    interfaces = {
        "I2C": enabled("/dev/i2c-1"),
        "SPI": enabled("/dev/spidev0.0"),
        "GPIO": enabled("/dev/gpiomem"),
    }
    status = all(interfaces.values())
    return {"status": status, "details": interfaces}


@register_check
def check_disk_space() -> Dict[str, Any]:
    try:
        stat = os.statvfs("/")
    except AttributeError:
        return {"status": False, "details": "statvfs not available on this platform"}

    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    status = free_gb >= 2.0
    return {"status": status, "details": f"{free_gb:.2f} GB free"}


@register_check
def check_gpu_memory() -> Dict[str, Any]:
    if which("vcgencmd"):
        result = run_command(["vcgencmd", "get_mem", "gpu"])
        status = result.returncode == 0 and "gpu" in result.stdout.lower()
        details = result.stdout.strip() if result.stdout else result.stderr.strip()
        return {"status": status, "details": details}
    return {
        "status": False,
        "details": "vcgencmd command not found. Install 'raspi-config' or enable VPU firmware tools.",
    }


def main() -> None:
    print_section("Raspberry Pi 5 Hardware Compatibility Check")
    results: Dict[str, Dict[str, Any]] = {}

    for check in CHECKS:
        outcome = check["func"]()
        results[check["name"]] = outcome
        icon = bool_icon(outcome.get("status", False))
        print(f"{icon} {check['name'].title():<30} -> {outcome['details']}")

    print_section("JSON Output")
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)

