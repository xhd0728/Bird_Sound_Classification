import os
from pathlib import Path

AUDIO_EXAMPLE_PATH = os.path.join(Path(__file__).resolve().parent.parent, "media", "example_audio")


def ret_file_name(file_name, classic) -> str:
    if os.path.exists(os.path.join(AUDIO_EXAMPLE_PATH, file_name)):
        return os.path.splitext(file_name)[0]
    return os.path.splitext(classic)[0]
