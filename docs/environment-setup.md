# Environment Setup Tutorial

## Activate the Virtual Environment
- From the repository root, run `source .venv/bin/activate` (use `.\.venv\Scripts\activate` on Windows for remote development).
- Confirm the prompt shows `(.venv)` and Python resolves to the virtualenv with `which python`.

## Install Additional Python Packages
- Use `pip install <package>` while the environment is active.
- Record optional dependencies in `configs/requirements.txt` when they are broadly useful.
- Run `pip freeze > configs/requirements.lock` if you need a deterministic snapshot.

## Environment Variables
- Copy `configs/config.yaml.example` to `configs/config.yaml` and adjust paths or GPIO pin assignments.
- Create a `.env` file to store secrets such as API tokens. Use `python-dotenv` to load them in scripts.

## Health Checks
- `python scripts/hardware_check.py` prints system compatibility and JSON results for automation.
- `python scripts/camera-test.py` validates camera capture pipeline.
- `python scripts/gpio-test.py` verifies LED blinking on the configured pin.

## IDE Recommendations
- Install the `Microsoft Python` extension in VS Code for linting and IntelliSense.
- Enable remote SSH development (`code --remote ssh-remote+pi@raspberrypi.local`).
- Configure the default formatter (`black`) and linter (`ruff`) in `.vscode/settings.json` if you standardise on them.

