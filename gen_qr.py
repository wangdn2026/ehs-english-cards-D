#!/usr/bin/env python3
"""
D课包 Day1 词卡二维码生成器
- 1-bit 纯黑白 + 最近邻缩放（禁用抗锯齿）
- 每个二维码指向词卡的公开 URL（扫码直达）
"""
import json
import sys
from pathlib import Path
import qrcode

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "img"

BASE_URL = "https://wangdn2026.github.io/ehs-english-cards-D"


def make_qr(url: str, out_path: Path):
    """生成 1-bit 纯黑白二维码（缩放时启用 nearest 邻居）"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.convert("1")  # 1-bit 黑白

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 gen_qr.py <data.json> [limit]")
        sys.exit(1)

    data_file = ROOT / "data" / sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    with open(data_file, encoding="utf-8") as f:
        data = json.load(f)

    cards = data["vocab"]
    if limit > 0:
        cards = cards[:limit]

    print(f"开始生成二维码: {len(cards)} 张")
    for card in cards:
        url = f"{BASE_URL}/day1/{card['id']}.html"
        out = IMG_DIR / f"{card['id']}_qr.png"
        # SVG 风格：1-bit 纯黑 + nearest 缩放
        # 但 qrcode SVG 默认是矢量，转 PNG 用 1-bit 模式更稳
        # 这里输出 SVG 但保留黑白纯色（无渐变）
        make_qr(url, out)
        print(f"  ✓ {card['id']}: {url}")


if __name__ == "__main__":
    main()