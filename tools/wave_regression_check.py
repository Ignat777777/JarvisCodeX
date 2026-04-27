import os
import sys
from statistics import median

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, Qt  # type: ignore
from PySide6.QtGui import QImage, QPainter  # type: ignore
from PySide6.QtWidgets import QApplication  # type: ignore

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import main


def _luma(argb: int) -> float:
    r = (argb >> 16) & 0xFF
    g = (argb >> 8) & 0xFF
    b = argb & 0xFF
    return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)


def _max_dark_run_on_core_stripe(image: QImage) -> int:
    w = image.width()
    h = image.height()
    if w <= 8 or h <= 8:
        return 0
    x = max(0, min(w - 1, int(round(w * 0.94))))
    y0 = max(0, int(round(h * 0.12)))
    y1 = max(y0 + 1, int(round(h * 0.88)))
    values = [_luma(image.pixel(x, y)) for y in range(y0, y1)]
    if not values:
        return 0
    mid = float(median(values))
    threshold = max(12.0, mid * 0.46)
    max_run = 0
    cur = 0
    for value in values:
        if value < threshold:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 0
    return int(max_run)


def _render_frame(bg: "main.BackgroundWidget", width: int, height: int, phase: float) -> QImage:
    bg.resize(width, height)
    bg._phase = float(phase)
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    image.fill(0)
    painter = QPainter(image)
    try:
        bg.render(painter, QPoint(0, 0))
    finally:
        painter.end()
    return image


def run_check() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    sizes = [
        (760, 520),
        (880, 620),
        (980, 700),
        (1120, 760),
        (1300, 840),
    ]
    themes = [main.BLUE_THEME, main.ORANGE_THEME]
    worst_run = 0
    failures: list[str] = []

    for palette in themes:
        bg = main.BackgroundWidget(palette)
        bg.set_visual_variant("waves1")
        bg.set_waves_suppressed(False)
        bg.set_animations_enabled(True)
        bg.set_corner_radius(22)
        bg.set_user_wave_transform(shift_x=0.0, shift_y=0.0, scale=1.0, rotation_deg=0.0)
        bg.show()
        app.processEvents()
        for width, height in sizes:
            for phase in (0.0, 0.6, 1.3, 2.1, 3.0, 3.8, 4.5, 5.3):
                frame = _render_frame(bg, width, height, phase)
                run = _max_dark_run_on_core_stripe(frame)
                worst_run = max(worst_run, run)
                if run > 22:
                    failures.append(
                        f"theme={palette.name} size={width}x{height} phase={phase:.2f} dark_run={run}"
                    )
        bg.hide()
        bg.deleteLater()
        app.processEvents()

    if failures:
        print("WAVE_CHECK_FAIL")
        for row in failures[:20]:
            print(row)
        print(f"worst_dark_run={worst_run}")
        return 1

    print("WAVE_CHECK_OK")
    print(f"worst_dark_run={worst_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_check())
