from collections import Counter
from pathlib import Path
import time
from typing import Iterable

import cv2  # type: ignore
import numpy as np  # type: ignore

try:
    import pygame  # type: ignore
except Exception:
    pygame = None


def estimate_distance(bbox_width, known_width, focal_length):
    """
    Estimate distance using the pinhole camera model.
    Distance = (Known Width * Focal Length) / Pixel Width
    """
    if bbox_width > 0:
        return (known_width * focal_length) / bbox_width
    return None


def play_alarm_sound(alarm_type="Beep"):
    """Generate and play an alarm sound."""
    if pygame is None:
        return

    try:
        frequency_map = {
            "Beep": 1000,
            "Siren": 700,
            "Voice Alert": 550,
        }
        duration_map = {
            "Beep": 0.25,
            "Siren": 0.45,
            "Voice Alert": 0.35,
        }

        sample_rate = 44100
        frequency = frequency_map.get(alarm_type, 1000)
        duration = duration_map.get(alarm_type, 0.3)

        samples = int(sample_rate * duration)
        timeline = np.linspace(0, duration, samples, endpoint=False)
        wave = np.sin(2 * np.pi * frequency * timeline)

        if alarm_type == "Siren":
            wave *= np.sin(2 * np.pi * 4 * timeline) * 0.5 + 0.5

        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))

        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.play()
    except Exception:
        pass


def add_text_to_frame(frame, text, position, color=(0, 255, 0), font_scale=1, thickness=2):
    """Add text overlay to a video frame."""
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
    )
    return frame


def draw_distance_box(frame, x1, y1, x2, y2, distance, is_close=False):
    """Draw a bounding box with distance label."""
    color = (0, 0, 255) if is_close else (0, 255, 0)
    thickness = 3 if is_close else 2

    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

    if distance:
        distance_text = f"{distance:.1f}m"
        cv2.putText(
            frame,
            distance_text,
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )

    return frame


def summarize_detected_classes(class_names: Iterable[str]) -> str:
    """Create a compact class summary for a frame."""
    counts = Counter(class_names)
    if not counts:
        return "No detections"
    top_items = [f"{name} x{count}" for name, count in counts.most_common(3)]
    return ", ".join(top_items)


def save_snapshot(frame, output_dir="snapshots"):
    """Save a snapshot and return the output path."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"snapshot_{int(time.time())}.jpg"
    snapshot_path = output_path / filename
    cv2.imwrite(str(snapshot_path), frame)
    return snapshot_path
