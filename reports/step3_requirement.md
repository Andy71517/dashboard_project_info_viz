# Dashboard Requirements Document

**Economic Hardship and Social Well-Being During Pandemic Recovery**  
**Group 6 — Anirudh Reddy Alledula · Shane Malamut · Yuxing Zhou**  
*Project Part 2 — Step 3 | November 2026*

**LLM interviews:** Maya Rodriguez and Jordan Lee — **GPT-5.6 Terra** (HOKIEAI ONEchat); Dr. Elena Chen — **GPT-6** (simulated ChatGPT interview).

## 1. The Real Need

When we started this project, our main question was whether improving employment conditions went along with less financial hardship and better social well-being after the pandemic. We expected unemployment to be a useful starting point. After talking with our stakeholders, we realized that it doesn't tell the whole story. A state's unemployment rate can improve even if its labor force shrinks, and people who worked recently can still struggle to pay their bills.

We want the dashboard to help users look at these issues side by side **without treating them as the same thing**. For policymakers, that means comparing unemployment, employment, and labor-force changes rather than relying on one recovery measure. For community organizations, it means seeing where adults report difficulty paying household expenses and how that differs by work, income, and social well-being. We also want users to see when an estimate is too uncertain to rely on.

This is a tool for exploring patterns and asking better questions, not for proving what caused them. Our data cannot show that unemployment or COVID-19 caused anxiety, loneliness, or household hardship, and they cannot tell an organization where to open a service center. Those decisions would require additional evidence.

## 2. Audience

**Maya Rodriguez — state policy decision-maker.** Maya works with workforce and social-support planning at the Virginia Department of Labor and Industry. She understands labor-market statistics and wants to identify states worth a closer policy review. She needs to compare 2019 and 2024 unemployment rates, see what happened during 2020, and check whether employment and labor-force counts tell a different story. A simple “recovered/not recovered” label would be misleading to her, especially if it hides changes in the number of people working or looking for work.

**Jordan Lee — nonprofit program manager and dashboard user.** Jordan works at Community Bridge Network, which provides employment assistance, financial support, benefits navigation, and referrals. He is less concerned with ranking states by unemployment and more interested in the people behind the hardship estimates: how common difficulty paying expenses is, roughly how many adults it represents, and which work and income groups report it. He needs clear labels and practical comparisons. However, he cannot make staffing or location decisions from state survey data alone. For that, he would also need local requests, unmet demand, waiting times, and service capacity.

**Dr. Elena Chen — skeptical domain expert.** Elena's role in our simulated expert review was to question how we prepared and interpreted the data. She pushed us to be precise about survey weights, sample sizes, missing responses, state-level versus individual-level measures, and the difference between association and causation. Her feedback is especially important for making sure a clear-looking chart doesn't give readers more confidence than the data deserve.

Our secondary audience is anyone who can read a chart but may not know the survey terminology. We want them to understand the question, the population being measured, and the important limits without having to read the notebook first.

## 3. Main Representations

We use two sources. The **2024 Census Household Pulse Survey (HPS)** contains 610,755 adult response records across Cycles 1–9, from January through September. It gives us self-reported measures of household expense difficulty, recent work, 2023 household income, loneliness, anxiety symptoms, social support, and age. The **BLS Local Area Unemployment Statistics (LAUS)** provide state labor-market measures from 2019–2024. We summarize HPS by state and cycle before attaching approximately time-aligned LAUS data, giving us 459 state-cycle records with no unmatched keys. This is a state-and-period comparison, **not a match between individual people**.

**Labor-market benchmarks (Q1).** We plan to use a sortable table and a connected-dot chart showing each state's 2019, 2020, and 2024 annual unemployment rates, its 2020 monthly peak, and changes in employment and labor-force counts since 2019. In our data, **21 of 51 jurisdictions** had a published 2024 annual unemployment rate at or below their 2019 rate. But that does not mean all 21 fully recovered. Virginia, for example, went from **2.8% in 2019 to 2.9% in 2024**: just above the strict threshold, even though its employment and labor-force counts rose. Annual rates are unadjusted, while the 2020 monthly peaks use seasonally adjusted data, so we will label those separately. We also keep exact published ties separate from a descriptive ±0.1-percentage-point display band.

**Where hardship is reported (Q2).** Our main overview will show the weighted percentage of adults who said paying their usual household expenses was **“somewhat” or “very” difficult**. Users should be able to select a state and cycle, see the national reference, and switch to an estimate of the number of adults reporting hardship. The estimated counts are useful for understanding scale, but they are **population estimates, not counts of people applying for help**. We also tested the state-level relationship between unemployment and hardship. The Spearman correlations were weak, roughly **0.10–0.21** across cycles. That makes the scatterplot useful as context, but not as a reliable way to rank where assistance is needed. Our state-resampling ranges are descriptive checks, not survey-design confidence intervals.

**Work and income (Q3).** A grouped chart will compare hardship across six combinations of recent work and household income: worked or did not work for pay in the past seven days, crossed with **under $50,000**, **$50,000–$99,999**, and **$100,000 or more** in *2023 household income*. For instance, the national Cycle 9 hardship estimate for recent workers in the under-$50,000 group is about **55.8%**. This tells us that recent work and reported hardship can coexist; it does **not** measure official unemployment or whether a person qualifies for aid. Some state-level groups are too small to display. The Virginia Cycle 9 result for this group is suppressed because it has **98 valid responses** (Kish effective sample size about **49.2**), below our minimum valid-count rule of 100. A suppressed result should never be displayed as zero.

**Loneliness and anxiety (Q4).** We will use paired charts to compare people who reported expense difficulty with those who reported little or none. “Frequent loneliness” means answering **always or usually**; “frequent anxiety” means symptoms on **more than half the days or nearly every day**. In Cycle 9, the national loneliness estimates were about **21.0% versus 8.2%**, and anxiety estimates were **26.9% versus 9.7%**, for hardship versus little/no hardship. The Virginia comparisons show the same direction. These are descriptions of self-reported experiences, **not medical diagnoses or evidence that hardship caused the symptoms**. We can show separate 90% confidence intervals, but we have not carried out a formal survey-weighted test of the difference between the groups.

**Age and social support (Q5).** A smaller supporting view will compare loneliness and lack of social support across the approximate age groups **18–34, 35–64, and 65+**. We will start with the national results. State-age estimates will only be shown when they meet our reliability rule; we cannot assume that the national pattern holds in every state.

**What users need to know about data quality.** HPS percentages use person weights and valid responses for the particular question, with reported **90% confidence intervals** and an accompanying valid count and Kish effective sample size. Our project suppresses a result if **valid n < 100** or **effective n < 30**. That rule helps us avoid showing very small cells, but it does not make every remaining estimate perfectly reliable. Missing answers can also affect the results; for example, income has roughly **14–19%** missing or invalid responses across cycles. In addition, Census documented a survey contact-frame change starting in **Cycle 8**. Missingness also changed around that time, but we cannot say the frame change caused it. We will mark Cycle 8 on time-series charts and explain that comparisons across that boundary need extra care.

These choices reflect the stakeholder rounds. Maya asked for a fuller picture of labor-market change, Jordan pushed us to focus on hardship and make the results usable for service planning, and Elena challenged the claims we could defend statistically. The resulting dashboard is less about telling one neat “recovery” story and more about showing what each measure actually says.

## 4. Exploration Tasks

We want users to be able to answer their own follow-up questions without digging through separate files. The main interactions will be:

1. **Select a state and HPS cycle,** with Virginia as the initial state and a national comparison where available. Show the dates covered by each cycle.
2. **Explore labor-market changes:** sort and filter states by annual unemployment rates, 2020 monthly peak, employment change, labor-force change, and the strict 2019-versus-2024 benchmark. Make it easy to find states whose unemployment rate improved while their employment or labor-force counts fell.
3. **Compare hardship rates and scale:** switch between weighted percentages and estimated numbers of adults reporting hardship, keeping the units clearly labeled.
4. **Compare groups:** examine work and 2023 income categories, switch between loneliness and anxiety by hardship group, and explore age groups nationally or within states where estimates are available.
5. **Check reliability and limitations:** read the valid count, effective sample size, 90% interval, missingness, suppression reason, and source note. The chart should also flag the Cycle 8 change and explain that LAUS is state-level context and that associations do not prove causation.

## 5. Conflicts

**What should users see first?** Maya preferred starting with labor-market recovery, while Jordan wanted hardship to be the focus. We chose a **hardship-first landing view**, since it connects more directly to the project's household well-being question and Jordan's service-planning needs. However, labor-market benchmarks will have a prominent section rather than being hidden in the background. We will not combine the measures into a single “recovery” or “need” score.

**Is a state comparison enough to guide action?** Maya can use state comparisons to decide what deserves further policy review, but Jordan needs ZIP- or county-level demand before choosing locations or staff. We decided to keep the first version **state-level** and be upfront that it cannot identify clients, local service gaps, or exact funding needs.

**Should states be ranked?** A sorted chart makes it easier to explore which estimates are higher or lower, but small differences may be misleading. We will allow sorting by point estimates while showing confidence intervals, sample sizes, and suppression. We will **not** present those positions as statistically proven rankings or funding priorities.

**How do we show changes over time?** Everyone wanted trends, but Elena pointed out the importance of the Cycle 8 survey change and the fact that HPS is a series of cross-sectional samples. We will keep the cycle views, clearly mark the change, and avoid presenting them as if they track the same people or directly measure changes in service demand.

## 6. Must-Have vs. Nice-to-Have Charts and Features

**Must-have for the first dashboard:**

- A **state hardship overview**, with weighted percentages, national comparison, 90% intervals, and a companion affected-adult point estimate.
- A **state profile** (Virginia by default) with work/income hardship, loneliness and anxiety comparisons, age/social-support context, and clear suppression labels.
- A **labor-market comparison** with sortable state records, annual unemployment rates, 2020 monthly peaks, and employment/labor-force changes since 2019.
- A **work-by-income chart** and a **loneliness/anxiety-by-hardship chart**, both with plain-language labels, sample information, and uncertainty.
- State/cycle selectors, a percentage-versus-count option, readable tooltips or notes for definitions and sources, and **visible Cycle 8 and reliability warnings**. Suppressed values must never be replaced with zeros.

**Nice to have if time and data allow:** a state map, small-multiple unemployment timelines, downloadable filtered data, and a user option to switch between the strict unemployment-rate benchmark and the ±0.1-point display band. More local indicators or organizational service-demand data could make a later version more actionable, but they would require additional datasets and careful validation. Formal tests of state or subgroup differences would also require additional survey-design analysis.

Before submitting our analysis, we still need to record the team's **manual review of at least 20 raw-versus-cleaned rows**. The notebook already reports 20 successful *automated* comparisons, but that is not the same as a human check. The Elena conversation was an AI-simulated expert review, not an independent audit of the survey variance calculations. We have kept those limits explicit rather than claiming work we did not do.