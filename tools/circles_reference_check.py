import argparse
import glob
import os
import sys
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint  # type: ignore
from PySide6.QtGui import QImage, QPainter  # type: ignore
from PySide6.QtWidgets import QApplication  # type: ignore

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import main


def _to_rgb_triplet(argb: int) -> tuple[int, int, int]:
    return ((argb >> 16) & 0xFF, (argb >> 8) & 0xFF, argb & 0xFF)


def _mean_abs_error(a: QImage, b: QImage) -> float:
    w = min(a.width(), b.width())
    h = min(a.height(), b.height())
    if w <= 0 or h <= 0:
        return 255.0
    total = 0.0
    count = 0
    for y in range(h):
        for x in range(w):
            ar, ag, ab = _to_rgb_triplet(a.pixel(x, y))
            br, bg, bb = _to_rgb_triplet(b.pixel(x, y))
            total += abs(ar - br) + abs(ag - bg) + abs(ab - bb)
            count += 3
    if count <= 0:
        return 255.0
    return total / float(count)


def _find_circles_roi(reference: QImage) -> tuple[int, int, int, int]:
    w = int(reference.width())
    h = int(reference.height())
    if w <= 4 or h <= 4:
        return 0, 0, max(1, w), max(1, h)
    x_start = max(0, int(w * 0.26))
    x_found = int(w * 0.38)
    step_y = max(1, h // 220)
    min_hits = max(8, int((h / step_y) * 0.10))
    for x in range(x_start, w):
        hits = 0
        for y in range(0, h, step_y):
            r, g, b = _to_rgb_triplet(reference.pixel(x, y))
            if (b - r) > 12 or max(r, g, b) > 42:
                hits += 1
        if hits >= min_hits:
            x_found = x
            break
    left = max(0, x_found - 10)
    return left, 0, max(1, w - left), h


def _render_circles(reference_w: int, reference_h: int) -> QImage:
    bg = main.BackgroundWidget(main.BLUE_THEME)
    bg.set_visual_variant("circles")
    bg.set_waves_suppressed(False)
    bg.set_animations_enabled(False)
    bg.set_window_transparency(0)
    bg.resize(reference_w, reference_h)
    bg.show()
    app = QApplication.instance()
    if app is not None:
        app.processEvents()

    image = QImage(reference_w, reference_h, QImage.Format_ARGB32_Premultiplied)
    image.fill(0)
    painter = QPainter(image)
    try:
        bg.render(painter, QPoint(0, 0))
    finally:
        painter.end()
    return image


def _default_reference_path() -> str:
    from_env = os.environ.get("CIRCLES_REF_PATH", "").strip().strip('"')
    if from_env and os.path.exists(from_env):
        return from_env

    root = os.path.join(ROOT_DIR, "_current_preview")
    pattern = os.path.join(root, "recheck_circles_*", "home_circles.png")
    matches = [p for p in glob.glob(pattern) if os.path.isfile(p)]
    if matches:
        matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return matches[0]

    fallback = os.path.join(root, "home_circles.png")
    if os.path.exists(fallback):
        return fallback
    return ""


def _similarity_once() -> tuple[float, str]:
    ref_path = _default_reference_path()
    if not ref_path or not os.path.exists(ref_path):
        return 0.0, "reference image not found"
    ref = QImage(ref_path)
    if ref.isNull():
        return 0.0, "reference image is invalid"

    rendered = _render_circles(ref.width(), ref.height())
    mae_full = _mean_abs_error(rendered, ref)
    sim_full = max(0.0, 1.0 - (mae_full / 255.0))

    roi_x, roi_y, roi_w, roi_h = _find_circles_roi(ref)
    ref_roi = ref.copy(roi_x, roi_y, roi_w, roi_h)
    rendered_roi = rendered.copy(roi_x, roi_y, roi_w, roi_h)
    mae_roi = _mean_abs_error(rendered_roi, ref_roi)
    sim_roi = max(0.0, 1.0 - (mae_roi / 255.0))

    # Main quality score focuses on the circles region.
    similarity = (sim_full * 0.25) + (sim_roi * 0.75)
    return (
        similarity,
        (
            f"similarity={similarity:.5f} "
            f"(full={sim_full:.5f} roi={sim_roi:.5f}) "
            f"mae_full={mae_full:.3f} mae_roi={mae_roi:.3f} "
            f"roi={roi_x},{roi_y},{roi_w}x{roi_h} "
            f"ref='{ref_path}'"
        ),
    )


def main_cli() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true", help="run check continuously")
    parser.add_argument("--interval", type=float, default=2.0, help="seconds between checks in loop mode")
    parser.add_argument("--iterations", type=int, default=0, help="0 = infinite loop")
    parser.add_argument("--min", dest="min_score", type=float, default=0.905, help="required minimum similarity")
    args = parser.parse_args()

    _ = QApplication.instance() or QApplication(sys.argv)

    def _run_once() -> bool:
        score, line = _similarity_once()
        print(line)
        return score >= float(args.min_score)

    if not args.loop:
        ok = _run_once()
        print("CIRCLES_REF_OK" if ok else "CIRCLES_REF_FAIL")
        return 0 if ok else 1

    index = 0
    while True:
        ok = _run_once()
        status = "OK" if ok else "FAIL"
        print(f"[{index}] {status}")
        index += 1
        if args.iterations > 0 and index >= int(args.iterations):
            break
        time.sleep(max(0.2, float(args.interval)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_cli())
