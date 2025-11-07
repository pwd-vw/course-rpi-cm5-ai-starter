"""Dim an LED using PWM on Raspberry Pi GPIO."""

from __future__ import annotations

import time


def main() -> None:
    try:
        from gpiozero import PWMLED  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit("Install gpiozero before running this template.") from exc

    led = PWMLED(18)
    print("Gradually fading LED on BCM 18. Press Ctrl+C to stop.")

    try:
        while True:
            for duty_cycle in [x / 20 for x in range(21)]:
                led.value = duty_cycle
                time.sleep(0.05)
            for duty_cycle in [x / 20 for x in range(21)]:
                led.value = 1 - duty_cycle
                time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopping PWM example...")
    finally:
        led.close()


if __name__ == "__main__":
    main()

