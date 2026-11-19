from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


FOCUS_STATE = "51"  # Virginia
FOCUS_CYCLE = 9


@dataclass
class OutputRecord:
	file: str
	title: str
	caption: str
	source: str


class PersonaRound2Builder:
	def __init__(self) -> None:
		self.repo_root = Path(__file__).resolve().parents[1]
		self.data_dir = self.repo_root / "data" / "processed"
		self.audit_dir = self.repo_root / "audit" / "step0"
		self.output_dir = self.repo_root / "reports" / "step0" / "persona_round2"
		self.chart_dir = self.output_dir / "charts"
		self.output_dir.mkdir(parents=True, exist_ok=True)
		self.chart_dir.mkdir(parents=True, exist_ok=True)

		self.records: list[OutputRecord] = []

		self.hps = pd.read_csv(self.data_dir / "hps_2024_aggregates.csv")
		self.joined = pd.read_csv(self.data_dir / "joined_state_cycle_2024.csv")
		self.laus_month = pd.read_csv(self.data_dir / "laus_state_month_2019_2024.csv")
		self.laus_annual = pd.read_csv(self.data_dir / "laus_state_annual_2019_2024.csv")
		self.missing = pd.read_csv(self.audit_dir / "hps_missingness.csv")

		state_names = self.joined[["state_fips", "state_name"]].drop_duplicates().copy()
		state_names["state_fips"] = state_names["state_fips"].astype(str).str.zfill(2)
		self.state_name_map = state_names.set_index("state_fips")["state_name"].to_dict()

		plt.rcParams.update(
			{
				"figure.figsize": (11, 6),
				"figure.dpi": 120,
				"font.size": 10.5,
				"axes.spines.top": False,
				"axes.spines.right": False,
				"axes.titleweight": "bold",
				"text.parse_math": False,
			}
		)

	def save_chart(self, fig: plt.Figure, filename: str, title: str, caption: str, source: str) -> None:
		path = self.chart_dir / filename
		fig.suptitle(title, x=0.02, y=0.99, ha="left", va="top", fontsize=14, fontweight="bold")
		fig.text(0.02, 0.015, source, ha="left", va="bottom", fontsize=8.5, color="#444444")
		fig.tight_layout(rect=(0, 0.05, 1, 0.95))
		fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
		plt.close(fig)
		self.records.append(OutputRecord(path.name, title, caption, source))

	def build_recovery_table(self) -> pd.DataFrame:
		annual = self.laus_annual.copy()
		month = self.laus_month.copy()

		annual_u = annual[annual["seasonal"] == "U"]
		month_s = month[(month["seasonal"] == "S") & (month["year"] == 2020)].copy()

		annual_wide = annual_u.pivot_table(
			index=["state_fips", "state_name"],
			columns="year",
			values=["unemployment_rate_pct", "employment_persons", "labor_force_persons"],
			aggfunc="first",
		)
		annual_wide.columns = [f"{a}_{b}" for a, b in annual_wide.columns]
		annual_wide = annual_wide.reset_index()

		peak_idx = month_s.groupby("state_fips")["unemployment_rate_pct"].idxmax()
		peaks = month_s.loc[peak_idx, ["state_fips", "unemployment_rate_pct", "month"]].copy()
		peaks = peaks.rename(
			columns={
				"unemployment_rate_pct": "unemployment_rate_2020_peak_monthly_pct",
				"month": "unemployment_rate_2020_peak_month",
			}
		)

		out = annual_wide.merge(peaks, on="state_fips", how="left", validate="one_to_one")
		out = out.rename(
			columns={
				"unemployment_rate_pct_2019": "unemployment_rate_2019_pct",
				"unemployment_rate_pct_2020": "unemployment_rate_2020_annual_pct",
				"unemployment_rate_pct_2024": "unemployment_rate_2024_pct",
				"employment_persons_2019": "employment_2019",
				"employment_persons_2024": "employment_2024",
				"labor_force_persons_2019": "labor_force_2019",
				"labor_force_persons_2024": "labor_force_2024",
			}
		)

		out["change_2019_2024_pp"] = out["unemployment_rate_2024_pct"] - out["unemployment_rate_2019_pct"]
		out["employment_change_pct"] = (out["employment_2024"] / out["employment_2019"] - 1.0) * 100
		out["labor_force_change_pct"] = (out["labor_force_2024"] / out["labor_force_2019"] - 1.0) * 100

		out["recovery_band"] = np.select(
			[
				out["change_2019_2024_pp"].abs().le(0.1),
				out["change_2019_2024_pp"].lt(-0.1),
				out["change_2019_2024_pp"].gt(0.1),
			],
			["within +-0.1", "at/below 2019", "above 2019"],
			default="check",
		)

		out["rate_down_but_labor_force_down"] = out["change_2019_2024_pp"].lt(0) & out["labor_force_change_pct"].lt(0)

		out["state_fips"] = out["state_fips"].astype(str).str.zfill(2)
		out = out.sort_values(["change_2019_2024_pp", "state_name"]).reset_index(drop=True)
		keep = [
			"state_fips",
			"state_name",
			"unemployment_rate_2019_pct",
			"unemployment_rate_2020_annual_pct",
			"unemployment_rate_2020_peak_monthly_pct",
			"unemployment_rate_2020_peak_month",
			"unemployment_rate_2024_pct",
			"change_2019_2024_pp",
			"recovery_band",
			"employment_change_pct",
			"labor_force_change_pct",
			"rate_down_but_labor_force_down",
		]
		out = out[keep]
		out.to_csv(self.output_dir / "state_recovery_table_with_flags.csv", index=False)
		return out

	def chart_state_profile(self) -> None:
		state_name = self.state_name_map.get(FOCUS_STATE, f"State {FOCUS_STATE}")
		fig, axes = plt.subplots(2, 2, figsize=(13, 9))

		state_all = self.hps[(self.hps["state_fips"] == FOCUS_STATE) & (self.hps["dimension"] == "all")].sort_values("cycle")
		us_all = self.hps[(self.hps["state_fips"] == "US") & (self.hps["dimension"] == "all")].sort_values("cycle")
		ax = axes[0, 0]
		ax.plot(state_all["cycle"], state_all["hardship_pct"], marker="o", color="#A25C38", label=state_name)
		ax.plot(us_all["cycle"], us_all["hardship_pct"], marker="o", color="#287D8E", label="United States")
		ax.axvline(8, linestyle="--", color="#666666", linewidth=1)
		ax.text(8.1, ax.get_ylim()[1] * 0.95, "possible survey change", fontsize=8, color="#666666")
		ax.set_title("Hardship trend")
		ax.set_xlabel("Cycle")
		ax.set_ylabel("Hardship (%)")
		ax.set_xticks(range(1, 10))
		ax.legend(frameon=False)

		ax = axes[0, 1]
		wi = self.hps[
			(self.hps["state_fips"] == FOCUS_STATE)
			& (self.hps["cycle"] == FOCUS_CYCLE)
			& (self.hps["dimension"] == "work_income")
		].copy()
		order = [
			f"{w} / {i}"
			for i in ["Under $50k", "$50k-$99,999", "$100k+"]
			for w in ["Worked in last 7 days", "Did not work in last 7 days"]
		]
		wi = wi.set_index("group").reindex(order).reset_index()
		yi = np.arange(len(wi))
		mask = wi["hardship_pct"].notna()
		colors = ["#287D8E" if str(group).startswith("Worked") else "#A25C38" for group in wi["group"]]
		ax.barh(yi[mask], wi.loc[mask, "hardship_pct"], color=np.array(colors, dtype=object)[mask.to_numpy()])
		for idx in yi[~mask.to_numpy()]:
			ax.text(1.0, idx, "suppressed", fontsize=8, va="center", color="#666666")
		ax.set_yticks(yi)
		ax.set_yticklabels(
			wi["group"].str.replace("Worked in last 7 days / ", "Worked · ", regex=False).str.replace(
				"Did not work in last 7 days / ", "Did not work · ", regex=False
			)
		)
		ax.invert_yaxis()
		ax.set_title(f"Work x income (cycle {FOCUS_CYCLE})")
		ax.set_xlabel("Hardship (%)")

		ax = axes[1, 0]
		hg = self.hps[
			(self.hps["state_fips"] == FOCUS_STATE)
			& (self.hps["cycle"] == FOCUS_CYCLE)
			& (self.hps["dimension"] == "hardship")
		].set_index("group")
		labels = ["Not at all/a little difficult", "Somewhat/very difficult"]
		x = np.arange(len(labels))
		for shift, metric, label, color in [
			(-0.18, "lonely", "Frequent loneliness", "#287D8E"),
			(0.18, "frequent_anxiety", "Frequent anxiety", "#A25C38"),
		]:
			vals = hg.loc[labels, f"{metric}_pct"].to_numpy(float)
			ax.bar(x + shift, vals, width=0.34, color=color, label=label)
		ax.set_xticks(x, ["Not at all/a little", "Somewhat/very"])
		ax.set_title(f"Q4 in {state_name} (cycle {FOCUS_CYCLE})")
		ax.set_xlabel("Expense difficulty group")
		ax.set_ylabel("Percent")
		ax.legend(frameon=False, fontsize=8)

		ax = axes[1, 1]
		age = self.hps[
			(self.hps["state_fips"].isin(["US", FOCUS_STATE]))
			& (self.hps["cycle"] == FOCUS_CYCLE)
			& (self.hps["dimension"] == "age")
		].copy()
		order_age = ["18-34", "35-64", "65+"]
		for loc, color in [("US", "#287D8E"), (FOCUS_STATE, "#A25C38")]:
			part = age[age["state_fips"] == loc].set_index("group").reindex(order_age)
			ax.plot(order_age, part["lonely_pct"], marker="o", label=f"{self.state_name_map.get(loc, 'US')} lonely", color=color)
		ax.set_title(f"Age pattern (cycle {FOCUS_CYCLE})")
		ax.set_ylabel("Frequent loneliness (%)")
		ax.legend(frameon=False, fontsize=8)

		title = f"State Profile: {state_name} (cycle {FOCUS_CYCLE})"
		caption = (
			"Single-state profile for persona review: hardship trend versus U.S., within-state work/income groups, "
			"hardship-group social outcomes, and age differences. Suppressed groups are labeled rather than imputed."
		)
		source = "Source: processed HPS aggregates only (no raw-data rerun)."
		self.save_chart(fig, "17_state_profile_focus.png", title, caption, source)

	def chart_state_hardship_percent_and_counts(self) -> None:
		focus = self.joined[self.joined["cycle"] == FOCUS_CYCLE].copy().sort_values("hardship_pct")
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 10), sharey=True, gridspec_kw={"width_ratios": [1.25, 1]})

		y = np.arange(len(focus))
		ax1.errorbar(
			focus["hardship_pct"],
			y,
			xerr=[focus["hardship_pct"] - focus["hardship_ci90_lower"], focus["hardship_ci90_upper"] - focus["hardship_pct"]],
			fmt="o",
			color="#287D8E",
			ecolor="#9CCBD6",
			capsize=2,
		)
		ax1.set_yticks(y, focus["state_name"])
		ax1.set_xlabel("Hardship (%)")
		ax1.set_title("Hardship percentage with 90% interval", loc="left", fontsize=10)

		counts_m = focus["hardship_weighted_numerator"] / 1_000_000.0
		ax2.barh(y, counts_m, color="#A25C38", alpha=0.88)
		ax2.set_xlabel("Estimated adults affected (millions)")
		ax2.set_title("Estimated number of adults", loc="left", fontsize=10)
		ax2.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.1f}"))

		for i, row in enumerate(focus.itertuples()):
			if bool(row.hardship_suppressed):
				ax2.text(0.02, i, "suppressed", va="center", fontsize=7.5, color="#666666")
			elif row.hardship_valid_n < 130:
				ax2.text(counts_m.iloc[i] + 0.02, i, f"n={int(row.hardship_valid_n)}", va="center", fontsize=7)

		title = "State hardship: percentage and affected adults"
		caption = (
			"Companion view for targeting decisions: left panel shows percentages with uncertainty, right panel shows "
			"estimated adult counts from weighted numerators."
		)
		source = "Source: joined HPS+LAUS cycle table and HPS weighted numerators (processed exports)."
		self.save_chart(fig, "18_state_hardship_pct_and_count.png", title, caption, source)

	def chart_timeline_with_va(self) -> None:
		states = ["06", "36", "48", FOCUS_STATE]
		part = self.laus_month[(self.laus_month["seasonal"] == "S") & (self.laus_month["state_fips"].isin(states))].copy()
		part["date"] = pd.to_datetime(part["date"])
		fig, ax = plt.subplots(figsize=(11.5, 5.8))

		palette = {"06": "#287D8E", "36": "#A25C38", "48": "#7A5BA6", FOCUS_STATE: "#0F3D49"}
		for state in states:
			df = part[part["state_fips"] == state].sort_values("date")
			ax.plot(df["date"], df["unemployment_rate_pct"], linewidth=2, color=palette[state], label=self.state_name_map.get(state, state))

		ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-12-31"), color="#DDE5EA", alpha=0.4)
		ax.set_xlabel("Month")
		ax.set_ylabel("Unemployment rate (%, seasonally adjusted)")
		ax.legend(frameon=False, ncols=2)
		title = "State unemployment timeline including Virginia"
		caption = "Adds Virginia to the existing comparison set so policy persona requests are represented in trend context."
		source = "Source: LAUS monthly seasonally adjusted rates (processed export)."
		self.save_chart(fig, "19_unemployment_timeline_with_va.png", title, caption, source)

	def chart_reliability_heatmap(self) -> None:
		subset = self.hps[
			(self.hps["cycle"] == FOCUS_CYCLE)
			& (self.hps["state_fips"] != "US")
			& (self.hps["dimension"] == "work_income")
		].copy()

		table = subset.pivot_table(index="state_fips", columns="group", values="hardship_suppressed", aggfunc="first")
		table = table.reindex(sorted(table.index))
		matrix = table.astype(float).to_numpy()

		fig, ax = plt.subplots(figsize=(13, 10))
		img = ax.imshow(matrix, aspect="auto", cmap="RdYlGn_r", vmin=0, vmax=1)
		ax.set_xticks(range(table.shape[1]), table.columns, rotation=35, ha="right")
		ax.set_yticks(range(table.shape[0]), [self.state_name_map.get(s, s) for s in table.index], fontsize=7)
		ax.set_xlabel("Work x income group")
		ax.set_ylabel("State")
		ax.set_title(f"Suppression map (cycle {FOCUS_CYCLE}): 1=suppressed, 0=reported", loc="left", fontsize=10)
		cbar = fig.colorbar(img, ax=ax, shrink=0.65)
		cbar.set_label("Suppressed")

		title = "Reliability heatmap for work x income cells"
		suppressed_share = float(np.nanmean(matrix))
		caption = (
			f"Shows where state work/income hardship estimates are suppressed under current reliability rules. "
			f"In cycle {FOCUS_CYCLE}, {suppressed_share:.1%} of cells are suppressed."
		)
		source = "Source: HPS state work/income aggregates with suppression flags (processed export)."
		self.save_chart(fig, "20_reliability_heatmap_work_income.png", title, caption, source)

	def chart_cycle8_marked_national_trends(self) -> None:
		us = self.hps[(self.hps["state_fips"] == "US") & (self.hps["dimension"] == "all")].sort_values("cycle")
		metrics = [
			("hardship", "Expense difficulty"),
			("lonely", "Frequent loneliness"),
			("lack_support", "Lack of support"),
			("frequent_anxiety", "Frequent anxiety"),
		]
		fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.8), sharex=True)

		for ax, (metric, label) in zip(axes.ravel(), metrics):
			ax.plot(us["cycle"], us[f"{metric}_pct"], marker="o", color="#287D8E")
			ax.fill_between(us["cycle"], us[f"{metric}_ci90_lower"], us[f"{metric}_ci90_upper"], color="#287D8E", alpha=0.18)
			ax.axvline(8, linestyle="--", color="#666666", linewidth=1)
			ax.set_title(label, loc="left", fontsize=10)
			ax.set_xticks(range(1, 10))
			ax.set_ylim(bottom=0)

		axes[0, 0].set_ylabel("Percent")
		axes[1, 0].set_ylabel("Percent")
		axes[1, 0].set_xlabel("Cycle")
		axes[1, 1].set_xlabel("Cycle")
		axes[0, 1].text(8.1, axes[0, 1].get_ylim()[1] * 0.9, "possible survey change", fontsize=8, color="#666666")

		title = "National outcomes with explicit cycle-8 marker"
		caption = "Adds a visual warning where missingness shifts sharply, to discourage over-reading cycle-to-cycle movement as demand change."
		source = "Source: U.S. HPS aggregates by cycle (processed export)."
		self.save_chart(fig, "21_national_trends_cycle8_marker.png", title, caption, source)

	def chart_unemployment_hardship_quadrants(self) -> None:
		part = self.joined[self.joined["cycle"] == FOCUS_CYCLE].copy()
		x = part["laus_aligned_unemployment_rate_pct"]
		y = part["hardship_pct"]
		x_med = float(x.median())
		y_med = float(y.median())

		fig, ax = plt.subplots(figsize=(8.8, 6.2))
		ax.scatter(x, y, s=42, color="#287D8E", alpha=0.85)
		ax.axvline(x_med, color="#777777", linestyle="--", linewidth=1)
		ax.axhline(y_med, color="#777777", linestyle="--", linewidth=1)

		q = part[(part["laus_aligned_unemployment_rate_pct"] <= x_med) & (part["hardship_pct"] >= y_med)]
		for row in q.nlargest(6, "hardship_pct").itertuples():
			ax.annotate(row.state_name, (row.laus_aligned_unemployment_rate_pct, row.hardship_pct), xytext=(5, 5), textcoords="offset points", fontsize=8)

		ax.set_xlabel("Aligned unemployment rate (%)")
		ax.set_ylabel("Hardship (%)")
		ax.set_title("Low unemployment but high hardship quadrant", loc="left", fontsize=11)

		title = "Quadrant view: unemployment is not a need proxy"
		caption = (
			f"Highlights states in the low-unemployment/high-hardship quadrant (n={len(q)} in cycle {FOCUS_CYCLE}), "
			"reinforcing that labor-market rates alone are not a targeting rule."
		)
		source = "Source: joined state-cycle file (processed HPS + aligned LAUS)."
		self.save_chart(fig, "22_unemployment_hardship_quadrants.png", title, caption, source)

	def build_state_profile_html(self, recovery: pd.DataFrame) -> None:
		state_name = self.state_name_map.get(FOCUS_STATE, "Virginia")
		row = recovery.loc[recovery["state_fips"].astype(str).str.zfill(2) == FOCUS_STATE].iloc[0]
		html = [
			"<!doctype html>",
			"<html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>",
			f"<title>Persona profile: {state_name}</title>",
			"<style>body{font:16px/1.5 Segoe UI,Arial,sans-serif;max-width:1100px;margin:28px auto;padding:0 18px;color:#1a2b33} h1,h2{line-height:1.2} img{width:100%;height:auto;border:1px solid #e1e1e1} .grid{display:grid;grid-template-columns:1fr;gap:22px} .card{padding:12px 14px;border:1px solid #ddd;border-radius:8px;background:#fafafa} table{border-collapse:collapse;width:100%} th,td{border:1px solid #ddd;padding:6px 8px;text-align:left}</style>",
			f"<h1>Persona-focused state profile: {state_name}</h1>",
			f"<div class='card'><b>Recovery status:</b> {row['recovery_band']} (2019 to 2024 change: {row['change_2019_2024_pp']:+.1f} pp). ",
			f"Labor force change: {row['labor_force_change_pct']:+.1f}%, employment change: {row['employment_change_pct']:+.1f}%.</div>",
			"<div class='grid'>",
		]

		for filename, title in [
			("17_state_profile_focus.png", "State profile"),
			("18_state_hardship_pct_and_count.png", "Hardship percent and count"),
			("22_unemployment_hardship_quadrants.png", "Unemployment-hardship quadrant"),
			("20_reliability_heatmap_work_income.png", "Reliability map"),
		]:
			html.append(f"<section><h2>{title}</h2><img src='charts/{filename}' alt='{title}'></section>")

		html.extend(
			[
				"</div>",
				"<h2>Notes</h2>",
				"<ul><li>All outputs use already-processed CSV exports only.</li><li>No raw respondent data or new downloads were required.</li><li>Cycle 8 is marked as a possible survey-change point; cause is not confirmed in this file.</li></ul>",
				"</html>",
			]
		)

		(self.output_dir / "state_profile_focus.html").write_text("\n".join(html), encoding="utf-8")

	def write_index_files(self) -> None:
		pd.DataFrame([r.__dict__ for r in self.records]).to_csv(self.output_dir / "chart_captions_round2.csv", index=False)
		summary = {
			"focus_state": FOCUS_STATE,
			"focus_cycle": FOCUS_CYCLE,
			"new_charts": len(self.records),
			"new_tables": ["state_recovery_table_with_flags.csv"],
			"notes": "Generated from processed exports only; no notebook rerun and no external docs required.",
		}
		(self.output_dir / "round2_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

	def run(self) -> None:
		recovery = self.build_recovery_table()
		self.chart_state_profile()
		self.chart_state_hardship_percent_and_counts()
		self.chart_timeline_with_va()
		self.chart_reliability_heatmap()
		self.chart_cycle8_marked_national_trends()
		self.chart_unemployment_hardship_quadrants()
		self.build_state_profile_html(recovery)
		self.write_index_files()
		print(f"Wrote {len(self.records)} charts to {self.chart_dir}")
		print(f"Wrote table: {self.output_dir / 'state_recovery_table_with_flags.csv'}")
		print(f"Wrote profile page: {self.output_dir / 'state_profile_focus.html'}")


if __name__ == "__main__":
	PersonaRound2Builder().run()
