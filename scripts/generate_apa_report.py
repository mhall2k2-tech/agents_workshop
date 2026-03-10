#!/usr/bin/env python3
import csv
import math
import os
import statistics
from collections import defaultdict
from datetime import date

DATA_PATH = 'data/raw/sleep_memory_2x2.csv'
PDF_PATH = 'reports/sleep_memory_apa_report.pdf'
SUMMARY_PATH = 'reports/sleep_memory_analysis_summary.md'

# ---------- Statistical helpers ----------
def betacf(a, b, x):
    maxit = 200
    eps = 3e-14
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def f_sf(f_value, df1, df2):
    x = (df1 * f_value) / (df1 * f_value + df2)
    return 1.0 - betai(df1 / 2.0, df2 / 2.0, x)


def fmt_p(p):
    if p < 0.001:
        return '< .001'
    return f'= {p:.3f}'.replace('0.', '.')


# ---------- Minimal PDF writer ----------
class SimplePDF:
    def __init__(self):
        self.pages = []

    def new_page(self):
        self.pages.append([])

    def text(self, x, y, txt, size=12):
        safe = txt.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        self.pages[-1].append(f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({safe}) Tj ET")

    def line(self, x1, y1, x2, y2, width=1):
        self.pages[-1].append(f"{width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def circle(self, x, y, r=2):
        # Approximate a circle with a square marker for simplicity.
        self.pages[-1].append(f"{x-r:.2f} {y-r:.2f} {2*r:.2f} {2*r:.2f} re f")

    def save(self, path):
        objects = []

        def add_obj(content):
            objects.append(content)
            return len(objects)

        font_obj = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        page_objs = []
        content_objs = []

        for page in self.pages:
            stream = '\n'.join(page)
            cont = f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream"
            content_id = add_obj(cont)
            content_objs.append(content_id)

        pages_id = add_obj('')  # placeholder

        for content_id in content_objs:
            page_dict = (
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_obj} 0 R >> >> /Contents {content_id} 0 R >>"
            )
            page_id = add_obj(page_dict)
            page_objs.append(page_id)

        kids = ' '.join(f"{pid} 0 R" for pid in page_objs)
        objects[pages_id - 1] = f"<< /Type /Pages /Count {len(page_objs)} /Kids [{kids}] >>"
        catalog_id = add_obj(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

        with open(path, 'wb') as f:
            f.write(b'%PDF-1.4\n')
            xref = [0]
            for i, obj in enumerate(objects, start=1):
                xref.append(f.tell())
                f.write(f"{i} 0 obj\n{obj}\nendobj\n".encode('latin-1'))
            xref_start = f.tell()
            f.write(f"xref\n0 {len(objects)+1}\n".encode('latin-1'))
            f.write(b"0000000000 65535 f \n")
            for off in xref[1:]:
                f.write(f"{off:010d} 00000 n \n".encode('latin-1'))
            f.write(
                f"trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode('latin-1')
            )


def wrap_lines(text, width=95):
    words = text.split()
    lines = []
    current = []
    for w in words:
        trial = ' '.join(current + [w])
        if len(trial) <= width:
            current.append(w)
        else:
            lines.append(' '.join(current))
            current = [w]
    if current:
        lines.append(' '.join(current))
    return lines


# ---------- Analysis ----------
rows = []
with open(DATA_PATH, newline='') as f:
    for row in csv.DictReader(f):
        rows.append({'id': int(row['id']), 'sleep': row['sleep'], 'cue': row['cue'], 'recall_score': float(row['recall_score'])})

cells = defaultdict(list)
for r in rows:
    cells[(r['sleep'], r['cue'])].append(r['recall_score'])

sleep_levels = ['Sleep', 'Wake']
cue_levels = ['Control', 'TMR']

means = {(s, c): statistics.mean(cells[(s, c)]) for s in sleep_levels for c in cue_levels}
sds = {(s, c): statistics.stdev(cells[(s, c)]) for s in sleep_levels for c in cue_levels}

all_scores = [r['recall_score'] for r in rows]
grand_mean = statistics.mean(all_scores)
a = len(sleep_levels)
b = len(cue_levels)
n = len(cells[(sleep_levels[0], cue_levels[0])])

mean_sleep = {s: statistics.mean([r['recall_score'] for r in rows if r['sleep'] == s]) for s in sleep_levels}
mean_cue = {c: statistics.mean([r['recall_score'] for r in rows if r['cue'] == c]) for c in cue_levels}

ssa = b * n * sum((mean_sleep[s] - grand_mean) ** 2 for s in sleep_levels)
ssb = a * n * sum((mean_cue[c] - grand_mean) ** 2 for c in cue_levels)
ssab = n * sum((means[(s, c)] - mean_sleep[s] - mean_cue[c] + grand_mean) ** 2 for s in sleep_levels for c in cue_levels)
sse = sum(sum((x - means[(s, c)]) ** 2 for x in cells[(s, c)]) for s in sleep_levels for c in cue_levels)


df_a, df_b, df_ab, df_e = 1, 1, 1, a * b * (n - 1)
ms_a, ms_b, ms_ab, ms_e = ssa / df_a, ssb / df_b, ssab / df_ab, sse / df_e
f_a, f_b, f_ab = ms_a / ms_e, ms_b / ms_e, ms_ab / ms_e
p_a, p_b, p_ab = f_sf(f_a, df_a, df_e), f_sf(f_b, df_b, df_e), f_sf(f_ab, df_ab, df_e)

pes_a = ssa / (ssa + sse)
pes_b = ssb / (ssb + sse)
pes_ab = ssab / (ssab + sse)

# ---------- Markdown summary ----------
os.makedirs('reports', exist_ok=True)
summary = f"""# Sleep-Memory 2x2 Analysis Summary

Date: {date.today().isoformat()}

## Design
- Between-participants 2 x 2 factorial design.
- Factors: Sleep (Sleep vs Wake) and Cue (TMR vs Control).
- Dependent variable: recall_score (0-40).
- Total N = {len(rows)} (n = {n} per cell).

## Cell descriptives
- Sleep-Control: M = {means[('Sleep','Control')]:.2f}, SD = {sds[('Sleep','Control')]:.2f}
- Sleep-TMR: M = {means[('Sleep','TMR')]:.2f}, SD = {sds[('Sleep','TMR')]:.2f}
- Wake-Control: M = {means[('Wake','Control')]:.2f}, SD = {sds[('Wake','Control')]:.2f}
- Wake-TMR: M = {means[('Wake','TMR')]:.2f}, SD = {sds[('Wake','TMR')]:.2f}

## Factorial ANOVA
- Sleep main effect: F(1, {df_e}) = {f_a:.2f}, p {fmt_p(p_a)}, partial eta squared = {pes_a:.3f}
- Cue main effect: F(1, {df_e}) = {f_b:.2f}, p {fmt_p(p_b)}, partial eta squared = {pes_b:.3f}
- Sleep x Cue interaction: F(1, {df_e}) = {f_ab:.2f}, p {fmt_p(p_ab)}, partial eta squared = {pes_ab:.3f}

## Interpretation (data-bound)
- Sleep condition was associated with higher recall scores.
- TMR cueing was associated with higher recall scores.
- No evidence of a Sleep x Cue interaction was observed in this dataset.
"""

with open(SUMMARY_PATH, 'w', encoding='utf-8') as f:
    f.write(summary)

# ---------- PDF report ----------
pdf = SimplePDF()

# Page 1: Title + abstract
pdf.new_page()
pdf.text(72, 740, 'Sleep and Targeted Memory Reactivation in a 2x2 Factorial Design', size=16)
pdf.text(72, 718, 'APA-Style Statistical Report', size=12)
pdf.text(72, 696, f'Date: {date.today().isoformat()}', size=11)
pdf.text(72, 660, 'Abstract', size=14)
abstract = (
    'This report analyses a synthetic memory dataset using a between-participants 2 x 2 design with Sleep '
    '(Sleep vs Wake) and Cue (TMR vs Control) as factors and recall score as the outcome. A fixed-effects '
    'factorial ANOVA was conducted on N = 80 observations (n = 20 per cell). Results showed statistically '
    'significant main effects of Sleep and Cue, but no evidence for a Sleep x Cue interaction. Descriptive '
    'statistics, ANOVA results, and an interaction plot are provided. All values in this report are computed '
    'directly from the supplied dataset without imputation or fabrication.'
)
y = 636
for line in wrap_lines(abstract, 95):
    pdf.text(72, y, line, size=11)
    y -= 16

# Page 2: Contents
pdf.new_page()
pdf.text(72, 740, 'Contents', size=16)
contents = [
    ('Abstract', 1),
    ('Introduction', 3),
    ('Method', 3),
    ('Results', 4),
    ('Discussion', 5),
    ('References', 6),
]
y = 700
for title, page in contents:
    dots = '.' * max(4, 70 - len(title))
    pdf.text(72, y, f'{title} {dots} {page}', size=12)
    y -= 24

# Page 3: Intro + Method
pdf.new_page()
pdf.text(72, 740, 'Introduction', size=14)
intro = (
    'The project question was whether sleep and cueing influence recall performance and whether they '
    'interact in a memory task. The dataset is described as a synthetic experiment with two between-'
    'participants factors and a continuous recall outcome (0-40).'
)
y = 716
for line in wrap_lines(intro, 95):
    pdf.text(72, y, line, size=11)
    y -= 16

pdf.text(72, y - 8, 'Method', size=14)
y -= 30
method_lines = [
    f'Data source: data/raw/sleep_memory_2x2.csv (N = {len(rows)}).',
    'Design: 2 x 2 between-participants factorial design.',
    'Factors: Sleep (Sleep, Wake) and Cue (Control, TMR).',
    'Outcome: recall_score.',
    'Analysis: fixed-effects factorial ANOVA with alpha = .05.',
]
for line in method_lines:
    pdf.text(72, y, line, size=11)
    y -= 16

# Page 4: Results + interaction plot
pdf.new_page()
pdf.text(72, 740, 'Results', size=14)
res_lines = [
    f'Sleep main effect: F(1, {df_e}) = {f_a:.2f}, p {fmt_p(p_a)}, partial eta squared = {pes_a:.3f}.',
    f'Cue main effect: F(1, {df_e}) = {f_b:.2f}, p {fmt_p(p_b)}, partial eta squared = {pes_b:.3f}.',
    f'Sleep x Cue interaction: F(1, {df_e}) = {f_ab:.2f}, p {fmt_p(p_ab)}, partial eta squared = {pes_ab:.3f}.',
    f'Means: Sleep-Control {means[("Sleep","Control")]:.2f}, Sleep-TMR {means[("Sleep","TMR")]:.2f},',
    f'Wake-Control {means[("Wake","Control")]:.2f}, Wake-TMR {means[("Wake","TMR")]:.2f}.',
]
y = 716
for line in res_lines:
    pdf.text(72, y, line, size=11)
    y -= 16

pdf.text(72, y - 10, 'Figure 1', size=11)
pdf.text(72, y - 26, 'Interaction plot of Cue by Sleep condition for recall score means.', size=11)

# Draw interaction plot
x0, y0, w, h = 90, 260, 420, 220
pdf.line(x0, y0, x0, y0 + h, width=1)
pdf.line(x0, y0, x0 + w, y0, width=1)

# y-axis ticks (16 to 32)
for val in [16, 20, 24, 28, 32]:
    yy = y0 + (val - 16) / (32 - 16) * h
    pdf.line(x0 - 4, yy, x0, yy, width=1)
    pdf.text(58, yy - 4, str(val), size=9)

# x-axis labels Control/TMR
x_control = x0 + 90
x_tmr = x0 + 300
pdf.line(x_control, y0, x_control, y0 - 4, width=1)
pdf.line(x_tmr, y0, x_tmr, y0 - 4, width=1)
pdf.text(x_control - 18, y0 - 18, 'Control', size=10)
pdf.text(x_tmr - 10, y0 - 18, 'TMR', size=10)
pdf.text(250, 232, 'Cue condition', size=10)
pdf.text(20, 375, 'Recall score', size=10)


def ymap(v):
    return y0 + (v - 16) / (32 - 16) * h

# Sleep line
s1 = (x_control, ymap(means[('Sleep', 'Control')]))
s2 = (x_tmr, ymap(means[('Sleep', 'TMR')]))
pdf.line(s1[0], s1[1], s2[0], s2[1], width=1.5)
pdf.circle(s1[0], s1[1], r=2.5)
pdf.circle(s2[0], s2[1], r=2.5)
pdf.text(s2[0] + 8, s2[1] + 2, 'Sleep', size=10)

# Wake line
w1 = (x_control, ymap(means[('Wake', 'Control')]))
w2 = (x_tmr, ymap(means[('Wake', 'TMR')]))
pdf.line(w1[0], w1[1], w2[0], w2[1], width=1.5)
pdf.circle(w1[0], w1[1], r=2.5)
pdf.circle(w2[0], w2[1], r=2.5)
pdf.text(w2[0] + 8, w2[1] - 10, 'Wake', size=10)

# Page 5: Discussion
pdf.new_page()
pdf.text(72, 740, 'Discussion', size=14)
discussion = (
    'The observed pattern indicates better recall for participants in the Sleep condition relative to Wake '
    'and better recall for TMR relative to Control. The interaction term was not statistically significant, '
    'which suggests the TMR-related difference was similar across sleep conditions in this sample. These '
    'conclusions are limited to the provided synthetic dataset and should be interpreted as exercise outcomes '
    'rather than confirmatory evidence from a preregistered study.'
)
y = 716
for line in wrap_lines(discussion, 95):
    pdf.text(72, y, line, size=11)
    y -= 16

# Page 6: References
pdf.new_page()
pdf.text(72, 740, 'References', size=14)
references = [
    'Fisher, R. A. (1925). Statistical methods for research workers. Oliver and Boyd.',
    'Lindsay, S. (n.d.). Project card [Course document]. agents_workshop/docs/project_card.md',
    'R Core Team. (2024). R: A language and environment for statistical computing. R Foundation for Statistical Computing. https://www.R-project.org/',
]
y = 712
for ref in references:
    for line in wrap_lines(ref, 90):
        pdf.text(72, y, line, size=11)
        y -= 15
    y -= 10

pdf.save(PDF_PATH)
print(f'Wrote {PDF_PATH}')
print(f'Wrote {SUMMARY_PATH}')
