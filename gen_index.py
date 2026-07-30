#!/usr/bin/env python3
"""
生成 Day1 词卡目录页 index.html
- 按"使用场景/学习路径"分三档：初级 / 中级 / 高级
- 默认只展开初级，初级内只展开第一个子分类
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
INDEX_FILE = ROOT / "index.html"

LEVEL_MAP = {
    ("生活医疗", "核心名词"): "初级",
    ("承包商安全管理", "核心动词"): "初级",
    ("承包商安全管理", "承包商分类"): "中级",
    ("承包商安全管理", "作业阶段术语"): "中级",
    ("生活医疗", "高频动词/短语"): "中级",
    ("承包商安全管理", "EHS体系/文件"): "高级",
    ("承包商安全管理", "安全审核考核"): "高级",
    ("承包商安全管理", "高频专业短语"): "高级",
    ("生活医疗", "常用固定短句"): "高级",
}
LEVEL_ORDER = ["初级", "中级", "高级"]
LEVEL_DESC = {
    "初级": "每天都会用",
    "中级": "工作场景常用",
    "高级": "专业体系 · 正式表达",
}
LEVEL_COLOR = {
    "初级": "#5BA4B5",
    "中级": "#E8845C",
    "高级": "#4A4A52",
}

SUBCAT_ORDER = [
    ("生活医疗", "核心名词"),
    ("承包商安全管理", "核心动词"),
    ("承包商安全管理", "承包商分类"),
    ("承包商安全管理", "作业阶段术语"),
    ("生活医疗", "高频动词/短语"),
    ("承包商安全管理", "EHS体系/文件"),
    ("承包商安全管理", "安全审核考核"),
    ("承包商安全管理", "高频专业短语"),
    ("生活医疗", "常用固定短句"),
]


def main():
    with open(DATA_DIR / "day1.json", encoding="utf-8") as f:
        data = json.load(f)

    sub_groups = defaultdict(list)
    for v in data["vocab"]:
        sub_groups[(v["cat"], v["sub_cat"])].append(v)

    level_groups = {lv: defaultdict(list) for lv in LEVEL_ORDER}
    for sub_key, items in sub_groups.items():
        lv = LEVEL_MAP.get(sub_key)
        if lv is None:
            continue
        level_groups[lv][sub_key] = items

    level_blocks = []
    for li, lv in enumerate(LEVEL_ORDER):
        subs = level_groups[lv]
        total_lv = sum(len(v) for v in subs.values())
        if total_lv == 0:
            continue
        sub_blocks = []
        for si, sub_key in enumerate(SUBCAT_ORDER):
            if sub_key not in subs:
                continue
            items = subs[sub_key]
            cat, sub = sub_key
            cards_html = "\n".join(
                f'    <a href="day1/{v["id"]}.html"><div class="en">{v["en"]}</div><div class="zh">{v["zh"]}</div></a>'
                for v in items
            )
            is_default_open = (li == 0 and si == 0)
            open_attr = " open" if is_default_open else ""
            sub_blocks.append(
                f'    <details class="subsection"{open_attr}>\n'
                f'      <summary>{cat} · {sub}<span class="count">{len(items)} 条</span></summary>\n'
                f'      <div class="vocab-grid">\n{cards_html}\n      </div>\n'
                f'    </details>'
            )
        subs_html = "\n".join(sub_blocks)
        lv_open = " open" if li == 0 else ""
        lv_color = LEVEL_COLOR[lv]
        level_blocks.append(
            f'<details class="level" data-level="{lv}"{lv_open} style="--lv-color:{lv_color};">\n'
            f'  <summary><span class="lv-tag">{lv}</span><span class="lv-desc">{LEVEL_DESC[lv]}</span><span class="lv-count">{total_lv} 条</span></summary>\n'
            f'  <div class="level-body">\n{subs_html}\n  </div>\n'
            f'</details>'
        )

    levels_html = "\n".join(level_blocks)
    total = len(data["vocab"])
    total_subs = sum(len(subs) for subs in level_groups.values())

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EHS英语训练营 · D课包词卡</title>
<style>
:root {{
  --primary: #5BA4B5;
  --accent: #E8845C;
  --ink: #2C2C2C;
  --bg-warm: #FDF8F0;
  --bg-page: #F5F0E8;
  --text-secondary: #6A6A7A;
  --border: #E8E2DA;
}}
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg-page);
  font-family: 'PingFang SC', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Microsoft YaHei', sans-serif;
  min-height: 100vh;
  padding: 40px 20px 60px;
  color: var(--ink);
}}
.page-header {{ text-align: center; margin-bottom: 32px; }}
.pkg-badge {{
  display: inline-block; background: var(--primary); color: #fff;
  font-size: 12px; font-weight: 600; padding: 4px 12px;
  border-radius: 12px; letter-spacing: 1px; margin-bottom: 12px;
}}
.page-header h1 {{ font-size: 28px; font-weight: 700; color: var(--ink); margin-bottom: 8px; }}
.page-header .subtitle {{ font-size: 14px; color: var(--text-secondary); }}
.day-section {{
  max-width: 1080px; margin: 0 auto 32px; background: #FFFFFF;
  border: 2px solid var(--primary); border-radius: 16px; padding: 24px 28px;
}}
.day-section h2 {{ font-size: 20px; color: var(--primary); margin-bottom: 4px; }}
.day-section .meta {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 18px; }}
.level {{
  margin-bottom: 16px; border: 1px solid var(--border);
  border-left: 4px solid var(--lv-color); border-radius: 10px;
  background: #FAFCFC; overflow: hidden;
}}
.level:last-child {{ margin-bottom: 0; }}
.level summary {{
  font-size: 16px; font-weight: 600; color: var(--ink); padding: 14px 16px;
  cursor: pointer; list-style: none; display: flex; align-items: center; gap: 10px;
  transition: background 0.15s;
}}
.level summary::-webkit-details-marker {{ display: none; }}
.level summary::marker {{ display: none; }}
.level summary:hover {{ background: rgba(91, 164, 181, 0.06); }}
.level summary::after {{
  content: '▾'; font-size: 14px; color: var(--text-secondary);
  transition: transform 0.2s; margin-left: auto;
}}
.level[open] > summary {{ border-bottom: 1px solid var(--border); background: rgba(91, 164, 181, 0.04); }}
.level[open] > summary::after {{ transform: rotate(180deg); }}
.lv-tag {{
  display: inline-block; background: var(--lv-color); color: #fff;
  font-size: 13px; font-weight: 700; padding: 3px 10px; border-radius: 6px; letter-spacing: 1px;
}}
.lv-desc {{ font-size: 13px; font-weight: 400; color: var(--text-secondary); }}
.lv-count {{
  font-size: 12px; font-weight: 500; color: var(--text-secondary);
  background: rgba(74, 74, 82, 0.08); padding: 3px 10px; border-radius: 8px;
  margin-left: auto; margin-right: 8px;
}}
.level-body {{ padding: 12px 14px; }}
.subsection {{
  margin-bottom: 10px; border: 1px solid var(--border);
  border-radius: 8px; background: #fff; overflow: hidden;
}}
.subsection:last-child {{ margin-bottom: 0; }}
.subsection summary {{
  font-size: 13px; font-weight: 600; color: var(--ink); padding: 10px 12px;
  cursor: pointer; list-style: none; display: flex; align-items: center;
  justify-content: space-between; transition: background 0.15s;
}}
.subsection summary::-webkit-details-marker {{ display: none; }}
.subsection summary::marker {{ display: none; }}
.subsection summary:hover {{ background: rgba(91, 164, 181, 0.06); }}
.subsection summary::after {{
  content: '▾'; font-size: 11px; color: var(--text-secondary);
  transition: transform 0.2s; margin-left: 8px;
}}
.subsection[open] > summary {{ border-bottom: 1px solid var(--border); }}
.subsection[open] > summary::after {{ transform: rotate(180deg); }}
.subsection summary .count {{
  font-size: 11px; font-weight: 400; color: var(--text-secondary);
  background: rgba(91, 164, 181, 0.10); padding: 2px 8px; border-radius: 6px; margin-right: 8px;
}}
.subsection[open] .vocab-grid {{ padding: 10px; }}
.vocab-grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px;
}}
.vocab-grid a {{
  display: block; padding: 10px 12px; background: var(--bg-warm);
  border-radius: 8px; text-decoration: none; color: var(--ink);
  border: 1px solid var(--border); transition: transform 0.1s, border-color 0.2s;
}}
.vocab-grid a:hover {{ border-color: var(--primary); transform: translateY(-2px); }}
.vocab-grid .en {{ font-size: 14px; font-weight: 600; margin-bottom: 2px; word-break: break-word; }}
.vocab-grid .zh {{ font-size: 11px; color: var(--text-secondary); word-break: break-word; }}
.brand-foot {{ text-align: center; margin-top: 32px; font-size: 12px; color: var(--text-secondary); letter-spacing: 1px; }}
</style>
</head>
<body>

<div class="page-header">
  <span class="pkg-badge">PACKAGE D · EHS英语训练营</span>
  <h1>D 课包 · 每节课词卡</h1>
  <div class="subtitle">医院门诊 & 承包商安全管理 · 安全五点半出品</div>
</div>

<div class="day-section">
  <h2>Day 1 · 医院门诊 & 承包商安全管理（一）</h2>
  <div class="meta">{total} 条 · 共 3 档 {total_subs} 个分类 · 从初级开始学</div>

{levels_html}

</div>

<div class="brand-foot">安全五点半 · E. H. S. 职场英语</div>

</body>
</html>
"""

    INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"✓ index.html 已生成，共 {total} 条词卡，3 档 {total_subs} 个子分类")


if __name__ == "__main__":
    main()
