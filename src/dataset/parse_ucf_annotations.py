"""
UCF-Crime Annotation Parser
============================

The official UCF-Crime dataset ships a temporal annotation file:
  Temporal_Anomaly_Annotation.txt

Format (space-separated):
  VideoName.mp4  ClassName  StartFrame1  EndFrame1  StartFrame2  EndFrame2

This script converts that file to the CSV format expected by generate_graphs.py:
  video_name, start_frame, end_frame, label

Usage:
    python dataset/parse_ucf_annotations.py \\
        --input /path/to/Temporal_Anomaly_Annotation.txt \\
        --output ../data/annotations/ucf_annotations.csv
"""

import argparse
import csv
from pathlib import Path


def parse_ucf_annotation_file(input_path, output_path):
    """Convert UCF-Crime annotation txt to CSV."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 4:
                continue

            video_name = parts[0]          # e.g. Abuse001_x264.mp4
            class_name = parts[1]          # e.g. Abuse

            # Annotation can have 1 or 2 temporal segments
            # Format: VideoName  Class  S1  E1  [S2  E2]
            segments = []
            i = 2
            while i + 1 < len(parts):
                start = int(parts[i])
                end   = int(parts[i + 1])
                if start != -1:
                    segments.append((start, end))
                i += 2

            if segments:
                for start, end in segments:
                    rows.append({
                        "video_name":  video_name,
                        "start_frame": start,
                        "end_frame":   end,
                        "label":       1,
                        "class_name":  class_name
                    })
            else:
                # Whole video is anomalous
                rows.append({
                    "video_name":  video_name,
                    "start_frame": -1,
                    "end_frame":   -1,
                    "label":       1,
                    "class_name":  class_name
                })

    with open(output_path, "w", newline="") as f:
        fieldnames = ["video_name", "start_frame", "end_frame", "label", "class_name"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsed {len(rows)} annotation entries → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse UCF-Crime temporal annotations")
    parser.add_argument("--input",  required=True, help="Path to Temporal_Anomaly_Annotation.txt")
    parser.add_argument("--output", default="../data/annotations/ucf_annotations.csv")
    args = parser.parse_args()

    parse_ucf_annotation_file(args.input, args.output)
