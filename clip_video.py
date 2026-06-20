from __future__ import annotations

import argparse
from video_clipper import clip_video


def main() -> None:
    parser = argparse.ArgumentParser(
        description="VidClippy: clip an MP4/video file from a start time for a given duration."
    )
    parser.add_argument("input", help="Path to the input video file.")
    parser.add_argument(
        "--start",
        required=True,
        help="Start time in seconds or HH:MM:SS format. Example: 0 or 00:01:30",
    )
    parser.add_argument(
        "--length",
        required=True,
        help="Clip length in seconds or HH:MM:SS format. Example: 30 or 00:00:30",
    )
    parser.add_argument(
        "--output",
        help="Optional output video path. If omitted, a filename is generated.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    parser.add_argument(
        "--reencode",
        action="store_true",
        help="Re-encode for frame-accurate clipping. Slower, but more precise.",
    )

    args = parser.parse_args()

    output = clip_video(
        input_file=args.input,
        start=args.start,
        length=args.length,
        output_file=args.output,
        overwrite=args.overwrite,
        reencode=args.reencode,
    )

    print(f"VidClippy created clip: {output}")


if __name__ == "__main__":
    main()
