# EHS英语训练营 · D课包词卡

> 维护：烟头叔叔（主 agent）｜主人：冬妮（@wangdn2026）
> 配套课程：D 课包每节课（医院门诊 / 承包商安全管理 等场景）

## 课节索引

| 课节 | 主题 | 词条数 | 状态 | 上线时间 |
|---|---|---|---|---|
| Day1 | 医院门诊 & 承包商安全管理（一） | 88 | ✅ 已上线 | 2026-07-29 |

## 目录结构

```
├── README.md
├── index.html              # 总目录页（按子分类展示 Day1 全量词卡）
├── template.html            # HTML 卡片模板（string.Template）
├── generate.py              # JSON → HTML 词卡
├── gen_audio.py             # edge-tts 批量生成 mp3
├── gen_qr.py                # 1-bit 二维码生成
├── gen_index.py             # 总目录页生成
├── merge_day1.py            # Day1 数据合并脚本
├── data/
│   ├── day1.json                          # Day1 完整 88 条
│   ├── day1_part1_medical.json            # 生活医疗 28 条
│   ├── day1_part2_contractor_a.json       # 承包商核心名词 37 条
│   ├── day1_part2_contractor_b.json       # 承包商短语+动词 23 条
│   └── day1_sample.json                   # 样张数据 3 条
├── day1/
│   ├── d1_med_01.html … d1_med_s03.html   # 生活医疗 28 张
│   ├── d1_con_01.html … d1_con_37.html   # 承包商核心名词 37 张
│   ├── d1_con_p01.html … d1_con_p15.html # 高频专业短语 15 张
│   └── d1_con_v01.html … d1_con_v08.html # 核心动词 8 张
├── audio/
│   ├── d1_*_word.mp3                      # 单词英文发音
│   └── d1_*_example.mp3                   # 例句英文发音
└── img/
    └── d1_*_qr.png                        # 1-bit 二维码（指向 GitHub Pages URL）
```

## Day1 词卡分类

| 大类 | 子分类 | 条数 |
|---|---|---|
| 生活医疗 | 核心名词 | 17 |
| 生活医疗 | 高频动词/短语 | 8 |
| 生活医疗 | 常用固定短句 | 3 |
| 承包商安全管理 | 承包商分类 | 12 |
| 承包商安全管理 | EHS体系/文件 | 13 |
| 承包商安全管理 | 安全审核考核 | 8 |
| 承包商安全管理 | 作业阶段术语 | 4 |
| 承包商安全管理 | 高频专业短语 | 15 |
| 承包商安全管理 | 核心动词 | 8 |
| **合计** | | **88** |

## 词卡规范

- **音频**：edge-tts 生成 mp3（单词女声 en-US-JennyNeural、例句男声 en-US-GuyNeural），"EHS" 统一转写为 "E. H. S." 避免吞音
- **二维码**：1-bit 纯黑白 + 最近邻缩放，禁用抗锯齿导致模糊，发布前实扫验证
- **HTML 体积**：单页 < 50KB
- **部署**：GitHub Pages（main 分支 / 根目录，legacy 模式）
- **模板**：Python `string.Template` 渲染，CSS 变量通过占位符注入
- **导航**：每张卡片有"上一张 / 下一张"链接，首尾跳转 `../index.html`

## 关联仓库

- A/B/C 课包同系列词卡：`wangdn2026/ehs-english-cards`
- EHS英语训练营主页：<待补>

## 本地复跑命令

```bash
# 1. 合并 part 数据
python3 merge_day1.py

# 2. 批量生成音频（幂等，跳过已存在）
python3 gen_audio.py day1.json

# 3. 批量生成二维码
python3 gen_qr.py day1.json

# 4. 批量生成 HTML
python3 generate.py day1.json

# 5. 重生成总目录
python3 gen_index.py
```
