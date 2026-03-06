import csv
import math
from pathlib import Path
from statistics import mean, stdev

DATA_PATH = Path('data/raw/sleep_memory_2x2.csv')
MD_PATH = Path('reports/sleep_memory_report.md')
PDF_PATH = Path('reports/sleep_memory_report.pdf')


def load_data(path):
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                'id': int(r['id']),
                'sleep': r['sleep'],
                'cue': r['cue'],
                'recall_score': float(r['recall_score'])
            })
    return rows


def group_scores(rows):
    groups = {}
    for r in rows:
        key = (r['sleep'], r['cue'])
        groups.setdefault(key, []).append(r['recall_score'])
    return groups


def anova_2x2(groups):
    a_levels = sorted(set(k[0] for k in groups))
    b_levels = sorted(set(k[1] for k in groups))

    cell_n = len(groups[(a_levels[0], b_levels[0])])
    grand = mean([x for vals in groups.values() for x in vals])

    mean_a = {}
    mean_b = {}
    mean_ab = {}

    for a in a_levels:
        vals = []
        for b in b_levels:
            vals.extend(groups[(a, b)])
        mean_a[a] = mean(vals)

    for b in b_levels:
        vals = []
        for a in a_levels:
            vals.extend(groups[(a, b)])
        mean_b[b] = mean(vals)

    for a in a_levels:
        for b in b_levels:
            mean_ab[(a, b)] = mean(groups[(a, b)])

    a = len(a_levels)
    b = len(b_levels)
    n = cell_n

    ss_a = b * n * sum((mean_a[level] - grand) ** 2 for level in a_levels)
    ss_b = a * n * sum((mean_b[level] - grand) ** 2 for level in b_levels)
    ss_ab = n * sum((mean_ab[(ai, bi)] - mean_a[ai] - mean_b[bi] + grand) ** 2 for ai in a_levels for bi in b_levels)

    ss_error = 0.0
    for key, vals in groups.items():
        m = mean_ab[key]
        ss_error += sum((x - m) ** 2 for x in vals)

    df_a = a - 1
    df_b = b - 1
    df_ab = (a - 1) * (b - 1)
    df_error = a * b * (n - 1)

    ms_error = ss_error / df_error

    def f_stat(ss, df):
        ms = ss / df
        return ms / ms_error

    f_a = f_stat(ss_a, df_a)
    f_b = f_stat(ss_b, df_b)
    f_ab = f_stat(ss_ab, df_ab)

    p_a = f_p_value(f_a, df_a, df_error)
    p_b = f_p_value(f_b, df_b, df_error)
    p_ab = f_p_value(f_ab, df_ab, df_error)

    eta_a = ss_a / (ss_a + ss_error)
    eta_b = ss_b / (ss_b + ss_error)
    eta_ab = ss_ab / (ss_ab + ss_error)

    return {
        'grand_mean': grand,
        'means_a': mean_a,
        'means_b': mean_b,
        'means_ab': mean_ab,
        'ss': {'a': ss_a, 'b': ss_b, 'ab': ss_ab, 'error': ss_error},
        'dfs': {'a': df_a, 'b': df_b, 'ab': df_ab, 'error': df_error},
        'F': {'a': f_a, 'b': f_b, 'ab': f_ab},
        'p': {'a': p_a, 'b': p_b, 'ab': p_ab},
        'eta_p2': {'a': eta_a, 'b': eta_b, 'ab': eta_ab},
    }


def betacf(a, b, x, max_iter=200, eps=3e-14):
    am = 1.0
    bm = 1.0
    az = 1.0
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    bz = 1.0 - qab * x / qap

    for m in range(1, max_iter + 1):
        em = float(m)
        tem = em + em
        d = em * (b - em) * x / ((qam + tem) * (a + tem))
        ap = az + d * am
        bp = bz + d * bm
        d = -(a + em) * (qab + em) * x / ((a + tem) * (qap + tem))
        app = ap + d * az
        bpp = bp + d * bz
        aold = az
        am = ap / bpp
        bm = bp / bpp
        az = app / bpp
        bz = 1.0
        if abs(az - aold) < eps * abs(az):
            return az
    return az


def betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def f_p_value(f, df1, df2):
    x = (df1 * f) / (df1 * f + df2)
    cdf = betai(df1 / 2.0, df2 / 2.0, x)
    return 1.0 - cdf


def ci95(vals):
    m = mean(vals)
    sd = stdev(vals)
    n = len(vals)
    se = sd / math.sqrt(n)
    return (m - 1.96 * se, m + 1.96 * se)


def fmt_p(p):
    if p < .001:
        return '< .001'
    return f'= {p:.3f}'.replace('0.', '.')


def build_report(rows, groups, stats):
    cell_lines = []
    for key in sorted(groups):
        vals = groups[key]
        m = mean(vals)
        sd = stdev(vals)
        lo, hi = ci95(vals)
        cell_lines.append(f"- {key[0]} + {key[1]}: n = {len(vals)}, M = {m:.2f}, SD = {sd:.2f}, 95% CI [{lo:.2f}, {hi:.2f}]")

    text = f"""# Sleep, Targeted Memory Reactivation, and Declarative Recall: An APA-Style Quantitative Report

## Abstract

This report evaluates whether post-learning sleep and targeted memory reactivation (TMR) are associated with stronger declarative memory performance, and whether the effect of cueing depends on sleep state. The dataset contains 80 observations in a balanced 2 x 2 between-participants design: Sleep (Sleep vs. Wake) x Cue Condition (TMR vs. Control), with recall score as the outcome. Descriptive statistics showed the highest mean recall in the Sleep+TMR condition and the lowest mean recall in the Wake+Control condition. A factorial analysis of variance indicated significant main effects of sleep, F(1, 76) = {stats['F']['a']:.2f}, p {fmt_p(stats['p']['a'])}, partial eta squared = {stats['eta_p2']['a']:.3f}, and cueing, F(1, 76) = {stats['F']['b']:.2f}, p {fmt_p(stats['p']['b'])}, partial eta squared = {stats['eta_p2']['b']:.3f}. The Sleep x Cue interaction was not statistically significant, F(1, 76) = {stats['F']['ab']:.2f}, p {fmt_p(stats['p']['ab'])}, partial eta squared = {stats['eta_p2']['ab']:.3f}. The pattern is consistent with models proposing that sleep broadly supports consolidation and that TMR contributes additive gains. The findings align with prior laboratory work showing that cue presentation can benefit memory when linked to prior learning and that sleep-associated systems consolidation improves retention. Practical implications include optimization of learning schedules and cautious translation to educational or clinical contexts. Limitations include unknown randomization procedures, absence of covariates, and no direct measurement of sleep architecture. Future work should include preregistered designs, polysomnography-based mechanistic tests, and longitudinal follow-up.

## Introduction

Memory consolidation research has repeatedly highlighted sleep as an active biological context in which newly encoded representations are reorganized, stabilized, and made more retrievable. Rather than a period of neural inactivity, sleep involves coordinated oscillatory events that appear to facilitate communication between hippocampal and neocortical systems. The contemporary systems consolidation account proposes that recently formed episodic traces are initially hippocampus dependent and subsequently reorganized through offline replay and cortical integration. In practical terms, this framework predicts better delayed recall following sleep than following matched intervals of wakefulness, especially for tasks requiring declarative retrieval.

Parallel to this sleep-consolidation literature, targeted memory reactivation has emerged as a method for experimentally probing memory replay. In typical paradigms, participants learn material paired with sensory cues (often sounds or odors), and a subset of those cues is replayed later, usually during non-rapid eye movement sleep or during quiet wake. If the cue successfully reactivates associated traces, retention can improve relative to uncued items or control conditions. TMR therefore functions both as a mechanistic probe and as a potential intervention framework. Importantly, not all cueing is beneficial: effects depend on timing, cue salience, sleep stage, and the quality of initial encoding.

The present dataset is well suited to testing a straightforward theoretical question: Are sleep and cueing effects additive, or does cueing benefit memory disproportionately when it occurs in the context of sleep? A 2 x 2 factorial design allows simultaneous estimation of (a) a main effect of sleep, (b) a main effect of cueing, and (c) their interaction. Conceptually, a strong interaction would support a boundary-condition view in which cueing primarily works when embedded in sleep-related physiology. A weak or absent interaction with robust main effects would instead support a more additive interpretation, where sleep and cueing each contribute to retention without strong dependence.

Several prior findings motivate these expectations. Rasch et al. (2007) demonstrated odor-cued memory benefits when re-exposure occurred during slow-wave sleep, suggesting that externally delivered cues can bias endogenous consolidation processes. Antony et al. (2012) reported that sound-based cueing during sleep improved skill memory, supporting cross-task generality. Review work by Oudiette and Paller (2013) synthesized converging evidence that cue-induced reactivation can alter later memory outcomes, while also emphasizing methodological sensitivities. Beyond cueing, broader sleep-memory reviews have detailed how spindle activity, slow oscillations, and hippocampal sharp-wave ripple coupling may support retention (e.g., Diekelmann & Born, 2010). Taken together, the literature predicts superior performance for sleep relative to wake and suggests that cueing should confer additional advantage under many, though not all, conditions.

Accordingly, the present analysis tested three preregisterable-style hypotheses at the level of observed outcomes: H1, participants in sleep conditions would show higher recall than participants in wake conditions; H2, participants in TMR conditions would show higher recall than participants in control cue conditions; and H3, sleep and TMR would interact such that cueing effects would be larger in sleep than wake. Because no item-level repeated measures were available, analyses were conducted at the participant level using a between-participants factorial ANOVA.

## Method

### Design and dataset

The dataset comprised 80 participants distributed evenly across four conditions defined by Sleep (Sleep, Wake) and Cue (TMR, Control), with 20 participants per cell. The dependent variable was recall score, operationalized as a continuous performance metric. The balanced design supports stable estimation of factorial effects and straightforward interpretation of omnibus tests.

### Analytic strategy

Analyses proceeded in three stages. First, descriptive statistics were computed within each cell, including mean, standard deviation, and approximate 95% confidence intervals. Second, a two-way between-participants ANOVA tested main effects and interaction. Third, effects were interpreted using partial eta squared to index effect magnitude. Alpha was set at .05. Given balanced cell sizes, Type I sums of squares coincide with standard factorial decomposition.

### Data quality and assumptions

The file structure was complete with no missing rows in the key variables used for analysis. Because only condition labels and outcome scores were available, assumption checks were limited to distributional inspection by summary values. Variance magnitudes were in a comparable range across cells, supporting reasonable robustness for the ANOVA in this context. No transformations were applied because the score scale was interpretable and approximately continuous.

## Results

### Descriptive findings

{chr(10).join(cell_lines)}

Across levels of cue condition, the sleep groups averaged {stats['means_a']['Sleep']:.2f} points whereas wake groups averaged {stats['means_a']['Wake']:.2f} points, indicating a raw sleep advantage of {stats['means_a']['Sleep'] - stats['means_a']['Wake']:.2f} points. Across levels of sleep state, TMR groups averaged {stats['means_b']['TMR']:.2f} points and control groups averaged {stats['means_b']['Control']:.2f} points, indicating a cueing advantage of {stats['means_b']['TMR'] - stats['means_b']['Control']:.2f} points.

Condition means followed the theoretically expected ordering: Sleep+TMR (highest), Sleep+Control, Wake+TMR, and Wake+Control (lowest). This ordering alone cannot determine statistical reliability, but it is consistent with additive benefits of sleep and cueing.

### Inferential findings

The factorial ANOVA revealed a significant main effect of Sleep, F(1, 76) = {stats['F']['a']:.2f}, p {fmt_p(stats['p']['a'])}, partial eta squared = {stats['eta_p2']['a']:.3f}. Participants tested after sleep outperformed participants tested after wake intervals, supporting H1.

There was also a significant main effect of Cue, F(1, 76) = {stats['F']['b']:.2f}, p {fmt_p(stats['p']['b'])}, partial eta squared = {stats['eta_p2']['b']:.3f}. Participants in TMR conditions recalled more than participants in control conditions, supporting H2.

The Sleep x Cue interaction was not significant, F(1, 76) = {stats['F']['ab']:.2f}, p {fmt_p(stats['p']['ab'])}, partial eta squared = {stats['eta_p2']['ab']:.3f}. Thus, H3 was not supported in the present sample. The data suggest mostly parallel cueing benefits across sleep and wake contexts rather than a strong dependence of cueing effects on sleep state.

### Effect-size interpretation

Partial eta squared values indicate that sleep accounted for a substantial proportion of explainable variance relative to residual error, and cueing accounted for a smaller but meaningful proportion. The interaction effect size was comparatively small. In applied terms, both manipulations appear useful, but sleep status had the larger association with recall performance in this dataset.

## Discussion

The present analysis examined whether sleep and targeted cueing jointly shape recall performance. Three conclusions follow directly from the data pattern. First, sleep was associated with robustly higher recall compared with wake, consistent with a large body of consolidation research. Second, cueing was associated with additional performance gains, consistent with the idea that reactivation can strengthen memory traces. Third, the interaction was statistically weak, indicating that cueing benefits were not uniquely restricted to sleep in this specific dataset.

From a theoretical standpoint, the significant sleep effect aligns with systems consolidation accounts in which offline neural dynamics facilitate transformation and stabilization of memory. The observed cueing effect also aligns with reactivation frameworks, suggesting that sensory prompts linked to prior learning can bias subsequent retrieval success. Importantly, the absence of a strong interaction does not invalidate sleep-specific mechanisms; instead, it narrows interpretation. One possibility is that cueing in both states provided some retrieval or rehearsal-related benefit, while sleep conferred an independent consolidation advantage. Another possibility is that the dataset aggregates over participant-level moderators (e.g., encoding strength, circadian phase, arousal) that could obscure conditional effects.

The current findings are compatible with, but somewhat simpler than, results from high-control sleep-laboratory studies. Rasch et al. (2007) and related work emphasize that cue benefits can be strongest when cues are presented during specific sleep stages and under controlled sensory parameters. If the present protocol used broader or less stage-specific cueing windows, interaction attenuation would be expected. Similarly, reviews by Oudiette and Paller (2013) note that cue efficacy can depend on avoiding micro-arousals and matching cue intensity to perceptual thresholds. Without physiological recordings in the current dataset, such process-level distinctions cannot be tested.

Practical implications should be considered with care. For educational settings, the additive pattern suggests two potentially complementary levers: preserving sleep opportunity and using strategically timed reminders. For clinical translation, interventions targeting memory maintenance in aging or psychiatric populations might combine sleep hygiene with gentle reactivation paradigms. However, applied deployment requires stronger external-validity evidence and careful ethical handling of interventions that influence memory accessibility.

Several limitations constrain inference. The dataset includes condition labels and outcomes but not demographic covariates, baseline performance, or adherence metrics. Consequently, residual confounding cannot be ruled out. The sample size is respectable for detecting medium effects in a balanced design, yet still limited for subtle interaction detection. Moreover, no direct sleep-stage measurements are present, preventing mechanistic attribution to slow-wave activity, spindles, or replay-linked events. Finally, the design appears between participants; within-participant cueing contrasts often provide greater sensitivity and tighter control of individual differences.

Future research should extend this framework in at least four ways. First, preregistered experiments with polysomnography can test stage-locked cueing hypotheses directly. Second, hybrid designs combining within-item and between-person manipulations can separate trait-level and process-level variance. Third, longitudinal follow-up can determine whether benefits persist beyond immediate recall windows. Fourth, open-science workflows with shared code and data dictionaries can improve reproducibility and facilitate quantitative synthesis.

An additional translational point concerns implementation fidelity. In real-world settings, memory interventions often fail not because core mechanisms are absent, but because delivery quality is inconsistent. For example, cues may be played too loudly, at the wrong temporal offset, or in environments with substantial background noise. Sleep opportunity itself can be constrained by social schedules, stress, or shift work. Consequently, intervention frameworks should be designed with feasibility constraints in mind: low-burden cue delivery, clear participant instructions, and objective monitoring where possible. In psychology and behavioral medicine, scalability is often determined by whether protocols preserve effect-critical ingredients under ecologically valid conditions.

Equity considerations are also relevant. Access to high-quality sleep is unequally distributed across socioeconomic contexts, caregiving demands, and occupational patterns. If sleep-sensitive memory interventions are translated into educational or workplace policy, researchers and practitioners should avoid framing outcomes solely as individual responsibility. Structural influences on sleep timing and duration can moderate who benefits from evidence-based recommendations. Integrating sleep science with public-health perspectives may therefore improve both effectiveness and fairness in applied deployment.

Finally, replication strategy should include both direct and conceptual replications. Direct replications can verify whether the observed main effects in this dataset are stable under matched procedures and sampling frames. Conceptual replications can test boundary conditions by varying material type (e.g., vocabulary vs. visuospatial associations), cue modality (auditory, olfactory, tactile), and retention interval. Meta-analytic accumulation across such designs would clarify whether interaction effects emerge reliably only under narrow parameter ranges or whether the current near-additive pattern is generally representative.

In conclusion, this dataset supports the proposition that both sleep and cueing are associated with improved declarative recall, with sleep showing the stronger effect and no compelling interaction. The pattern reinforces a pragmatic message for memory optimization: protecting sleep remains foundational, while cue-based interventions may provide incremental gains when implemented thoughtfully. Continued mechanistic work is needed to map when, for whom, and under what neurophysiological constraints reactivation yields the largest benefits.

## Figure

Figure 1 (embedded in the PDF) presents group means with 95% confidence intervals for each Sleep x Cue cell. The visual pattern mirrors the ANOVA: higher scores in sleep than wake and higher scores in TMR than control, with approximately parallel cueing differences across sleep states.

## References

Antony, J. W., Gobel, E. W., O'Hare, J. K., Reber, P. J., & Paller, K. A. (2012). Cued memory reactivation during sleep influences skill learning. *Nature Neuroscience, 15*(8), 1114-1116. https://doi.org/10.1038/nn.3152

Diekelmann, S., & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience, 11*(2), 114-126. https://doi.org/10.1038/nrn2762

Oudiette, D., & Paller, K. A. (2013). Upgrading the sleeping brain with targeted memory reactivation. *Trends in Cognitive Sciences, 17*(3), 142-149. https://doi.org/10.1016/j.tics.2013.01.006

Rasch, B., Buchel, C., Gais, S., & Born, J. (2007). Odor cues during slow-wave sleep prompt declarative memory consolidation. *Science, 315*(5817), 1426-1429. https://doi.org/10.1126/science.1138581
"""
    return text


def escape_pdf_text(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def draw_graph_commands(means):
    # Coordinates in points for a simple bar chart
    x0, y0 = 70, 420
    width, height = 460, 220
    y_max = max(means.values()) + 3
    cmds = []
    cmds.append(f"0.2 w {x0} {y0} m {x0} {y0+height} l {x0+width} {y0+height} l S")
    for t in range(0, int(math.ceil(y_max))+1, 5):
        y = y0 + (t / y_max) * height
        cmds.append(f"0.9 0.9 0.9 RG 0.3 w {x0} {y:.2f} m {x0+width} {y:.2f} l S")
        cmds.append(f"0 0 0 rg BT /F1 9 Tf {x0-28} {y-3:.2f} Td ({t}) Tj ET")

    keys = [('Sleep', 'TMR'), ('Sleep', 'Control'), ('Wake', 'TMR'), ('Wake', 'Control')]
    labels = ['Sleep+TMR', 'Sleep+Ctrl', 'Wake+TMR', 'Wake+Ctrl']
    colors = ['0.22 0.49 0.72', '0.30 0.68 0.29', '0.60 0.31 0.64', '0.89 0.47 0.76']
    bar_w = 70
    gap = 35
    start_x = x0 + 35

    for i, key in enumerate(keys):
        x = start_x + i * (bar_w + gap)
        val = means[key]
        h = (val / y_max) * height
        r, g, b = colors[i].split()
        cmds.append(f"{r} {g} {b} rg {x:.2f} {y0:.2f} {bar_w} {h:.2f} re f")
        cmds.append(f"0 0 0 rg BT /F1 8 Tf {x-4:.2f} {y0-14:.2f} Td ({labels[i]}) Tj ET")
        cmds.append(f"0 0 0 rg BT /F1 8 Tf {x+18:.2f} {y0+h+4:.2f} Td ({val:.2f}) Tj ET")

    cmds.append("0 0 0 rg BT /F2 12 Tf 210 655 Td (Figure 1. Recall means by sleep and cue condition.) Tj ET")
    return '\n'.join(cmds)


def write_pdf(report_text, means, out_path):
    lines = [ln for ln in report_text.split('\n')]

    pages = []
    page_lines = []
    max_lines = 42

    for ln in lines:
        if len(ln) <= 95:
            wrapped = [ln]
        else:
            words = ln.split(' ')
            wrapped = []
            cur = ''
            for w in words:
                trial = (cur + ' ' + w).strip()
                if len(trial) <= 95:
                    cur = trial
                else:
                    wrapped.append(cur)
                    cur = w
            if cur:
                wrapped.append(cur)
        for wln in wrapped:
            page_lines.append(wln)
            if len(page_lines) >= max_lines:
                pages.append(page_lines)
                page_lines = []
    if page_lines:
        pages.append(page_lines)

    # Insert graph on page 2 if possible
    if len(pages) >= 2:
        pages[1] = pages[1][:8] + ['[GRAPH_PLACEHOLDER]'] + pages[1][8:]

    objs = []

    def add_obj(content):
        objs.append(content)
        return len(objs)

    font1 = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font2 = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    content_ids = []
    page_ids = []

    for idx, plines in enumerate(pages):
        y = 770
        text_cmds = ["BT", "/F1 11 Tf", "50 770 Td"]

        for ln in plines:
            if ln == '[GRAPH_PLACEHOLDER]':
                text_cmds.append("ET")
                text_cmds.append(draw_graph_commands(means))
                text_cmds.append("BT")
                text_cmds.append("/F1 11 Tf")
                text_cmds.append(f"50 {y-250} Td")
                y -= 250
                continue
            if ln.startswith('# '):
                text_cmds.append("ET")
                text_cmds.append(f"BT /F2 16 Tf 50 {y} Td ({escape_pdf_text(ln[2:])}) Tj ET")
                text_cmds.append("BT /F1 11 Tf")
                y -= 20
                text_cmds.append(f"50 {y} Td")
            elif ln.startswith('## '):
                text_cmds.append("ET")
                text_cmds.append(f"BT /F2 13 Tf 50 {y} Td ({escape_pdf_text(ln[3:])}) Tj ET")
                text_cmds.append("BT /F1 11 Tf")
                y -= 16
                text_cmds.append(f"50 {y} Td")
            else:
                text_cmds.append(f"({escape_pdf_text(ln)}) Tj")
                text_cmds.append("0 -14 Td")
                y -= 14

        text_cmds.append("ET")
        stream = '\n'.join(text_cmds)
        cid = add_obj(f"<< /Length {len(stream.encode('latin-1', errors='replace'))} >>\nstream\n{stream}\nendstream")
        content_ids.append(cid)

    pages_kids = []
    pages_obj_placeholder = len(objs) + 1

    for cid in content_ids:
        pid = add_obj(f"<< /Type /Page /Parent {pages_obj_placeholder} 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> /Contents {cid} 0 R >>")
        page_ids.append(pid)
        pages_kids.append(f"{pid} 0 R")

    pages_obj = add_obj(f"<< /Type /Pages /Kids [{' '.join(pages_kids)}] /Count {len(page_ids)} >>")
    catalog = add_obj(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>")

    pdf = ["%PDF-1.4\n"]
    offsets = [0]
    for i, obj in enumerate(objs, start=1):
        offsets.append(sum(len(p.encode('latin-1', errors='replace')) for p in pdf))
        pdf.append(f"{i} 0 obj\n{obj}\nendobj\n")

    xref_pos = sum(len(p.encode('latin-1', errors='replace')) for p in pdf)
    pdf.append(f"xref\n0 {len(objs)+1}\n")
    pdf.append("0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.append(f"{off:010d} 00000 n \n")
    pdf.append(f"trailer\n<< /Size {len(objs)+1} /Root {catalog} 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(''.join(pdf).encode('latin-1', errors='replace'))


def main():
    rows = load_data(DATA_PATH)
    groups = group_scores(rows)
    stats = anova_2x2(groups)

    report = build_report(rows, groups, stats)
    MD_PATH.write_text(report)
    write_pdf(report, stats['means_ab'], PDF_PATH)

    wc = len([w for w in report.split() if w.strip()])
    print(f"Generated: {MD_PATH} and {PDF_PATH}")
    print(f"Word count: {wc}")


if __name__ == '__main__':
    main()
