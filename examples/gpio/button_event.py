"""Button event template demonstrating callbacks with gpiozero."""

from __future__ import annotations

from datetime import datetime


def on_press() -> None:
    print(f"[{datetime.now():%H:%M:%S}] Button pressed")


def on_release() -> None:
    print(f"[{datetime.now():%H:%M:%S}] Button released")


def main() -> None:
    try:
        from gpiozero import Button  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit("Install gpiozero before running this template.") from exc

    button = Button(23, pull_up=True, bounce_time=0.05)
    button.when_pressed = on_press
    button.when_released = on_release

    print("Listening for button events on BCM pin 23. Press Ctrl+C to exit.")
    try:
        button.wait_for_inactive()
        button.wait_for_active()
        while True:
            button.wait_for_press()
            button.wait_for_release()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        button.close()


if __name__ == "__main__":
    main()

