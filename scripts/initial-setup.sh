#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
REQUIREMENTS_FILE="${ROOT_DIR}/configs/requirements.txt"
LOG_DIR="${ROOT_DIR}/logs"

APT_PACKAGES=(
  python3
  python3-pip
  python3-venv
  python3-numpy
  python3-opencv
  python3-libcamera
  python3-picamera2
  python3-gpiozero
  python3-rpi-lgpio
  libcamera-apps
  ffmpeg
)

print_header() {
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

ensure_running_on_pi() {
  if [[ ! -f /proc/device-tree/model ]]; then
    echo "[WARN] Unable to detect Raspberry Pi model (missing /proc/device-tree/model)."
    echo "       Continuing anyway, but hardware-specific steps may fail."
    return
  fi

  local model
  model=$(tr -d '\0' < /proc/device-tree/model)
  echo "[INFO] Detected device: ${model}"

  if [[ "${model}" != *"Raspberry Pi 5"* ]]; then
    echo "[WARN] This starter kit is optimised for Raspberry Pi 5, but detected: ${model}"
    echo "       Continuing with best-effort installation."
  fi
}

update_system() {
  print_header "Updating package lists"
  sudo apt update

  print_header "Installing base dependencies"
  sudo apt install -y "${APT_PACKAGES[@]}"
}

enable_camera_stack() {
  if command -v raspi-config >/dev/null 2>&1; then
    print_header "Ensuring camera stack is enabled"
    sudo raspi-config nonint do_camera 0 || true
    sudo raspi-config nonint do_i2c 0 || true
    sudo raspi-config nonint do_spi 0 || true
  else
    echo "[WARN] raspi-config not found; skipping automated interface enablement."
    echo "       Please enable camera, I2C, and SPI manually if required."
  fi
}

create_virtualenv() {
  print_header "Configuring Python virtual environment"

  if [[ -d "${VENV_DIR}" ]]; then
    echo "[INFO] Reusing existing virtual environment at ${VENV_DIR}"
  else
    python3 -m venv "${VENV_DIR}"
    echo "[INFO] Created virtual environment at ${VENV_DIR}"
  fi

  # shellcheck disable=SC1090
  source "${VENV_DIR}/bin/activate"

  python -m pip install --upgrade pip wheel

  if [[ -f "${REQUIREMENTS_FILE}" ]]; then
    python -m pip install -r "${REQUIREMENTS_FILE}"
  else
    echo "[WARN] Requirements file not found at ${REQUIREMENTS_FILE}; skipping pip install."
  fi
}

prep_directories() {
  mkdir -p "${LOG_DIR}"
  mkdir -p "${ROOT_DIR}/artifacts/captures"
  mkdir -p "${ROOT_DIR}/artifacts/gpio"
  echo "[INFO] Created standard directories under ${ROOT_DIR}/artifacts"
}

post_install_summary() {
  print_header "Installation summary"
  echo "Repository directory : ${ROOT_DIR}"
  echo "Virtual environment  : ${VENV_DIR}"
  echo "Requirements         : ${REQUIREMENTS_FILE}"
  echo "Log directory        : ${LOG_DIR}"
  echo "Activate environment with: source ${VENV_DIR}/bin/activate"
  echo "Run hardware checks using: python scripts/hardware_check.py"
}

main() {
  ensure_running_on_pi
  update_system
  enable_camera_stack
  create_virtualenv
  prep_directories
  post_install_summary
}

main "$@"
