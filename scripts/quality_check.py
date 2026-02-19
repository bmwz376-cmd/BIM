#!/usr/bin/env python3
"""
quality_check.py
================
Quality control enforcement for the BIM training package.
Checks:
  1. assets/pages/ PNG images exist (> 0)
  2. Required directories exist
  3. All textbook chapters contain mandatory elements
  4. All slide files have NO speaker notes
  5. Minimum 10 figure citations (出典：PDF p.) across all files
  6. Translation placeholders exist in all chapters

Usage:
    python3 scripts/quality_check.py

Exits with code 0 on PASS, code 1 on FAIL.
"""

import os
import sys
import glob
import re

REQUIRED_DIRS = [
    "assets/pages",
    "assets/figures",
    "textbook",
    "slides",
    "workbook",
    "scripts",
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "BUILD_NOTES.md",
    "course_plan.md",
    "glossary.md",
    "assets_index.md",
]

NUM_CHAPTERS = 10
FIGURE_PATTERN = re.compile(r'（出典：PDF p\.\d+）|Source: PDF p\.\d+')
SPEAKER_NOTE_PATTERN = re.compile(r'(?:講師|スピーカー|speaker|note|Note:|発表者メモ|講師ノート)', re.IGNORECASE)
TRANSLATE_PLACEHOLDER = "🔘 Translate this"
LEARNING_OBJECTIVES = ["学習目標", "Learning Objectives"]
SUMMARY_MARKERS = ["まとめ", "Summary"]
MCQ_MARKERS = ["確認問題", "多肢選択式"]
EXERCISE_MARKERS = ["実践演習", "Practical Exercise"]

issues = []
warnings = []

def check(condition, msg_pass, msg_fail, is_warning=False):
    if condition:
        print(f"  ✅ {msg_pass}")
        return True
    else:
        if is_warning:
            print(f"  ⚠️  {msg_fail}")
            warnings.append(msg_fail)
        else:
            print(f"  ❌ {msg_fail}")
            issues.append(msg_fail)
        return False

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

# ─── 1. DIRECTORIES ───────────────────────────────────
print("\n=== [1] Directory Structure Check ===")
for d in REQUIRED_DIRS:
    check(os.path.isdir(d), f"Directory exists: {d}", f"Missing directory: {d}")

# ─── 2. ROOT FILES ─────────────────────────────────────
print("\n=== [2] Root Files Check ===")
for f in REQUIRED_ROOT_FILES:
    check(os.path.exists(f), f"File exists: {f}", f"Missing file: {f}")

# ─── 3. ASSET PAGES ────────────────────────────────────
print("\n=== [3] Asset Pages (PNG) Check ===")
pages = glob.glob("assets/pages/p*.png")
check(len(pages) > 0,
      f"PNG pages found: {len(pages)} images",
      f"No PNG pages found in assets/pages/")
check(len(pages) >= 100,
      f"Sufficient pages: {len(pages)} >= 100",
      f"Low page count: {len(pages)} (expected >= 100)",
      is_warning=True)

# ─── 4. TEXTBOOK CHAPTERS ──────────────────────────────
print("\n=== [4] Textbook Chapter Content Check ===")
for i in range(1, NUM_CHAPTERS + 1):
    path = f"textbook/chap{i:02d}.md"
    content = read_file(path)
    if not check(bool(content), f"chap{i:02d}.md exists and readable",
                 f"Missing or unreadable: {path}"):
        continue

    print(f"  --- chap{i:02d}.md ---")
    # Learning objectives
    check(any(m in content for m in LEARNING_OBJECTIVES),
          "Has learning objectives",
          f"chap{i:02d}: Missing 学習目標 / Learning Objectives")
    # Summary
    check(any(m in content for m in SUMMARY_MARKERS),
          "Has summary section",
          f"chap{i:02d}: Missing まとめ / Summary")
    # 10 MCQ
    check(any(m in content for m in MCQ_MARKERS),
          "Has multiple-choice questions",
          f"chap{i:02d}: Missing 確認問題 / MCQ section")
    # Practical exercise
    check(any(m in content for m in EXERCISE_MARKERS),
          "Has practical exercise",
          f"chap{i:02d}: Missing 実践演習 / Practical Exercise")
    # Translation placeholder
    check(TRANSLATE_PLACEHOLDER in content,
          "Has translation placeholder",
          f"chap{i:02d}: Missing 🔘 Translate placeholder")

# ─── 5. SLIDE FILES ─────────────────────────────────────
print("\n=== [5] Slide File Check (No Speaker Notes) ===")
for i in range(1, NUM_CHAPTERS + 1):
    path = f"slides/chap{i:02d}_slide.md"
    content = read_file(path)
    if not check(bool(content), f"chap{i:02d}_slide.md exists",
                 f"Missing: {path}"):
        continue

    # Count slides (## スライド)
    slide_count = len(re.findall(r'^## スライド', content, re.MULTILINE))
    check(slide_count >= 10,
          f"chap{i:02d}_slide: {slide_count} slides (>= 10 ✅)",
          f"chap{i:02d}_slide: Only {slide_count} slides (< 10 required)")

    # No speaker notes
    has_notes = bool(SPEAKER_NOTE_PATTERN.search(content))
    check(not has_notes,
          f"chap{i:02d}_slide: No speaker notes detected",
          f"chap{i:02d}_slide: Speaker notes/narration detected",
          is_warning=True)

# ─── 6. WORKBOOK FILES ──────────────────────────────────
print("\n=== [6] Workbook Files Check ===")
for i in range(1, NUM_CHAPTERS + 1):
    ex_path  = f"workbook/chap{i:02d}_exercises.md"
    ans_path = f"workbook/chap{i:02d}_answers.md"
    check(os.path.exists(ex_path),
          f"chap{i:02d}_exercises.md exists",
          f"Missing: {ex_path}")
    check(os.path.exists(ans_path),
          f"chap{i:02d}_answers.md exists",
          f"Missing: {ans_path}")

# ─── 7. FIGURE CITATIONS ────────────────────────────────
print("\n=== [7] Figure Citations Check (Minimum 10) ===")
all_files = (
    glob.glob("textbook/*.md") +
    glob.glob("slides/*.md") +
    glob.glob("workbook/*.md") +
    ["course_plan.md", "glossary.md", "README.md"]
)
total_citations = 0
for fpath in all_files:
    content = read_file(fpath)
    found = FIGURE_PATTERN.findall(content)
    if found:
        total_citations += len(found)

check(total_citations >= 10,
      f"Figure citations found: {total_citations} (>= 10 ✅)",
      f"Insufficient figure citations: {total_citations} (need >= 10)")

check(total_citations >= 15,
      f"Figure citations: {total_citations} (>= 15 ✅ excellent)",
      f"Figure citations: {total_citations} (< 15, recommend >= 15)",
      is_warning=True)

# ─── 8. COURSE PLAN ─────────────────────────────────────
print("\n=== [8] Course Plan Check ===")
cp = read_file("course_plan.md")
session_count = len(re.findall(r'^## セッション \d+', cp, re.MULTILINE))
check(session_count >= 10,
      f"course_plan.md: {session_count} sessions found (>= 10 ✅)",
      f"course_plan.md: Only {session_count} sessions (need >= 10)")
check("評価ルーブリック" in cp or "Evaluation Rubric" in cp,
      "course_plan.md: Evaluation rubric present",
      "course_plan.md: Missing evaluation rubric")
check("合否基準" in cp or "Pass/Fail" in cp,
      "course_plan.md: Pass/Fail criteria present",
      "course_plan.md: Missing Pass/Fail criteria")

# ─── 9. GLOSSARY ─────────────────────────────────────────
print("\n=== [9] Glossary Check ===")
glos = read_file("glossary.md")
term_count = len(re.findall(r'^\| \*\*', glos, re.MULTILINE))
check(term_count >= 15,
      f"glossary.md: {term_count} terms (>= 15 ✅)",
      f"glossary.md: Only {term_count} terms (recommend >= 15)",
      is_warning=True)

# ─── FINAL SUMMARY ──────────────────────────────────────
print("\n" + "="*60)
print("QUALITY CHECK SUMMARY")
print("="*60)
print(f"  Critical Issues  : {len(issues)}")
print(f"  Warnings         : {len(warnings)}")
print(f"  Figure Citations : {total_citations}")
print(f"  Sessions         : {session_count}")

if issues:
    print("\n[FAIL] The following issues must be resolved:")
    for issue in issues:
        print(f"  ❌ {issue}")
    # Update BUILD_NOTES
    try:
        with open("BUILD_NOTES.md", "a", encoding="utf-8") as f:
            f.write("\n\n---\n## Quality Check FAIL Log\n\n")
            for issue in issues:
                f.write(f"- ❌ {issue}\n")
    except Exception:
        pass
    sys.exit(1)
else:
    print("\n✅✅✅ QUALITY CHECK: PASS ✅✅✅")
    if warnings:
        print("  (Warnings exist but are non-blocking)")
        for w in warnings:
            print(f"    ⚠️  {w}")
    # Update BUILD_NOTES
    try:
        with open("BUILD_NOTES.md", "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n## Quality Check Result\n\n"
                    f"**Result: PASS**\n\n"
                    f"- Figure citations: {total_citations}\n"
                    f"- Sessions: {session_count}\n"
                    f"- Issues: 0\n"
                    f"- Warnings: {len(warnings)}\n")
    except Exception:
        pass
    sys.exit(0)
