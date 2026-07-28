#!/usr/bin/env python3
"""
D课包 Day1 词卡 HTML 生成器
- 输入：JSON 词条数据 + 元数据
- 输出：单页 HTML 词卡（带喇叭播放键 + 二维码占位）
"""
import json
import os
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).parent
TEMPLATE_FILE = ROOT / "template.html"


def render_card(data: dict, card: dict, prev_url: str = "#", next_url: str = "#") -> str:
    """生成单张词卡 HTML"""
    audio_word_path = f"../audio/{card['id']}_word.mp3"
    audio_example_path = f"../audio/{card['id']}_example.mp3"

    tmpl = Template(TEMPLATE_FILE.read_text(encoding="utf-8"))
    return tmpl.safe_substitute(
        TITLE_ZH=data["title_zh"],
        TITLE_EN=data["title_en"],
        DAY=data["day"],
        PKG=data["package"],
        CARD_ID=card["id"],
        CAT=card["cat"],
        SUB_CAT=card.get("sub_cat", ""),
        EN=card["en"],
        ZH=card["zh"],
        EXAMPLE_EN=card["example_en"],
        EXAMPLE_ZH=card["example_zh"],
        AUDIO_WORD=audio_word_path,
        AUDIO_EXAMPLE=audio_example_path,
        PREV_URL=prev_url,
        NEXT_URL=next_url,
        QR_PLACEHOLDER=f"../img/{card['id']}_qr.png",
    )


def main():
    """命令行：python3 generate.py day1_part1_medical.json"""
    if len(sys.argv) < 2:
        print("用法: python3 generate.py <data.json>")
        sys.exit(1)

    data_file = ROOT / "data" / sys.argv[1]
    if not data_file.exists():
        print(f"数据文件不存在: {data_file}")
        sys.exit(1)

    with open(data_file, encoding="utf-8") as f:
        data = json.load(f)

    out_dir = ROOT / "day1" / data["day"].lower()
    out_dir.mkdir(parents=True, exist_ok=True)

    cards = data["vocab"]
    for i, card in enumerate(cards):
        prev_url = f"{cards[i-1]['id']}.html" if i > 0 else "index.html"
        next_url = f"{cards[i+1]['id']}.html" if i < len(cards) - 1 else "index.html"
        html = render_card(data, card, prev_url, next_url)
        out = out_dir / f"{card['id']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  ✓ {card['id']}: {card['en']}")


if __name__ == "__main__":
    main()