# Voice Cloner

A simple local web app for authorized voice cloning with XTTS-v2.

## Features

- Upload or record a reference voice.
- Enter text and generate speech in the reference voice.
- Multiple language choices.
- Generated WAV files are saved locally in the `outputs/` folder.
- An explicit permission/ownership confirmation is required before generation.

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or 3.11
- Several GB of disk space for the model
- CPU works; a compatible CUDA GPU can accelerate generation

## Install on Windows

Use Python 3.11 if possible:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open the local Gradio URL printed in the terminal.

The first generation downloads XTTS-v2, so the first run can take longer and requires internet access.

## Better reference audio

Use a clean recording with one speaker, little background noise, and natural speech. Several seconds of clear audio is a good starting point.

## Permission

Only clone your own voice or a voice you have the speaker's explicit permission to use. Do not use the app to impersonate someone or mislead people.

## Model license

This repository contains app code, not XTTS-v2 model weights. XTTS-v2 is distributed under the Coqui Public Model License (CPML). Review the model license before redistribution or commercial use.

## Structure

```text
voice-cloner/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```