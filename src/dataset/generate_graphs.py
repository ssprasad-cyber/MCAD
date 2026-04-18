"""
Graph Dataset Generator — UCF-Crime aware
==========================================

Processes surveillance videos into temporal graph sequences.
Supports:
  - Single video mode  (--video / --label)
  - UCF-Crime bulk mode (--ucf_root)
  - Temporal annotations via --annotations CSV
  - Sliding-window chunking (avoids loading full video to RAM)

UCF-Crime folder structure expected:
    <ucf_root>/
        Anomaly/
            Abuse/        video1.mp4 ...
            Arrest/       ...
            ...
        Normal_Videos_event/   or   Normal/
            Normal_***.mp4

Annotations CSV columns:
    video_name, start_frame, end_frame, label (0/1)
    (leave start/end as -1 to label the full video)

Usage (single video):
    cd src
    python dataset/generate_graphs.py \\
        --video ../data/raw/fight.mp4 \\
        --label 1 \\
        --output_dir ../data/graphs

Usage (UCF-Crime bulk):
    python dataset/generate_graphs.py \\
        --ucf_root /path/to/ucf-crime \\
        --output_dir ../data/graphs \\
        --fps 10 \\
        --window 10 \\
        --stride 5
"""

import os
import cv2
import csv
import json
import argparse
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from edge_processing.frame_capture.frame_packet import FramePacket
from edge_processing.detection.yolov8_detector import YOLOv8Detector
from edge_processing.detection.detection_manager import DetectionManager
from edge_processing.tracking.deepsort_tracker import DeepSortTracker
from edge_processing.tracking.tracking_manager import TrackingManager
from edge_processing.graph.graph_manager import GraphManager
from edge_processing.graph.motion_memory import MotionMemory


# UCF-Crime 13 anomaly class names
UCF_ANOMALY_CLASSES = [
    "abuse", "arrest", "arson", "assault", "burglary",
    "explosion", "fighting", "roadaccidents", "robbery",
    "shooting", "shoplifting", "stealing", "vandalism"
]


def _build_pipeline():
    """Instantiate all pipeline components and return them."""
    detector = YOLOv8Detector("yolov8n.pt")
    detect_mgr = DetectionManager(detector)
    tracker = DeepSortTracker()
    tracking_mgr = TrackingManager(tracker)
    graph_mgr = GraphManager()
    motion_memory = MotionMemory()
    return detect_mgr, tracking_mgr, graph_mgr, motion_memory


def _process_frame(frame, frame_idx, fps, detect_mgr, tracking_mgr, graph_mgr, motion_memory):
    """Run one frame through the pipeline and return a graph dict."""
    timestamp = frame_idx / max(fps, 1)
    pkt = FramePacket(camera_id="dataset_cam", frame=frame, timestamp=timestamp)

    det_pkt = detect_mgr.process(pkt)
    det_pkt.detections = [
        d for d in det_pkt.detections
        if str(d.get("class_name", "")).strip().lower() == "person"
        and d["confidence"] > 0.5
    ]

    track_pkt = tracking_mgr.process(det_pkt)

    people = []
    for track in track_pkt.tracks:
        x1, y1, x2, y2 = map(int, track["bbox"])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        gid = track["track_id"]
        vx, vy = motion_memory.compute(gid, (cx, cy))
        people.append({
            "gid": gid,
            "center": (cx, cy),
            "velocity": (vx, vy),
            "bbox_size": (x2 - x1) * (y2 - y1)
        })

    graph = graph_mgr.process(people)
    return {
        "timestamp": timestamp,
        "nodes": graph["nodes"],
        "edges": graph["edges"]
    }


def load_annotations(csv_path):
    """
    Load temporal annotations from CSV.
    Expected columns: video_name, start_frame, end_frame, label
    Returns dict: { video_stem -> list of (start, end, label) }
    """
    annotations = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stem = Path(row["video_name"]).stem
            start = int(row.get("start_frame", -1))
            end = int(row.get("end_frame", -1))
            lbl = int(row["label"])
            annotations.setdefault(stem, []).append((start, end, lbl))
    return annotations


def frame_label(frame_idx, annotation_segments, default_label):
    """
    Given frame index, determine label from temporal annotation.
    Falls back to default_label if no annotation matches.
    """
    for start, end, lbl in annotation_segments:
        if start == -1 and end == -1:
            return lbl  # whole-video label
        if start <= frame_idx <= end:
            return lbl
    return default_label


def process_video(
    video_path,
    default_label,
    output_dir,
    fps_target=10,
    window_size=10,
    stride=5,
    annotation_segments=None,
    class_id=None,          # optional multi-class id
):
    """
    Process one video file into sliding-window graph sequence JSON files.
    Each output JSON contains one temporal window of graphs.

    Args:
        video_path:           str path to video
        default_label:        int 0/1 used when no per-frame annotation exists
        output_dir:           Path to write output JSONs
        fps_target:           target frames-per-second to sample
        window_size:          number of frames per sequence window
        stride:               sliding window stride
        annotation_segments:  list of (start_frame, end_frame, label) or None
        class_id:             optional int for multi-class mode (None = binary)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    video_stem = Path(video_path).stem
    detect_mgr, tracking_mgr, graph_mgr, motion_memory = _build_pipeline()

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"  [SKIP] Cannot open: {video_path}")
        return 0

    native_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_skip = max(1, round(native_fps / fps_target))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Sliding-window buffer — store processed graph frames
    buffer = []         # list of (frame_index, graph_dict, label)
    window_idx = 0
    saved_count = 0
    abs_frame = 0       # absolute frame counter (including skipped)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if abs_frame % frame_skip == 0:
            # Determine label for this frame
            lbl = frame_label(abs_frame, annotation_segments or [], default_label)
            g = _process_frame(
                frame, abs_frame, native_fps,
                detect_mgr, tracking_mgr, graph_mgr, motion_memory
            )
            buffer.append((abs_frame, g, lbl))

            # Emit window when buffer is full
            while len(buffer) >= window_size:
                window_frames = buffer[:window_size]

                # Majority vote for window label
                window_label = int(
                    sum(lbl for _, _, lbl in window_frames) > window_size // 2
                )

                sequence = [g for _, g, _ in window_frames]

                out = {
                    "video": video_stem,
                    "window_start_frame": window_frames[0][0],
                    "window_end_frame": window_frames[-1][0],
                    "label": window_label,
                    "class_id": class_id,   # None in binary mode
                    "sequence": sequence
                }

                out_path = output_dir / f"{video_stem}_w{window_idx:05d}.json"
                with open(out_path, "w") as f:
                    json.dump(out, f)   # no indent for compact storage

                window_idx += 1
                saved_count += 1
                buffer = buffer[stride:]   # slide

        abs_frame += 1

    cap.release()
    print(f"  [{video_stem}] {saved_count} windows saved → {output_dir}")
    return saved_count


def process_ucf_crime(ucf_root, output_dir, fps_target, window_size, stride, annotations=None):
    """
    Walk UCF-Crime folder structure and process all videos.
    Binary: Anomaly=1, Normal=0
    Multi-class: uses class folder name → UCF_ANOMALY_CLASSES index
    """
    ucf_root = Path(ucf_root)
    total = 0

    # --- Anomaly videos ---
    anomaly_root = ucf_root / "Anomaly"
    if anomaly_root.exists():
        for class_folder in sorted(anomaly_root.iterdir()):
            if not class_folder.is_dir():
                continue
            class_name = class_folder.name.lower()
            class_id = next(
                (i for i, c in enumerate(UCF_ANOMALY_CLASSES) if c in class_name),
                None
            )
            videos = sorted(class_folder.glob("*.mp4")) + sorted(class_folder.glob("*.avi"))
            print(f"\n[Anomaly/{class_folder.name}] {len(videos)} videos")
            for v in videos:
                stem = v.stem
                segs = annotations.get(stem, []) if annotations else []
                total += process_video(
                    v, default_label=1,
                    output_dir=Path(output_dir) / "anomaly",
                    fps_target=fps_target,
                    window_size=window_size,
                    stride=stride,
                    annotation_segments=segs,
                    class_id=class_id
                )
    else:
        print(f"[WARN] No 'Anomaly' folder found at {ucf_root}")

    # --- Normal videos ---
    for candidate in ["Normal_Videos_event", "Normal", "normal"]:
        normal_root = ucf_root / candidate
        if normal_root.exists():
            videos = sorted(normal_root.glob("*.mp4")) + sorted(normal_root.glob("*.avi"))
            print(f"\n[Normal] {len(videos)} videos")
            for v in videos:
                total += process_video(
                    v, default_label=0,
                    output_dir=Path(output_dir) / "normal",
                    fps_target=fps_target,
                    window_size=window_size,
                    stride=stride,
                    annotation_segments=[],
                    class_id=None
                )
            break
    else:
        print("[WARN] No Normal folder found")

    print(f"\nDone. Total windows generated: {total}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCAD Graph Dataset Generator")

    # Mode: single video
    parser.add_argument("--video", type=str, default=None, help="Path to single input video")
    parser.add_argument("--label", type=int, default=0, help="Label for single video (0=normal,1=anomaly)")

    # Mode: UCF-Crime bulk
    parser.add_argument("--ucf_root", type=str, default=None, help="Root of UCF-Crime dataset")

    # Common
    parser.add_argument("--output_dir", type=str, default="../data/graphs", help="Output directory for JSON files")
    parser.add_argument("--fps", type=int, default=10, help="Target FPS for frame extraction")
    parser.add_argument("--window", type=int, default=10, help="Temporal window size (frames)")
    parser.add_argument("--stride", type=int, default=5, help="Sliding window stride")
    parser.add_argument("--annotations", type=str, default=None,
                        help="Optional CSV with temporal annotations (video_name,start_frame,end_frame,label)")

    args = parser.parse_args()

    annotations = load_annotations(args.annotations) if args.annotations else {}

    if args.ucf_root:
        process_ucf_crime(
            ucf_root=args.ucf_root,
            output_dir=args.output_dir,
            fps_target=args.fps,
            window_size=args.window,
            stride=args.stride,
            annotations=annotations
        )
    elif args.video:
        video_stem = Path(args.video).stem
        segs = annotations.get(video_stem, [])
        process_video(
            video_path=args.video,
            default_label=args.label,
            output_dir=args.output_dir,
            fps_target=args.fps,
            window_size=args.window,
            stride=args.stride,
            annotation_segments=segs
        )
    else:
        parser.error("Provide --video or --ucf_root")
