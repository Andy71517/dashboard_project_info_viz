# Submission execution and PDF checks

On November 21, 2026, we reran the notebook from the original SHA-256-checked HPS and BLS inputs after the language revision. This was a complete local Python 3.12.2 run, not execution in Colab. All 39 code cells completed in 196.5 seconds, with 226 passing notebook checks, no error outputs, and 23 inline figures. The state-cycle join contains 459 rows with no unmatched keys. All 20 automated raw-to-processed comparisons passed. The seven regenerated main analysis CSVs and seven follow-up analysis CSVs reproduce the prior results within numerical tolerance of 1e-8 (relative tolerance 1e-9).

The executed notebook is saved in `notebooks/COVID_Recovery_Step0.ipynb`. Its code and Markdown sources are unchanged from the preceding language-revision commit. We refreshed the public captions, chart export, briefing, follow-up tables, and execution records. As in the earlier public export, we omitted output lines containing machine-specific workspace locations; no analysis results or plots were removed. Original respondent data and the private case-comparison table remain outside the repository.

The three submission PDFs are in `reports/submission/`:

- `01_Executed_Notebook.pdf`: 76 pages, with all code and saved outputs, including 23 figures. Landscape A3 pages keep wide code and charts readable; long code lines wrap for printing.
- `02_Requirements.pdf`: 4 pages, preserving the current requirements document.
- `03_Conversations.pdf`: 59 pages, preserving all three transcript texts. The original Maya and Jordan PDF exports cropped some charts, so we reflowed the text and all 32 embedded images from those exports. Images appear at the source text's image marker in their original PDF order. The Elena interview remains clearly labeled as an LLM simulation.

All pages were rendered and reviewed. Text extraction checks retained every code line, transcript line, and requirements paragraph; all text lies within page boundaries, no empty pages remain, and all expected images are present. Repository checks and Round 1 data checks passed before publication.

The team's manual review of at least 20 raw-versus-cleaned cases remains pending. Automated checks do not replace that review. The expert interview is simulated and does not constitute an independent statistical audit.

## Presentation update

The submission PDFs now use the earlier documents' visual style: dark blue titles, blue section headings, muted footer rules, and shaded speaker labels in the conversations. The newer complete charts and page layouts are retained. A before-and-after comparison confirms that the text and embedded image content are unchanged, excluding footer and pagination styling. The executed notebook file is unchanged. All final pages were rendered and reviewed; completeness and page-boundary checks passed.
