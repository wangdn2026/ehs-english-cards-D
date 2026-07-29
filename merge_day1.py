#!/usr/bin/env python3
"""
合并 Day1 各 part 数据 → day1.json
- part1_medical.json：生活医疗 28 条
- part2_contractor_a.json：承包商核心名词 37 条
- part2_contractor_b.json：高频短语 15 + 核心动词 8 = 23 条
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"


def main():
    parts = ["day1_part1_medical.json", "day1_part2_contractor_a.json", "day1_part2_contractor_b.json"]
    merged = None
    total = 0
    for p in parts:
        with open(DATA_DIR / p, encoding="utf-8") as f:
            d = json.load(f)
        if merged is None:
            merged = {
                "package": d["package"],
                "day": d["day"],
                "title_zh": d["title_zh"],
                "title_en": d["title_en"],
                "vocab": [],
            }
        merged["vocab"].extend(d["vocab"])
        total += len(d["vocab"])
        print(f"  ✓ {p}: +{len(d['vocab'])} 条")

    # ID 唯一性校验
    ids = [v["id"] for v in merged["vocab"]]
    dup = [i for i in ids if ids.count(i) > 1]
    if dup:
        print(f"!! 重复 ID: {set(dup)}")
        return

    out = DATA_DIR / "day1.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 合并完成: {total} 条 → {out}")

    # 分类统计
    from collections import Counter
    cat = Counter(v["cat"] for v in merged["vocab"])
    sub = Counter((v["cat"], v["sub_cat"]) for v in merged["vocab"])
    print(f"\n分类统计:")
    for k, v in cat.items():
        print(f"  {k}: {v} 条")
    print(f"\n子分类:")
    for (c, s), n in sorted(sub.items()):
        print(f"  {c} / {s}: {n} 条")


if __name__ == "__main__":
    main()
