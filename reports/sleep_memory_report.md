# Sleep, Targeted Memory Reactivation, and Declarative Recall: An APA-Style Quantitative Report

## Abstract

This report evaluates whether post-learning sleep and targeted memory reactivation (TMR) are associated with stronger declarative memory performance, and whether the effect of cueing depends on sleep state. The dataset contains 80 observations in a balanced 2 x 2 between-participants design: Sleep (Sleep vs. Wake) x Cue Condition (TMR vs. Control), with recall score as the outcome. Descriptive statistics showed the highest mean recall in the Sleep+TMR condition and the lowest mean recall in the Wake+Control condition. A factorial analysis of variance indicated significant main effects of sleep, F(1, 76) = 42.01, p < .001, partial eta squared = 0.356, and cueing, F(1, 76) = 16.01, p < .001, partial eta squared = 0.174. The Sleep x Cue interaction was not statistically significant, F(1, 76) = 0.07, p = .798, partial eta squared = 0.001. The pattern is consistent with models proposing that sleep broadly supports consolidation and that TMR contributes additive gains. The findings align with prior laboratory work showing that cue presentation can benefit memory when linked to prior learning and that sleep-associated systems consolidation improves retention. Practical implications include optimization of learning schedules and cautious translation to educational or clinical contexts. Limitations include unknown randomization procedures, absence of covariates, and no direct measurement of sleep architecture. Future work should include preregistered designs, polysomnography-based mechanistic tests, and longitudinal follow-up.

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

- Sleep + Control: n = 20, M = 26.49, SD = 3.58, 95% CI [24.92, 28.06]
- Sleep + TMR: n = 20, M = 29.85, SD = 3.92, 95% CI [28.14, 31.57]
- Wake + Control: n = 20, M = 21.58, SD = 3.36, 95% CI [20.11, 23.05]
- Wake + TMR: n = 20, M = 24.54, SD = 3.22, 95% CI [23.12, 25.95]

Across levels of cue condition, the sleep groups averaged 28.17 points whereas wake groups averaged 23.06 points, indicating a raw sleep advantage of 5.11 points. Across levels of sleep state, TMR groups averaged 27.19 points and control groups averaged 24.04 points, indicating a cueing advantage of 3.16 points.

Condition means followed the theoretically expected ordering: Sleep+TMR (highest), Sleep+Control, Wake+TMR, and Wake+Control (lowest). This ordering alone cannot determine statistical reliability, but it is consistent with additive benefits of sleep and cueing.

### Inferential findings

The factorial ANOVA revealed a significant main effect of Sleep, F(1, 76) = 42.01, p < .001, partial eta squared = 0.356. Participants tested after sleep outperformed participants tested after wake intervals, supporting H1.

There was also a significant main effect of Cue, F(1, 76) = 16.01, p < .001, partial eta squared = 0.174. Participants in TMR conditions recalled more than participants in control conditions, supporting H2.

The Sleep x Cue interaction was not significant, F(1, 76) = 0.07, p = .798, partial eta squared = 0.001. Thus, H3 was not supported in the present sample. The data suggest mostly parallel cueing benefits across sleep and wake contexts rather than a strong dependence of cueing effects on sleep state.

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
