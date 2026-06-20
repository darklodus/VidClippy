from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class FFmpegNotFoundError(RuntimeError):
    pass


def ensure_ffmpeg_available() -> None:
    """Raise a helpful error if ffmpeg is not installed or not in PATH."""
    if shutil.which("ffmpeg") is None:
        raise FFmpegNotFoundError(
            "FFmpeg was not found. Install FFmpeg and make sure `ffmpeg` is available in PATH."
        )


def build_output_path(input_path: Path, start: str, length: str) -> Path:
    """Build a default output filename beside the input file."""
    safe_start = str(start).replace(":", "-").replace(".", "_")
    safe_length = str(length).replace(":", "-").replace(".", "_")
    return input_path.with_name(f"{input_path.stem}_clip_{safe_start}_{safe_length}{input_path.suffix}")


def clip_video(
    input_file: str | Path,
    start: str | int | float,
    length: str | int | float,
    output_file: str | Path | None = None,
    overwrite: bool = False,
    reencode: bool = False,
) -> Path:
    """
    Clip a video from `start` for `length`.

    Args:
        input_file: Path to the source MP4/video file.
        start: Start time, either seconds like 30 or timestamp like 00:00:30.
        length: Clip duration, either seconds like 30 or timestamp like 00:00:30.
        output_file: Optional output path. If omitted, one is generated.
        overwrite: Replace existing output file if True.
        reencode: Use frame-accurate re-encoding if True. Otherwise use fast stream copy.

    Returns:
        Path to the clipped output video.
    """
    ensure_ffmpeg_available()

    input_path = Path(input_file).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    output_path = (
        Path(output_file).expanduser().resolve()
        if output_file is not None
        else build_output_path(input_path, str(start), str(length)).resolve()
    )

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use overwrite=True or --overwrite."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y" if overwrite else "-n",
        "-ss",
        str(start),
        "-i",
        str(input_path),
        "-t",
        str(length),
    ]

    if reencode:
        command += [
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
        ]
    else:
        command += ["-c", "copy"]

    command.append(str(output_path))

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"FFmpeg failed with exit code {exc.returncode}") from exc

    return output_path
