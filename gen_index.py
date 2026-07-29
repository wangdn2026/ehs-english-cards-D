#!/usr/bin/env python3
"""
生成 Day1 词卡目录页 index.html
- 按子分类分块展示所有词卡
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
INDEX_FILE = ROOT / "index.html"

# 子分类顺序（与原数据一致）
SUBCAT_ORDER = [
    ("生活医疗", "核心名词"),
    ("生活医疗", "高频动词/短语"),
    ("生活医疗", "常用固定短句"),
    ("承包商安全管理", "承包商分类"),
    ("承包商安全管理", "EHS体系/文件"),
    ("承包商安全管理", "安全审核考核"),
    ("承包商安全管理", "作业阶段术语"),
    ("承包商安全管理", "高频专业短语"),
    ("承包商安全管理", "核心动词"),
]


def main():
    with open(DATA_DIR / "day1.json", encoding="utf-8") as f:
        data = json.load(f)

    # 按子分类分组
    groups = defaultdict(list)
    for v in data["vocab"]:
        groups[(v["cat"], v["sub_cat"])].append(v)

    total = len(data["vocab"])

    # 渲染各子分类块
    sections = []
    for cat, sub in SUBCAT_ORDER:
        items = groups.get((cat, sub), [])
        if not items:
            continue
        cards_html = "\n".join(
            f'    <a href="day1/{v["id"]}.html"><div class="en">{v["en"]}</div><div class="zh">{v["zh"]} · {v["sub_cat"]}</div></a>'
            for v in items
        )
        sections.append(
            f'<div class="subsection">\n'
            f'  <h3>{cat} · {sub}<span class="count">{len(items)} 条</span></h3>\n'
            f'  <div class="vocab-grid">\n{cards_html}\n  </div>\n'
            f'</div>'
        )

    sections_html = "\n".join(sections)

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
.page-header {{
  text-align: center;
  margin-bottom: 32px;
}}
.pkg-badge {{
  display: inline-block;
  background: var(--primary);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
  letter-spacing: 1px;
  margin-bottom: 12px;
}}
.page-header h1 {{
  font-size: 28px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
}}
.page-header .subtitle {{
  font-size: 14px;
  color: var(--text-secondary);
}}
.day-section {{
  max-width: 1080px;
  margin: 0 auto 32px;
  background: #FFFFFF;
  border: 2px solid var(--primary);
  border-radius: 16px;
  padding: 24px 28px;
}}
.day-section h2 {{
  font-size: 20px;
  color: var(--primary);
  margin-bottom: 4px;
}}
.day-section .meta {{
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 18px;
}}
.subsection {{
  margin-bottom: 22px;
}}
.subsection:last-child {{
  margin-bottom: 0;
}}
.subsection h3 {{
  font-size: 14px;
  color: var(--ink);
  margin-bottom: 10px;
  padding-left: 8px;
  border-left: 3px solid var(--accent);
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.subsection h3 .count {{
  font-size: 12px;
  font-weight: 400;
  color: var(--text-secondary);
  margin-left: 8px;
}}
.vocab-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
}}
.vocab-grid a {{
  display: block;
  padding: 10px 12px;
  background: var(--bg-warm);
  border-radius: 8px;
  text-decoration: none;
  color: var(--ink);
  border: 1px solid var(--border);
  transition: transform 0.1s, border-color 0.2s;
}}
.vocab-grid a:hover {{
  border-color: var(--primary);
  transform: translateY(-2px);
}}
.vocab-grid .en {{
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
  word-break: break-word;
}}
.vocab-grid .zh {{
  font-size: 11px;
  color: var(--text-secondary);
  word-break: break-word;
}}
.brand-foot {{
  text-align: center;
  margin-top: 32px;
  font-size: 12px;
  color: var(--text-secondary);
  letter-spacing: 1px;
}}
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
  <div class="meta">{total} 条 · 生活医疗 + 承包商安全管理 · 点击进入单词卡</div>

{sections_html}

</div>

<div class="brand-foot">安全五点半 · E. H. S. 职场英语</div>

</body>
</html>
"""

    INDEX_FILE.write_text(html, encoding="utf-8")
    print(f"✓ index.html 已生成，共 {total} 条词卡，{len(sections)} 个子分类块")


if __name__ == "__main__":
    main()
