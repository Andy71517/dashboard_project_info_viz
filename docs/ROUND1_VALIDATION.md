# Round 1 execution and validation

Validated November 19, 2026, after reviewing source commit `98e70bf`.

The complete notebook ran from the original fingerprint-checked files through all 23 charts and follow-up tables. All 39 code cells executed with no error outputs. The full raw-data run took 380 seconds locally. Chart/export cells were then rerun from those same weighted outputs to polish sample labels, suppression markers and the Cycle 8 annotation; no respondent records were changed by that layout pass.

| Check | Actual result |
|---|---|
| HPS original response records | 610,755 |
| State-cycle join | 459 rows; zero unmatched on either side |
| HPS aggregate views | 8,892; overlapping groups |
| Notebook checks | 226 passing; no failures |
| Automated raw-to-processed spot-check | 20 cases, 180 field comparisons, all passed |
| Saved inline figures | 23 |
| Round 1 request dispositions | 17: 10 answered, 4 partial, 1 unavailable, 2 out of scope |
| Overall state-cycle hardship evidence | 459 rows |
| State work/income evidence | 2,754 rows |
| State age evidence | 1,377 rows |
| Exact published-rate at/below | 21 jurisdictions |
| Separate ±0.1 display band | 6 jurisdictions |
| Virginia suppressed work/under-$50k cell | valid n=98; remains suppressed |
| Round 2 persona replies | Not generated |

The saved outputs are local execution evidence, not execution in the user's Google account. Manual review of the private 20-case comparison remains a team task. Original Round 1 conversations, persona responses and transcript PDFs were preserved. The original review was archived before its corrections.

Run `python scripts/check_repository.py` for the committed artifact/link/privacy checks and `python scripts/check_round1.py` for decimal arithmetic, exact ties, peak-month ties, count changes, decline flags, suppression and all-cycle evidence checks. Final results: **478 repository checks passed** and **3,632 Round 1 data/edge-case checks passed**. All 23 rendered figures were visually inspected, including the corrected Virginia suppression marker, interval/sample labels, and Cycle 8 annotations.

The [methods note](ROUND1_METHODS.md) separates the documented Phase 4.2 frame change from the unidentified cause of missingness, point adult counts from count uncertainty, and marginal intervals from formal ranking tests. The [next-round handoff](../personas/round2_handoff.md) contains questions to ask, not invented replies.

During publication, remote commit `8970b6e` added `reports/step3_requirement.md`. That authored draft was preserved and merged. A status note identifies it as a working proposal pending the later-round feedback, without rewriting its body or treating it as evidence those conversations occurred.

## Subsequent BLS access repair

The acquisition cell was tested again after a Colab HTTP 403 report for `la.txt`. It now retrieves the exact verified BLS support archive from a pinned repository revision when files are absent, while retaining both official BLS hosts as a fallback. It also recognizes a manual upload directly in the input cell. Existing inputs are preserved; archive and member fingerprints remain mandatory.

Eight regression tests passed, covering simulated BLS 403s, both official-host directions, local/offline recovery, corrupted archives, altered member fingerprints, existing-file preservation, and an informative fully-blocked-network failure. A live run of the actual acquisition cell started without all seven BLS files, restored them from the repository archive, and matched all 16 original input fingerprints. All 39 code-cell outputs and 23 figures were retained. The updated repository check passed 484 checks. This does not claim execution in the user's Colab account.
