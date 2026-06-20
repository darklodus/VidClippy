# VidClippy

VidClippy is a small Python toolkit for clipping MP4 videos using FFmpeg.

## Requirements

1. Python 3.9+
2. FFmpeg installed and available from your terminal:
   ```bash
   ffmpeg -version
   ```

## Basic usage

Clip the first 30 seconds:

```bash
python clip_video.py "input.mp4" --start 0 --length 30
```

Clip from 1 minute 10 seconds for 30 seconds:

```bash
python clip_video.py "input.mp4" --start 70 --length 30
```

Choose an output file:

```bash
python clip_video.py "input.mp4" --start 0 --length 30 --output "clip.mp4"
```

## Time formats supported

You can use seconds:

```bash
--start 90 --length 30
```

Or timestamp style:

```bash
--start 00:01:30 --length 00:00:30
```

## Fast copy mode vs re-encode mode

By default, this uses FFmpeg stream copy mode, which is very fast and avoids quality loss:

```bash
-c copy
```

For frame-accurate clips, use:

```bash
python clip_video.py "input.mp4" --start 3.25 --length 10 --reencode
```

Re-encoding is slower but more precise.

## Batch usage

Create a `clips.json` file:

```json
[
  {
    "input": "video.mp4",
    "start": "0",
    "length": "30",
    "output": "clip_001.mp4"
  },
  {
    "input": "video.mp4",
    "start": "00:01:00",
    "length": "00:00:15",
    "output": "clip_002.mp4"
  }
]
```

Run:

```bash
python batch_clip_video.py clips.json
```
