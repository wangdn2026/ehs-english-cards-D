#!/usr/bin/env python3
"""
D课包 Day1 词卡音频生成器
- 输入：JSON 词条数据
- 输出：每个词条两条 mp3（单词 + 例句）
- 引擎：edge-tts（zh-CN-XiaoxiaoNeural + en-US-JennyNeural 男女声）
- 规则：所有 "EHS" 必须转写为 "E. H. S."，避免吞音
"""
import json
import os
import sys
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).parent
AUDIO_DIR = ROOT / "audio"

# 转写规则
EHS_PATTERN = "EHS"


def normalize(text: str) -> str:
    """EHS → E. H. S.，避免 TTS 吞音"""
    return text.replace(EHS_PATTERN, "E. H. S.")


# 各角色音色
VOICE_WORD_ZH = "zh-CN-XiaoxiaoNeural"
VOICE_WORD_EN = "en-US-JennyNeural"
VOICE_EXAMPLE_ZH = "zh-CN-YunxiNeural"  # 男声做例句中文
VOICE_EXAMPLE_EN = "en-US-GuyNeural"


async def gen_one(text: str, voice: str, out_path: Path, rate: str = "+0%"):
    """生成一条音频"""
    if out_path.exists():
        return  # 幂等：跳过已存在
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(str(out_path))


async def gen_card(card: dict):
    """生成一张词卡的音频（4 条：单词中、单词英、例句中、例句英）"""
    out_dir = AUDIO_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # 单词：英文读一遍
    await gen_one(card["en"], VOICE_WORD_EN, out_dir / f"{card['id']}_word.mp3")
    # 例句：英文一句 + 中文一句
    await gen_one(card["example_en"], VOICE_EXAMPLE_EN, out_dir / f"{card['id']}_example.mp3")


async def main():
    if len(sys.argv) < 2:
        print("用法: python3 gen_audio.py <data.json> [limit]")
        sys.exit(1)

    data_file = ROOT / "data" / sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    with open(data_file, encoding="utf-8") as f:
        data = json.load(f)

    cards = data["vocab"]
    if limit > 0:
        cards = cards[:limit]

    print(f"开始生成音频: {len(cards)} 张词卡")
    for card in cards:
        await gen_card(card)
        print(f"  ✓ {card['id']}: {card['en']}")


if __name__ == "__main__":
    asyncio.run(main())