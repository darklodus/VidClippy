from __future__ import annotations

import argparse
import json
from pathlib import Path

from video_clipper import clip_video


def main() -> None:
    parser = argparse.ArgumentParser(description="VidClippy: create multiple clips from a JSON file.")
    parser.add_argument("json_file", help="Path to a clips JSON file.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output files if they already exist.",
    )
    parser.add_argument(
        "--reencode",
        action="store_true",
        help="Re-encode all clips for frame-accurate clipping.",
    )

    args = parser.parse_args()

    json_path = Path(args.json_file).expanduser().resolve()
    clips = json.loads(json_path.read_text(encoding="utf-8"))

    if not isinstance(clips, list):
        raise ValueError("The JSON file must contain a list of clip definitions.")

    for index, clip in enumerate(clips, start=1):
        try:
            output = clip_video(
                input_file=clip["input"],
                start=clip["start"],
                length=clip["length"],
                output_file=clip.get("output"),
                overwrite=args.overwrite,
                reencode=args.reencode,
            )
            print(f"[{index}] VidClippy created clip: {output}")
        except Exception as exc:
            print(f"[{index}] Failed: {exc}")


if __name__ == "__main__":
    main()
