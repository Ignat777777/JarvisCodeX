from __future__ import annotations

import math

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QBrush, QLinearGradient, QPainter, QPainterPath


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _mix(color_a: QColor, color_b: QColor, ratio: float) -> QColor:
    ratio = _clamp(float(ratio), 0.0, 1.0)
    inv = 1.0 - ratio
    return QColor(
        int(color_a.red() * inv + color_b.red() * ratio),
        int(color_a.green() * inv + color_b.green() * ratio),
        int(color_a.blue() * inv + color_b.blue() * ratio),
    )


def _with_alpha(color: QColor, alpha: float) -> QColor:
    out = QColor(color)
    out.setAlpha(max(0, min(255, int(alpha))))
    return out


def _accent_from_palette(palette: object) -> QColor:
    user_accent = QColor(str(getattr(palette, "accent", "") or ""))
    if not user_accent.isValid():
        return QColor("#f0187d")
    return user_accent


def _vertical_boundary(
    width: int,
    height: int,
    anchor: float,
    amplitude: float,
    phase: float,
    phase_offset: float,
    skew: float,
    motion: float,
) -> list[tuple[float, float]]:
    w = float(max(2, width))
    h = float(max(2, height))
    step = 4 if h <= 760 else 5
    points: list[tuple[float, float]] = []
    drift = math.sin(phase * 0.42 + phase_offset * 0.7) * w * 0.006 * motion
    for raw_y in range(0, int(h) + step, step):
        y = min(h, float(raw_y))
        u = y / max(1.0, h)
        shoulder = math.sin((u * math.pi) + phase_offset) * amplitude
        ripple = math.sin((u * math.tau * 1.18) + (phase * 0.36) + phase_offset) * amplitude * 0.22 * motion
        slow = math.sin((u * math.tau * 0.48) - (phase * 0.22) + phase_offset * 1.4) * amplitude * 0.16 * motion
        x = (w * anchor) + shoulder + ripple + slow + ((u - 0.5) * skew * w) + drift
        points.append((y, _clamp(x, 0.0, w)))
    if points[-1][0] < h:
        points.append((h, points[-1][1]))
    return points


def _boundary_path(left: list[tuple[float, float]], right: list[tuple[float, float]]) -> QPainterPath:
    path = QPainterPath()
    path.setFillRule(Qt.WindingFill)
    count = min(len(left), len(right))
    if count < 2:
        return path
    path.moveTo(left[0][1], left[0][0])
    for index in range(1, count):
        path.lineTo(left[index][1], left[index][0])
    for index in range(count - 1, -1, -1):
        path.lineTo(right[index][1], right[index][0])
    path.closeSubpath()
    return path


def _right_path(boundary: list[tuple[float, float]], width: int, height: int) -> QPainterPath:
    path = QPainterPath()
    path.setFillRule(Qt.WindingFill)
    if len(boundary) < 2:
        return path
    edge = float(max(2, width))
    h = float(max(2, height))
    path.moveTo(boundary[0][1], 0.0)
    for y, x in boundary[1:]:
        path.lineTo(x, y)
    path.lineTo(edge, h)
    path.lineTo(edge, 0.0)
    path.closeSubpath()
    return path


def _gradient_for_band(
    width: int,
    left_color: QColor,
    right_color: QColor,
    left_alpha: float,
    right_alpha: float,
) -> QLinearGradient:
    gradient = QLinearGradient(0.0, 0.0, float(max(2, width)), 0.0)
    gradient.setColorAt(0.00, _with_alpha(left_color, left_alpha))
    gradient.setColorAt(0.62, _with_alpha(_mix(left_color, right_color, 0.42), (left_alpha + right_alpha) * 0.52))
    gradient.setColorAt(1.00, _with_alpha(right_color, right_alpha))
    return gradient


def _draw_bottom_reflection(painter: QPainter, width: int, height: int, accent: QColor, opacity: float) -> None:
    w = float(max(2, width))
    h = float(max(2, height))
    reflection = QLinearGradient(w * 0.45, h * 0.74, w * 0.88, h)
    reflection.setColorAt(0.00, QColor(0, 0, 0, 0))
    reflection.setColorAt(0.58, _with_alpha(_mix(accent, QColor("#ffffff"), 0.16), 38 * opacity))
    reflection.setColorAt(1.00, QColor(0, 0, 0, 0))
    painter.fillRect(QRectF(0.0, 0.0, w, h), QBrush(reflection))


def draw_waves1_background(
    painter: QPainter,
    width: int,
    height: int,
    phase: float,
    palette: object,
    *,
    user_shift_x: float = 0.0,
    user_shift_y: float = 0.0,
    user_scale: float = 1.0,
    user_rotation_deg: float = 0.0,
    opacity_scale: float = 1.0,
    animations_enabled: bool = True,
) -> None:
    w = max(2, int(width))
    h = max(2, int(height))
    opacity = _clamp(float(opacity_scale), 0.0, 1.0)
    motion = 1.0 if bool(animations_enabled) else 0.0
    scale = _clamp(float(user_scale), 0.62, 1.82)
    shift_x = _clamp(float(user_shift_x), -float(w) * 0.12, float(w) * 0.12)
    rotation = _clamp(float(user_rotation_deg), -24.0, 24.0)

    accent = _accent_from_palette(palette)
    hot = _mix(accent, QColor("#ffffff"), 0.05)
    pale = _mix(hot, QColor("#ffffff"), 0.26)
    ink = QColor("#03050b")
    layer0 = _mix(ink, hot, 0.12)
    layer1 = _mix(ink, hot, 0.20)
    layer2 = _mix(ink, hot, 0.30)
    layer3 = _mix(ink, hot, 0.42)
    layer4 = _mix(ink, hot, 0.56)

    painter.save()
    try:
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        base = QLinearGradient(0.0, 0.0, float(w), 0.0)
        base.setColorAt(0.00, QColor(0, 0, 0, 0))
        base.setColorAt(0.42, _with_alpha(QColor("#02040a"), 48 * opacity))
        base.setColorAt(0.66, _with_alpha(layer0, 150 * opacity))
        base.setColorAt(1.00, _with_alpha(hot, 236 * opacity))
        painter.fillRect(QRectF(0.0, 0.0, float(w), float(h)), QBrush(base))

        scale_anchor = (scale - 1.0) * 0.045
        anchors = [
            0.528 - scale_anchor,
            0.603 - scale_anchor * 0.62,
            0.670 - scale_anchor * 0.35,
            0.737 - scale_anchor * 0.18,
            0.806,
            0.880 + scale_anchor * 0.12,
        ]
        phase_offsets = [0.15, 0.82, 1.48, 2.18, 2.92, 3.56]
        amplitude_base = max(18.0, float(w) * 0.028) * scale
        skew_base = 0.036 + (rotation / 900.0)
        boundaries: list[list[tuple[float, float]]] = []
        for index, anchor in enumerate(anchors):
            boundary = _vertical_boundary(
                w,
                h,
                anchor + (shift_x / max(1.0, float(w))),
                amplitude_base * (1.18 - index * 0.072),
                float(phase),
                phase_offsets[index],
                skew_base * (1.0 - index * 0.08),
                motion,
            )
            boundaries.append(boundary)

        bands = [
            (ink, layer0, 70, 140),
            (layer0, layer1, 132, 176),
            (layer1, layer2, 156, 190),
            (layer2, layer3, 176, 208),
            (layer3, layer4, 194, 226),
        ]
        for index in range(len(boundaries) - 1):
            left_color, right_color, left_alpha, right_alpha = bands[min(index, len(bands) - 1)]
            path = _boundary_path(boundaries[index], boundaries[index + 1])
            painter.fillPath(
                path,
                QBrush(_gradient_for_band(w, left_color, right_color, left_alpha * opacity, right_alpha * opacity)),
            )

        right_fill = QLinearGradient(float(w) * 0.72, 0.0, float(w), 0.0)
        right_fill.setColorAt(0.00, _with_alpha(layer4, 214 * opacity))
        right_fill.setColorAt(0.38, _with_alpha(hot, 242 * opacity))
        right_fill.setColorAt(1.00, _with_alpha(pale, 246 * opacity))
        painter.fillPath(_right_path(boundaries[-1], w, h), QBrush(right_fill))

        inner_shadow = QLinearGradient(float(w) * 0.47, 0.0, float(w) * 0.74, 0.0)
        inner_shadow.setColorAt(0.00, QColor(0, 0, 0, 0))
        inner_shadow.setColorAt(0.52, _with_alpha(QColor("#03050b"), 84 * opacity))
        inner_shadow.setColorAt(1.00, QColor(0, 0, 0, 0))
        painter.fillRect(QRectF(0.0, 0.0, float(w), float(h)), QBrush(inner_shadow))

        veil = QLinearGradient(0.0, 0.0, float(w) * 0.58, 0.0)
        veil.setColorAt(0.00, _with_alpha(QColor("#02040a"), 252 * opacity))
        veil.setColorAt(0.42, _with_alpha(QColor("#02040a"), 228 * opacity))
        veil.setColorAt(0.78, _with_alpha(QColor("#02040a"), 118 * opacity))
        veil.setColorAt(1.00, QColor(0, 0, 0, 0))
        painter.fillRect(QRectF(0.0, 0.0, float(w), float(h)), QBrush(veil))

        vertical_shade = QLinearGradient(0.0, 0.0, 0.0, float(h))
        vertical_shade.setColorAt(0.00, _with_alpha(QColor("#03050b"), 72 * opacity))
        vertical_shade.setColorAt(0.18, QColor(0, 0, 0, 0))
        vertical_shade.setColorAt(0.78, QColor(0, 0, 0, 0))
        vertical_shade.setColorAt(1.00, _with_alpha(QColor("#03050b"), 80 * opacity))
        painter.fillRect(QRectF(0.0, 0.0, float(w), float(h)), QBrush(vertical_shade))

        _draw_bottom_reflection(painter, w, h, hot, opacity)
    finally:
        painter.restore()
