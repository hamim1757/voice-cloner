import uuid
import threading
from pathlib import Path

import gradio as gr
import torch
from TTS.api import TTS

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Italian": "it", "Portuguese": "pt", "Polish": "pl", "Turkish": "tr",
    "Russian": "ru", "Dutch": "nl", "Czech": "cs", "Arabic": "ar",
    "Chinese": "zh-cn", "Japanese": "ja", "Hungarian": "hu",
    "Korean": "ko", "Hindi": "hi",
}

_tts = None
_tts_lock = threading.Lock()
_generation_lock = threading.Lock()

def get_tts():
    global _tts
    if _tts is None:
        with _tts_lock:
            if _tts is None:
                _tts = TTS(
                    model_name=MODEL_NAME,
                    progress_bar=True,
                    gpu=torch.cuda.is_available(),
                )
    return _tts

def generate_voice(reference_audio, text, language_name, consent):
    if not consent:
        raise gr.Error("Please confirm that you own the reference voice or have the speaker's permission.")
    if not reference_audio:
        raise gr.Error("Add a reference voice recording first.")
    if not text or not text.strip():
        raise gr.Error("Enter some text to synthesize.")

    reference_path = Path(str(reference_audio))
    if reference_path.suffix.lower() not in {".wav", ".mp3", ".m4a", ".flac", ".ogg"}:
        raise gr.Error("Use a WAV, MP3, M4A, FLAC, or OGG recording.")

    language = LANGUAGES.get(language_name)
    if not language:
        raise gr.Error("Choose a supported language.")

    output_path = OUTPUT_DIR / f"voice_{uuid.uuid4().hex}.wav"

    try:
        with _generation_lock:
            get_tts().tts_to_file(
                text=text.strip(),
                speaker_wav=str(reference_path),
                language=language,
                file_path=str(output_path),
            )
    except Exception as exc:
        raise gr.Error(f"Generation failed: {exc}") from exc

    return str(output_path)

css = """
.gradio-container { max-width: 980px !important; margin: 0 auto !important; }
.hero { padding: 28px 0 8px; }
.hero h1 { font-size: 42px !important; margin-bottom: 4px !important; }
.hero p { opacity: 0.75; font-size: 16px; }
"""

with gr.Blocks(title="Voice Cloner", css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        '<div class="hero"><h1>Voice Cloner</h1>'
        '<p>Local voice cloning with XTTS-v2. Record or upload a reference voice, '
        'write your text, and generate speech.</p></div>'
    )
    with gr.Row():
        with gr.Column():
            reference_audio = gr.Audio(
                sources=["upload", "microphone"],
                type="filepath",
                label="Reference voice",
            )
            gr.Markdown("Use a clear recording with one speaker and little background noise.")
        with gr.Column():
            language = gr.Dropdown(
                choices=list(LANGUAGES.keys()),
                value="English",
                label="Output language",
            )
            text_input = gr.Textbox(
                label="Text to speak",
                placeholder="Type something for the cloned voice to say...",
                lines=7,
            )
    consent = gr.Checkbox(
        label="I own this voice or have the speaker's explicit permission to use it.",
        value=False,
    )
    generate_button = gr.Button("Generate voice", variant="primary", size="lg")
    output_audio = gr.Audio(label="Generated audio", type="filepath")
    generate_button.click(
        fn=generate_voice,
        inputs=[reference_audio, text_input, language, consent],
        outputs=output_audio,
    )
    gr.Markdown(
        "**Privacy:** this app is designed to run locally. Reference audio is used for "
        "generation and the app only keeps generated files in the outputs folder.\n\n"
        "**Model:** XTTS-v2 has its own model license; review it before commercial use."
    )

if __name__ == "__main__":
    demo.queue().launch()
