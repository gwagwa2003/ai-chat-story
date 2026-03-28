import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOTENV_PATH = PROJECT_ROOT / ".env"


def load_dotenv(path: str | Path | None = None) -> None:
    dotenv_path = Path(path) if path else DEFAULT_DOTENV_PATH
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        os.environ.setdefault(key, value)


def get_env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(f"Missing required environment variable: {name}")


def resolve_project_path(path_value: str) -> str:
    path = Path(path_value)
    if path.is_absolute():
        return str(path)
    return str((PROJECT_ROOT / path).resolve())


def get_server_host() -> str:
    return get_env("SERVER_HOST", "localhost") or "localhost"


def get_server_port() -> int:
    return int(get_env("SERVER_PORT", "8888") or "8888")


def get_default_chat_model() -> str:
    return (
        get_env(
            "DEFAULT_CHAT_MODEL",
            "ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j",
        )
        or "ft:gpt-4o-mini-2024-07-18:personal:chatv1:AESsNK7j"
    )


def get_openai_api_key() -> str:
    return require_env("OPENAI_API_KEY")


def get_anthropic_api_key() -> str:
    return require_env("ANTHROPIC_API_KEY")


def get_gpt_sovits_api_url() -> str:
    return get_env("GPT_SOVITS_API_URL", "http://localhost:9872/") or "http://localhost:9872/"


def get_tts_ref_audio_path() -> str:
    return resolve_project_path(
        get_env("TTS_REF_AUDIO", "server/Voice/ly_refaudio.wav")
        or "server/Voice/ly_refaudio.wav"
    )


def get_tts_aux_ref_audio_paths() -> list[str]:
    raw_value = (
        get_env("TTS_AUX_REF_AUDIO", "server/Voice/ly_refaudio.wav")
        or "server/Voice/ly_refaudio.wav"
    )
    return [
        resolve_project_path(path.strip())
        for path in raw_value.split(",")
        if path.strip()
    ]


def get_tts_prompt_text() -> str:
    return (
        get_env("TTS_PROMPT_TEXT", "因為你身上別著星穹列車的徽章呀，我在大銀幕上見過!")
        or "因為你身上別著星穹列車的徽章呀，我在大銀幕上見過!"
    )


def get_gpt_weights_path() -> str:
    return resolve_project_path(
        get_env("GPT_WEIGHTS_PATH", "server/GPT_weights/D2-e15.ckpt")
        or "server/GPT_weights/D2-e15.ckpt"
    )


def get_sovits_weights_path() -> str:
    return resolve_project_path(
        get_env("SOVITS_WEIGHTS_PATH", "server/SoVITS_weights/D2_e8_s120.pth")
        or "server/SoVITS_weights/D2_e8_s120.pth"
    )


load_dotenv()

