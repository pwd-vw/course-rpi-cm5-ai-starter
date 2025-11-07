# GPIO Control Guide

## Pin Numbering
- The project uses Broadcom (BCM) numbering by default.
- Run `pinout` on the Raspberry Pi to view the full header map.

## Quick Tests
- Blink LED: `python scripts/gpio-test.py --led-pin 18`
- PWM fade: `python examples/gpio/pwm_led.py`
- Button events: `python examples/gpio/button_event.py`

## Wiring Conventions
- Always add a current-limiting resistor (e.g. 220 Ω) for LEDs.
- Use the internal pull-ups: `Button(23, pull_up=True)` reduces the need for external resistors.
- Keep wire lengths short (<20 cm) for reliable button reads.

## Safety Tips
- Never exceed 16 mA per GPIO pin or 50 mA total across all pins.
- Power external components (motors, relays) with separate supplies and optocouplers where necessary.
- Disconnect power before modifying the breadboard circuit.

## Extending the Templates
- Replace `LED` with `PWMLED` for dimming control.
- Use `gpiozero.Servo` for pan/tilt rigs (requires 50 Hz PWM-capable pin).
- Combine `Button` and `LED` for interactive tutorials such as Morse code or step-by-step tasks.

