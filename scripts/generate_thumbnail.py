#!/usr/bin/env python3
"""
generate_thumbnail.py

Extract a single frame from a video and save as PNG.

Usage:
  python scripts/generate_thumbnail.py public/videos/truck-auto-loading.mp4 --time 3 --output public/videos/truck-auto-loading.png
"""

import argparse
import os
import cv2

def main():
    p = argparse.ArgumentParser(description='Extract thumbnail from video')
    p.add_argument('video', help='Path to video file')
    p.add_argument('--time', type=float, default=3.0, help='Timestamp in seconds to capture')
    p.add_argument('--output', help='Output image path (PNG). Defaults to video basename + .png')
    p.add_argument('--width', type=int, default=1280, help='Resize width; preserves aspect ratio')
    args = p.parse_args()

    video = args.video
    out = args.output or os.path.splitext(video)[0] + '.png'

    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print('ERROR: cannot open video:', video)
        return 2

    # Seek to approximate timestamp (in milliseconds)
    cap.set(cv2.CAP_PROP_POS_MSEC, int(args.time * 1000))
    ret, frame = cap.read()
    if not ret:
        # fallback to first frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            print('ERROR: cannot read frame from video:', video)
            return 3

    h, w = frame.shape[:2]
    if args.width and w != args.width:
        ratio = args.width / float(w)
        newh = max(1, int(h * ratio))
        frame = cv2.resize(frame, (args.width, newh), interpolation=cv2.INTER_AREA)

    # Ensure directory exists
    out_dir = os.path.dirname(out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    ok = cv2.imwrite(out, frame)
    if not ok:
        print('ERROR: failed to write image to', out)
        return 4

    print('Wrote thumbnail:', out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
