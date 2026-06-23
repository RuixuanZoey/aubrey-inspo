#!/usr/bin/env python3
"""将飞书导出数据导入 AubreyInspo 网站"""
import csv
import zipfile
import os
import shutil
import re

CSV_PATH = "/Users/zhaoruixuan/Downloads/PPT风格&模板小抄本_模板收集表.csv"
ZIP_PATH = "/Users/zhaoruixuan/Downloads/PPT风格&模板小抄本_模板收集表_附件.zip"
IMAGES_DIR = "/Users/zhaoruixuan/WorkBuddy/2026-06-23-13-50-26/aubrey-inspo/public/images/inspirations"
CONTENT_DIR = "/Users/zhaoruixuan/WorkBuddy/2026-06-23-13-50-26/aubrey-inspo/src/content/inspirations"

# 清理旧示例文件
for f in os.listdir(CONTENT_DIR):
    if f.startswith("example-"):
        os.remove(os.path.join(CONTENT_DIR, f))

# 色系名称规范化
COLOR_MAP = {
    "黑/灰色": "黑灰",
    "紫色": "紫",
    "绿色": "绿",
    "蓝色": "蓝",
    "黄色": "黄",
    "橙色": "橙",
    "粉色": "粉",
}

def normalize_color(raw):
    """取第一个色系并规范化名称"""
    if not raw:
        return "其他"
    first = raw.split(",")[0].strip()
    return COLOR_MAP.get(first, first)

def normalize_layout(raw):
    """简化板式名称（去掉数字后缀）"""
    if not raw:
        return "其他"
    first = raw.split(",")[0].strip()
    # 去掉数字后缀：并列关系-3 → 并列关系
    first = re.sub(r'-\d+.*$', '', first)
    first = re.sub(r'-4以上$', '', first)
    return first

def slugify(text):
    """生成文件名安全的 slug"""
    return re.sub(r'[^\w\-]', '-', text).strip('-')[:50]

# 1. 解压图片
print("📦 解压图片...")
with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    names = sorted(z.namelist())
    for i, name in enumerate(names):
        new_name = f"flybook-{i+1:03d}.png"
        new_path = os.path.join(IMAGES_DIR, new_name)
        with z.open(name) as src:
            with open(new_path, 'wb') as dst:
                shutil.copyfileobj(src, dst)
        print(f"  ✅ [{i+1}/63] {new_name}")

# 2. 读取 CSV 并生成 Markdown
print("\n📝 生成 Markdown 文件...")
with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"  共 {len(rows)} 条数据")

for i, row in enumerate(rows):
    style = row.get('风格', '').strip()
    color_raw = row.get('色系', '').strip()
    layout_raw = row.get('板式', '').strip()
    
    color = normalize_color(color_raw)
    layout = normalize_layout(layout_raw)
    
    # 生成图片路径
    image = f"/images/inspirations/flybook-{i+1:03d}.png"
    
    # 标题：风格 + 色系 + 板式
    title = f"{style}·{color}·{layout}"
    
    # 备注：保留原始多标签信息
    parts = []
    if ',' in color_raw:
        parts.append(f"色系: {color_raw}")
    if ',' in layout_raw:
        parts.append(f"板式: {layout_raw}")
    note = "; ".join(parts) if parts else f"飞书导入 #{i+1}"
    
    # 生成 Markdown
    slug = slugify(f"{style}-{color}-{layout}-{i+1}")
    md_content = f"""---
title: "{title}"
image: "{image}"
style: "{style}"
colorScheme: "{color}"
layout: "{layout}"
note: "{note}"
source: ""
createdAt: 2026-06-23T00:00:00.000Z
---

{title}
"""
    md_path = os.path.join(CONTENT_DIR, f"flybook-{i+1:03d}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

print(f"\n  ✅ 生成了 {len(rows)} 个 Markdown 文件")

# 3. 统计标签分布
print("\n📊 标签统计:")
from collections import Counter
styles = Counter(row.get('风格', '').strip() for row in rows)
colors = Counter(normalize_color(row.get('色系', '').strip()) for row in rows)
layouts = Counter(normalize_layout(row.get('板式', '').strip()) for row in rows)

print(f"  风格: {dict(styles)}")
print(f"  色系: {dict(colors)}")
print(f"  板式: {dict(layouts)}")

print("\n🎉 导入完成！")
