#!/usr/bin/env python3
"""
QA Audit Script — BIM Training Package
Generates QA_REPORT.md with PASS/FAIL per rule.
"""
import os, re, datetime

REPO = '/home/user/webapp'
issues = []   # (severity, rule_id, file_path, line_no, message)
passes = []   # (rule_id, message)

def fail(severity, rule, path, line, msg):
    issues.append((severity, rule, path, line, msg))

def ok(rule, msg):
    passes.append((rule, msg))


# ══════════════════════════════════════════════
# RULE 1 — File inventory
# ══════════════════════════════════════════════
required_files = (
    ['README.md', 'BUILD_NOTES.md', 'course_plan.md', 'glossary.md', 'assets_index.md'] +
    [f'textbook/chap{i:02d}.md'           for i in range(1, 11)] +
    [f'slides/chap{i:02d}_slide.md'       for i in range(1, 11)] +
    [f'workbook/chap{i:02d}_exercises.md' for i in range(1, 11)] +
    [f'workbook/chap{i:02d}_answers.md'   for i in range(1, 11)]
)
for f in required_files:
    if os.path.exists(os.path.join(REPO, f)):
        ok('R1_FILE_EXISTS', f)
    else:
        fail('CRITICAL', 'R1_FILE_MISSING', f, 0, 'Required file does not exist')


# ══════════════════════════════════════════════
# RULE 2 — Textbook chapter checks (chap01–10)
# ══════════════════════════════════════════════
TB_REQUIRED_SECTIONS = [
    'この章で理解すべきこと',
    '要点まとめ',
    '確認問題',
    '演習課題',
    'Translate this chapter',
]

for i in range(1, 11):
    path = f'textbook/chap{i:02d}.md'
    full = os.path.join(REPO, path)
    if not os.path.exists(full):
        continue
    txt  = open(full, encoding='utf-8').read()
    lines = txt.splitlines()

    for section in TB_REQUIRED_SECTIONS:
        if section in txt:
            ok('R2_TB_SECTION', f'{path}: "{section}" present')
        else:
            ln = 0
            fail('HIGH', 'R2_TB_SECTION_MISSING', path, ln,
                 f'Required section missing: {section}')

    # MCQ count — **問N. pattern
    mcqs = re.findall(r'\*\*問\d+\.', txt)
    if len(mcqs) >= 10:
        ok('R2_MCQ_COUNT', f'{path}: {len(mcqs)} MCQs found')
    else:
        fail('HIGH', 'R2_INSUFFICIENT_MCQ', path, 0,
             f'Only {len(mcqs)}/10 MCQs found')

    # Figure citations
    fig_count = txt.count('（出典：PDF p.')
    if fig_count >= 2:
        ok('R2_FIGURES', f'{path}: {fig_count} figure citations')
    else:
        fail('HIGH', 'R2_FEW_FIGURES', path, 0,
             f'Only {fig_count} figure citations (need ≥2)')

    # Figure template completeness: each 【図表:...】 block must have ①②③④
    for m in re.finditer(r'【図表：(.+?)】', txt):
        blk_start = m.start()
        blk = txt[blk_start:blk_start + 600]
        title = m.group(1)
        missing = [tag for tag in ['① 図の説明：','② 読み取り方：','③ 教育上の狙い：','④ 実務活用シーン：']
                   if tag not in blk]
        ln = txt[:blk_start].count('\n') + 1
        if missing:
            fail('MEDIUM', 'R2_FIG_TEMPLATE', path, ln,
                 f'Figure "{title[:30]}" missing tags: {missing}')
        else:
            ok('R2_FIG_TEMPLATE', f'{path} ln{ln}: figure template complete')

    # だ・である調 check — flag lines ending with です。or ます。
    dm_lines = []
    for ln_no, ln in enumerate(lines, 1):
        if ln.startswith(('#', '>', '-', '`', '|', '!')):
            continue
        if re.search(r'(?<![ないなくなけれ])です。|(?<![いくさ])ます。', ln):
            dm_lines.append(ln_no)
    if dm_lines:
        fail('MEDIUM', 'R2_DESU_MASU', path, dm_lines[0],
             f'Possible desu/masu at lines: {dm_lines[:5]}')
    else:
        ok('R2_DESU_MASU', f'{path}: no desu/masu violations detected')


# ══════════════════════════════════════════════
# RULE 3 — Slide checks
# ══════════════════════════════════════════════
for i in range(1, 11):
    path = f'slides/chap{i:02d}_slide.md'
    full = os.path.join(REPO, path)
    if not os.path.exists(full):
        continue
    txt  = open(full, encoding='utf-8').read()
    lines = txt.splitlines()

    prose_lines = []
    for ln_no, ln in enumerate(lines, 1):
        if (len(ln) > 80
                and not ln.startswith(('#', '-', '!', '（出典', '|', '>', '`', ' '))
                and ln.strip() not in ('---', '')
                and not ln.strip().startswith('**')):
            prose_lines.append((ln_no, ln[:60]))

    if prose_lines:
        fail('HIGH', 'R3_SLIDE_PROSE', path, prose_lines[0][0],
             f'{len(prose_lines)} long-prose lines found (first: ln{prose_lines[0][0]})')
    else:
        ok('R3_SLIDE_PROSE', f'{path}: no long prose violations')

    fig_count = txt.count('（出典：PDF p.')
    if fig_count >= 2:
        ok('R3_SLIDE_FIGURES', f'{path}: {fig_count} figure citations')
    else:
        fail('MEDIUM', 'R3_SLIDE_FEW_FIGURES', path, 0,
             f'Only {fig_count} figure citations (recommend ≥2)')


# ══════════════════════════════════════════════
# RULE 4 — Workbook checks
# ══════════════════════════════════════════════
for i in range(1, 11):
    for kind in ['exercises', 'answers']:
        path = f'workbook/chap{i:02d}_{kind}.md'
        full = os.path.join(REPO, path)
        if not os.path.exists(full):
            continue
        txt = open(full, encoding='utf-8').read()
        if len(txt) >= 500:
            ok('R4_WORKBOOK_SIZE', f'{path}: {len(txt)} chars')
        else:
            fail('HIGH', 'R4_THIN_WORKBOOK', path, 0,
                 f'File too thin: {len(txt)} chars (< 500)')
        if '対応章' in txt or '対応演習' in txt:
            ok('R4_WORKBOOK_LINK', f'{path}: chapter link present')
        else:
            fail('MEDIUM', 'R4_NO_CHAPTER_LINK', path, 0,
                 'Missing chapter back-link (対応章 / 対応演習)')


# ══════════════════════════════════════════════
# RULE 5 — Course plan checks
# ══════════════════════════════════════════════
cp_path = 'course_plan.md'
cp = open(os.path.join(REPO, cp_path), encoding='utf-8').read()

session_count = len(re.findall(r'## セッション\s*\d+', cp))
if session_count >= 10:
    ok('R5_SESSION_COUNT', f'course_plan.md: {session_count} sessions defined')
else:
    fail('CRITICAL', 'R5_SESSION_COUNT', cp_path, 0,
         f'Only {session_count}/10 sessions defined')

for req in ['最終到達度定義', '評価ルーブリック', '合否基準']:
    if req in cp:
        ok('R5_COURSE_SECTION', f'course_plan.md: "{req}" present')
    else:
        fail('HIGH', 'R5_COURSE_SECTION_MISSING', cp_path, 0,
             f'Missing required section: {req}')

for i in range(1, 11):
    pat = rf'## セッション\s*{i}.*?(?=## セッション|\Z)'
    m = re.search(pat, cp, re.DOTALL)
    if not m:
        fail('HIGH', 'R5_SESSION_MISSING', cp_path, 0, f'Session {i} block not found')
        continue
    block = m.group()
    for field in ['学習目標', '演習内容', '宿題', '期待される到達レベル', '使用図表']:
        if field in block:
            ok('R5_SESSION_FIELD', f'Session {i}: {field} present')
        else:
            fail('MEDIUM', 'R5_SESSION_FIELD_MISSING', cp_path, 0,
                 f'Session {i} missing field: {field}')


# ══════════════════════════════════════════════
# RULE 6 — Global figure citation count (≥10)
# ══════════════════════════════════════════════
total_figs = 0
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'assets']]
    for f in files:
        if f.endswith('.md'):
            total_figs += open(os.path.join(root, f),
                               encoding='utf-8').read().count('（出典：PDF p.')
if total_figs >= 10:
    ok('R6_GLOBAL_FIGURES', f'Total figure citations across repo: {total_figs} (≥10 required)')
else:
    fail('CRITICAL', 'R6_GLOBAL_FIGURES', '(all .md files)', 0,
         f'Only {total_figs} figure citations (need ≥10)')


# ══════════════════════════════════════════════
# Build QA_REPORT.md
# ══════════════════════════════════════════════
SEVERITIES = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
sev_counts = {s: sum(1 for x in issues if x[0] == s) for s in SEVERITIES}
total_issues = len(issues)
overall = 'PASS ✅' if total_issues == 0 else f'FAIL ❌  ({total_issues} issues)'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
report_lines = [
    f'# QA Report — 建築・BIM研修パッケージ',
    f'',
    f'**Generated:** {now}  ',
    f'**Overall Result:** {overall}  ',
    f'',
    f'---',
    f'',
    f'## Summary',
    f'',
    f'| Severity | Count |',
    f'|----------|-------|',
]
for s in SEVERITIES:
    report_lines.append(f'| {s} | {sev_counts[s]} |')
report_lines += [
    f'| **PASS** | **{len(passes)}** |',
    f'',
    f'---',
    f'',
]

if issues:
    report_lines.append('## Issues (sorted by severity)\n')
    for sev in SEVERITIES:
        grp = [(r, p, l, m) for sv, r, p, l, m in issues if sv == sev]
        if not grp:
            continue
        report_lines.append(f'### {sev}\n')
        for rule, path, ln, msg in grp:
            ln_str = f'L{ln}' if ln else '—'
            report_lines.append(f'- **[{rule}]** `{path}` ({ln_str}): {msg}')
        report_lines.append('')
else:
    report_lines.append('## Issues\n\n_None — all rules passed._\n')

report_lines += [
    '---',
    '',
    '## Passes\n',
]
for rule, msg in passes:
    report_lines.append(f'- ✅ [{rule}] {msg}')

report_lines += [
    '',
    '---',
    '',
    '## Rule Definitions',
    '',
    '| ID | Description |',
    '|----|-------------|',
    '| R1 | Required file inventory (45 files) |',
    '| R2 | Textbook chapter requirements (sections, MCQs, figures, style) |',
    '| R3 | Slide requirements (bullet-only, no prose, figure citations) |',
    '| R4 | Workbook size and chapter link |',
    '| R5 | Course plan: 10 sessions, required fields, rubric, pass criteria |',
    '| R6 | Global figure citation count ≥ 10 |',
]

report_path = os.path.join(REPO, 'QA_REPORT.md')
open(report_path, 'w', encoding='utf-8').write('\n'.join(report_lines) + '\n')
print(f'QA_REPORT.md written: {report_path}')
print(f'Overall: {overall}')
print(f'Issues:  {total_issues}  (CRITICAL={sev_counts["CRITICAL"]} HIGH={sev_counts["HIGH"]} MEDIUM={sev_counts["MEDIUM"]})')
print(f'Passes:  {len(passes)}')
if issues:
    print('\nTop issues:')
    for sev, rule, path, ln, msg in sorted(issues, key=lambda x: SEVERITIES.index(x[0]))[:20]:
        print(f'  [{sev}] {rule} | {path} | {msg}')
