"""Analytical responses to Round 1; does not generate stakeholder conversations.

This code is also embedded in the Colab notebook for transparent reproduction.
"""
from pathlib import Path
import base64
import html
import json
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

PHASE42_NOTE = ("Cycle 8 starts Phase 4.2. Census added prepaid wireless numbers to the contact frame and warned that response rates and sample composition may change. This does not identify the cause or size of the observed missingness drop. Cycle shifts are not service-demand changes.")
PHASE42_URL = "https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-2_2024_Household_Pulse_Survey_User_Notes_09122024.pdf"
RANK_NOTE = "Order is descriptive. Interval overlap is not a test of equality, difference, or rank. A state and the U.S. estimate share respondents."


def mark_cycle8(ax):
    ax.axvline(7.5, color="#666666", linestyle="--", linewidth=1)
    ax.text(.99,.02,"C8: Phase 4.2 frame change",transform=ax.transAxes,ha="right",va="bottom",fontsize=7,color="#555555",bbox=dict(facecolor="white",alpha=.8,edgecolor="none",pad=1))


class Round1Followup:
    def __init__(self,hps,joined,monthly,annual,missingness,output_dir,focus_state="51",focus_cycle=9):
        self.hps,self.joined,self.monthly,self.annual=[d.copy() for d in [hps,joined,monthly,annual]]
        for data in [self.hps,self.joined,self.monthly,self.annual]:
            data["state_fips"]=data.state_fips.astype(str).str.replace(r"\.0$","",regex=True).str.zfill(2)
        self.missing=missingness.copy()
        self.output=Path(output_dir);self.charts=self.output/"charts"
        self.charts.mkdir(parents=True,exist_ok=True)
        self.state,self.cycle=str(focus_state).zfill(2),int(focus_cycle)
        self.names=self.joined.set_index("state_fips").state_name.to_dict();self.names["US"]="United States"
        self.records=[]
        plt.rcParams.update({"text.parse_math":False,"font.size":10,"axes.spines.top":False,"axes.spines.right":False})

    def save(self,fig,filename,title,caption):
        if filename != "19_unemployment_timeline_with_va.png":
            caption += " Missing HPS answers are excluded per outcome; the accompanying all-cycle tables give valid n, Kish effective n, missing n and suppression flags."
        fig.suptitle(title,x=.03,y=.99,ha="left",fontsize=14,fontweight="bold")
        fig.text(.03,.01,"Sources: Census HPS weighted adults and/or BLS LAUS. HPS error bars: 90% intervals. Read the caption and evidence tables.",fontsize=8)
        fig.tight_layout(rect=(0,.055,1,.945))
        fig.savefig(self.charts/filename,dpi=140,bbox_inches="tight",facecolor="white");plt.close(fig)
        record=dict(file=filename,title=title,caption=caption);self.records.append(record)
        return record

    @staticmethod
    def interval(ax,x,rows,metric,color,label=None):
        usable=rows[metric+"_pct"].notna() & ~rows[metric+"_suppressed"].astype(bool)
        v=rows.loc[usable,metric+"_pct"]
        ax.errorbar(np.asarray(x)[usable],v,yerr=[v-rows.loc[usable,metric+"_ci90_lower"],rows.loc[usable,metric+"_ci90_upper"]-v],fmt="o",capsize=3,color=color,label=label)
        for position in np.asarray(x)[~usable]:ax.text(position,1,"suppressed",rotation=90,va="bottom",ha="center",fontsize=7)

    def tables(self):
        rates=self.annual.pivot(index=["state_fips","state_name"],columns="year",values="unemployment_rate_pct").reset_index()
        rates.columns.name=None
        out=rates[["state_fips","state_name",2019,2020,2024]].rename(columns={2019:"rate_2019_pct",2020:"rate_2020_annual_pct",2024:"rate_2024_pct"})
        tenths=np.rint(out.rate_2024_pct*10).astype(int)-np.rint(out.rate_2019_pct*10).astype(int)
        out["change_2019_2024_pp"]=tenths/10
        out["published_rate_at_or_below_2019"]=tenths.le(0)
        out["exact_published_tie"]=tenths.eq(0)
        out["rounding_band"]=np.select([tenths.lt(-1),tenths.abs().le(1),tenths.gt(1)],
            ["Below by more than 0.1 pp","Within +/-0.1 pp","Above by more than 0.1 pp"],default="check")
        for variable,label in [("employment_persons","employment"),("labor_force_persons","labor_force")]:
            wide=self.annual.pivot(index="state_fips",columns="year",values=variable)
            for year in [2019,2024]:out[f"{label}_{year}_persons"]=out.state_fips.map(wide[year])
            out[label+"_change_persons"]=out[label+"_2024_persons"]-out[label+"_2019_persons"]
            out[label+"_change_pct"]=100*out[label+"_change_persons"]/out[label+"_2019_persons"]
            out["rate_down_but_"+label+"_down"]=tenths.lt(0)&out[label+"_change_persons"].lt(0)
        peaks=[]
        for state,data in self.monthly.loc[self.monthly.year.eq(2020)&self.monthly.seasonal.eq("S")].groupby("state_fips"):
            peak=data.unemployment_rate_pct.max()
            months=data.loc[data.unemployment_rate_pct.eq(peak),"month"].astype(int).sort_values()
            peaks.append(dict(state_fips=state,peak_2020_monthly_sa_pct=peak,peak_2020_months=";".join(f"{m:02d}" for m in months)))
        self.recovery=out.merge(pd.DataFrame(peaks),on="state_fips",validate="one_to_one").sort_values("state_name")
        assert len(self.recovery)==51
        va=self.recovery.loc[self.recovery.state_fips.eq("51")].iloc[0]
        assert va.rounding_band=="Within +/-0.1 pp" and va.change_2019_2024_pp==.1
        self.recovery.to_csv(self.output/"state_recovery_table_with_flags.csv",index=False)
        common=["state_fips","state_name","cycle","start_date","end_date","sample_n"]
        suffixes=["pct","ci90_lower","ci90_upper","valid_n","missing_n","effective_n","suppressed","weighted_numerator","weighted_denominator"]
        state=self.joined[common+["hardship_"+s for s in suffixes]].copy()
        state["hardship_missing_pct"]=100*state.hardship_missing_n/state.sample_n
        state["reliability"]=np.where(state.hardship_suppressed,"suppressed","passes project rule")
        state["estimated_adults_reporting_hardship"]=state.hardship_weighted_numerator
        state["count_uncertainty"]="Point only; requires replicate totals for an interval, not scaled percentage intervals"
        state["displayed_pct_tie_group"]=state.hardship_pct.round(1)
        state["ranking_note"]=RANK_NOTE
        self.state_table=state
        state.to_csv(self.output/"state_hardship_by_cycle.csv",index=False)
        for dim,name in [("work_income","state_work_income_by_cycle.csv"),("age","state_age_by_cycle.csv")]:
            data=self.hps.loc[self.hps.state_fips.ne("US")&self.hps.dimension.eq(dim)].copy()
            data["state_name"]=data.state_fips.map(self.names);data.to_csv(self.output/name,index=False)
        self.hps.loc[self.hps.state_fips.eq(self.state)&self.hps.dimension.isin(["all","work_income","hardship","age"])].to_csv(self.output/"focus_state_estimates.csv",index=False)
        self.hps.loc[self.hps.state_fips.eq("US")&self.hps.dimension.isin(["work_income","hardship","age"])].to_csv(self.output/"national_group_estimates_and_samples.csv",index=False)
        methods=dict(phase42_note=PHASE42_NOTE,phase42_source=PHASE42_URL,source_page=1,
            recovery_rule="Integer tenths of published rates; exact <=0 and separate +/-0.1 display band",
            peak_rule="Maximum 2020 seasonally adjusted monthly rate; all tied months retained",
            ranking_policy=RANK_NOTE,count_intervals="Not estimated from marginal percentage intervals",
            covariance="Absent from aggregate exports; no pairwise or national significance claims",
            project_rule="valid n>=100 and Kish effective n>=30; not a representativeness guarantee",
            rounds="Round 1 follow-up only; Round 2 stakeholder responses not generated")
        (self.output/"methods.json").write_text(json.dumps(methods,indent=2),encoding="utf8")
        return self.recovery

    def chart_profile(self):
        fig,axes=plt.subplots(2,3,figsize=(17,10))
        focus=self.hps.loc[self.hps.state_fips.eq(self.state)]
        for state,color in [("US","#287D8E"),(self.state,"#A25C38")]:
            rows=self.hps.loc[self.hps.state_fips.eq(state)&self.hps.dimension.eq("all")].sort_values("cycle")
            self.interval(axes[0,0],rows.cycle,rows,"hardship",color,self.names[state])
        axes[0,0].set(title="Expense difficulty by cycle",xlabel="2024 collection cycle",ylabel="Adults with hardship (%)",xticks=range(1,10))
        mark_cycle8(axes[0,0]);axes[0,0].legend(fontsize=8,loc="lower left")
        work=focus.loc[focus.cycle.eq(self.cycle)&focus.dimension.eq("work_income")].sort_values("group")
        labels=[r.group.replace(" in last 7 days","")+f"  n={r.hardship_valid_n}" for r in work.itertuples()]
        ax=axes[0,1]
        for i,r in enumerate(work.itertuples()):
            if r.hardship_suppressed:ax.text(1,i,"suppressed (not zero)",va="center",fontsize=8)
            else:
                ax.barh(i,r.hardship_pct,color="#287D8E")
                ax.errorbar(r.hardship_pct,i,xerr=[[r.hardship_pct-r.hardship_ci90_lower],[r.hardship_ci90_upper-r.hardship_pct]],fmt="none",ecolor="black",capsize=3)
        ax.set(yticks=range(len(work)),yticklabels=labels,title=f"Work and 2023 income, C{self.cycle}",xlabel="Adults with hardship (%)")
        ax.tick_params(axis="y",labelsize=7);ax.set_ylim(len(work)-.5,-.5)
        groups=["Not at all/a little difficult","Somewhat/very difficult"]
        social=focus.loc[focus.cycle.eq(self.cycle)&focus.dimension.eq("hardship")].set_index("group").reindex(groups)
        ax=axes[0,2]
        for shift,metric,color,label in [(-.18,"lonely","#287D8E","Frequent loneliness"),(.18,"frequent_anxiety","#A25C38","Frequent anxiety symptoms")]:
            for j,(_,r) in enumerate(social.iterrows()):
                if r[metric+"_suppressed"]:continue
                x=j+shift;v=r[metric+"_pct"]
                ax.bar(x,v,width=.33,color=color,label=label if j==0 else None)
                ax.errorbar(x,v,yerr=[[v-r[metric+"_ci90_lower"]],[r[metric+"_ci90_upper"]-v]],fmt="none",ecolor="black",capsize=3)
                ax.text(x,r[metric+"_ci90_upper"]+1,f"n={int(r[metric+'_valid_n'])}",ha="center",fontsize=7)
        ax.set(xticks=[0,1],xticklabels=["Not at all/a little","Somewhat/very"],title=f"Social outcomes by hardship, C{self.cycle}",ylabel="Adults reporting outcome (%)",xlabel="Expense difficulty group",ylim=(0,45))
        ax.set_ylim(0,np.nanmax(social[["lonely_ci90_upper","frequent_anxiety_ci90_upper"]].to_numpy(float))*1.25)
        ax.legend(fontsize=7,loc="upper left")
        for ax,metric,title in [(axes[1,0],"lonely","Frequent loneliness by age"),(axes[1,1],"lack_support","Lack of needed support by age")]:
            for shift,state,color in [(-.1,"US","#287D8E"),(.1,self.state,"#A25C38")]:
                rows=self.hps.loc[self.hps.state_fips.eq(state)&self.hps.cycle.eq(self.cycle)&self.hps.dimension.eq("age")].set_index("group").reindex(["18-34","35-64","65+"])
                xs=np.arange(3)+shift;self.interval(ax,xs,rows,metric,color,self.names[state])
                for j,(_,r) in enumerate(rows.iterrows()):
                    if not r[metric+"_suppressed"]:ax.annotate(f"n={int(r[metric+'_valid_n'])}",(xs[j],r[metric+"_ci90_upper"]),xytext=(8 if state==self.state else -8,5),textcoords="offset points",fontsize=7,ha="left" if state==self.state else "right",color=color)
            ax.set(xticks=range(3),xticklabels=["18–34","35–64","65+"],xlabel="Approximate age",ylabel="Adults reporting outcome (%)",title=title,ylim=(0,None));ax.legend(fontsize=8)
            ax.set_xlim(-.5,2.5)
        r=self.state_table.loc[self.state_table.state_fips.eq(self.state)&self.state_table.cycle.eq(self.cycle)].iloc[0]
        axes[1,2].axis("off")
        axes[1,2].text(0,.98,f"{self.names[self.state]} · Cycle {self.cycle}\n{r.start_date} to {r.end_date}\n\nHardship valid n={r.hardship_valid_n:,}\nKish effective n={r.hardship_effective_n:.1f}\nMissing expense answer={r.hardship_missing_pct:.1f}%\n\n90% intervals; missing excluded per outcome.\nRule: valid n≥100 and effective n≥30.\nThese are adult population estimates, not clients.\nWork in 7 days ≠ official employment status.\nIncome is 2023 household income.\nSocial measures are not diagnoses or causal effects.\nFull missingness and reliability tables accompany this chart.",va="top",fontsize=10,linespacing=1.6)
        return self.save(fig,"17_state_profile_focus.png",f"{self.names[self.state]} profile with intervals and sample sizes",
            f"Cycle {self.cycle}. Suppressed cells are explicit; reported HPS estimates have 90% intervals and outcome-specific valid n. "+PHASE42_NOTE)

    def chart_counts(self):
        d=self.state_table.loc[self.state_table.cycle.eq(self.cycle)].sort_values("hardship_pct")
        fig,(left,right)=plt.subplots(1,2,figsize=(15,14),sharey=True);y=np.arange(len(d))
        left.errorbar(d.hardship_pct,y,xerr=[d.hardship_pct-d.hardship_ci90_lower,d.hardship_ci90_upper-d.hardship_pct],fmt="o",capsize=2,color="#287D8E")
        left.set(yticks=y,yticklabels=[f"{r.state_name}   n={r.hardship_valid_n}, eff={r.hardship_effective_n:.0f}" for r in d.itertuples()],xlabel="Hardship (%, 90% interval)");left.tick_params(axis="y",labelsize=7)
        right.barh(y,d.estimated_adults_reporting_hardship/1e6,color="#A25C38");right.set_xlabel("Estimated adults (millions; point estimate only)")
        return self.save(fig,"18_state_hardship_pct_and_count.png",f"State hardship percentages and estimated adults · Cycle {self.cycle}",
            RANK_NOTE+" Overall state cells pass the project rule. All 459 cells and their missingness are in state_hardship_by_cycle.csv. Count intervals require replicate totals, not scaled percentage intervals. Counts are not clients, households, or service demand.")

    def chart_timeline(self):
        fig,ax=plt.subplots(figsize=(11,6))
        for state in list(dict.fromkeys(["06","36","48",self.state])):
            d=self.monthly.loc[self.monthly.state_fips.eq(state)&self.monthly.seasonal.eq("S")].copy();assert len(d)==72,(state,len(d))
            ax.plot(pd.to_datetime(d.date),d.unemployment_rate_pct,label=self.names[state])
        ax.set(xlabel="Month, 2019–2024",ylabel="Unemployment rate (%, seasonally adjusted)",xlim=(pd.Timestamp("2019-01-01"),pd.Timestamp("2024-12-01")));ax.legend()
        return self.save(fig,"19_unemployment_timeline_with_va.png","Monthly unemployment including Virginia",
            "Every line contains 72 monthly observations. Peaks use adjusted monthly rates; the recovery table separately reports unadjusted annual averages. BLS uncertainty estimates are absent from these exports.")

    def chart_reliability(self,age=False):
        dim="age" if age else "work_income";metrics=["lonely","lack_support"] if age else ["hardship"]
        d=self.hps.loc[self.hps.cycle.eq(self.cycle)&self.hps.state_fips.ne("US")&self.hps.dimension.eq(dim)]
        states=sorted(self.names.keys()-{"US"},key=lambda x:self.names[x]);columns=[];values=[]
        for metric in metrics:
            for group in sorted(d.group.unique()):
                part=d.loc[d.group.eq(group)].set_index("state_fips").reindex(states)
                values.append(np.where(part[metric+"_suppressed"].isna(),2,np.where(part[metric+"_suppressed"].eq(True),1,0)))
                columns.append(group.replace(" in last 7 days","")+"\n"+metric.replace("_"," "))
        fig,ax=plt.subplots(figsize=(13,12))
        image=ax.imshow(np.array(values).T,aspect="auto",cmap=ListedColormap(["#C5E5E7","#B76847","#DDDDDD"]),vmin=-.5,vmax=2.5)
        ax.set(xticks=range(len(columns)),xticklabels=columns,yticks=range(len(states)),yticklabels=[self.names[s] for s in states]);ax.tick_params(axis="x",labelrotation=25,labelsize=8);ax.tick_params(axis="y",labelsize=7)
        bar=fig.colorbar(image,ax=ax,ticks=[0,1,2],shrink=.6);bar.ax.set_yticklabels(["Passes rule","Suppressed","Absent cell"])
        name="23_reliability_heatmap_age.png" if age else "20_reliability_heatmap_work_income.png"
        return self.save(fig,name,("Age/social outcome" if age else "Work/income hardship")+f" reliability · Cycle {self.cycle}",
            "Rule: valid n≥100 and Kish effective n≥30; not a guarantee of unbiased or precise estimates. All cycles' valid n, effective n, missing n, CIs and flags accompany the chart. Absent, suppressed and reported cells are distinct.")

    def chart_national_trends(self):
        d=self.hps.loc[self.hps.state_fips.eq("US")&self.hps.dimension.eq("all")].sort_values("cycle")
        fig,axes=plt.subplots(2,2,figsize=(12,8))
        for ax,metric in zip(axes.flat,["hardship","lonely","lack_support","frequent_anxiety"]):
            self.interval(ax,d.cycle,d,metric,"#287D8E");mark_cycle8(ax)
            ax.set(title=metric.replace("_"," ").capitalize(),xlabel="2024 collection cycle",ylabel="Adults (%, weighted)",xticks=range(1,10),ylim=(0,None))
        return self.save(fig,"21_national_trends_cycle8_marker.png","National measures with a documented comparability warning",PHASE42_NOTE+" Cross-cycle differences have not been tested with a repeated-response covariance model.")

    def chart_quadrants(self):
        d=self.joined.loc[self.joined.cycle.eq(self.cycle)].copy()
        xm,ym=d.laus_aligned_unemployment_rate_pct.median(),d.hardship_pct.median()
        d["low_unemployment_high_hardship"]=d.laus_aligned_unemployment_rate_pct.le(xm)&d.hardship_pct.ge(ym)
        d[["state_fips","state_name","cycle","laus_aligned_unemployment_rate_pct","hardship_pct","low_unemployment_high_hardship"]].to_csv(self.output/"descriptive_quadrants.csv",index=False)
        fig,ax=plt.subplots(figsize=(11,7));ax.scatter(d.laus_aligned_unemployment_rate_pct,d.hardship_pct,color="#287D8E")
        ax.axvline(xm,linestyle="--",color="#888888");ax.axhline(ym,linestyle="--",color="#888888")
        for r in d.loc[d.low_unemployment_high_hardship].nlargest(5,"hardship_pct").itertuples():ax.annotate(r.state_name,(r.laus_aligned_unemployment_rate_pct,r.hardship_pct),xytext=(4,6),textcoords="offset points",fontsize=8)
        ax.set(xlabel="Aligned unemployment rate (%, unadjusted)",ylabel="Adults with hardship (%, weighted)")
        return self.save(fig,"22_unemployment_hardship_quadrants.png",f"Unemployment and hardship measure different things · Cycle {self.cycle}",
            f"The median-based quadrant contains {int(d.low_unemployment_high_hardship.sum())} jurisdictions. Thresholds are exploratory, not validated need categories or an allocation rule. "+RANK_NOTE)

    def export(self):
        pd.DataFrame(self.records).to_csv(self.output/"chart_captions.csv",index=False)
        table=self.recovery.to_html(index=False,table_id="recovery",float_format=lambda x:f"{x:.3f}",escape=True)
        page=["<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Round 1 follow-up evidence</title><style>body{font:16px/1.5 system-ui;max-width:1350px;margin:30px auto;padding:20px}img{max-width:100%;height:auto}th,td{padding:7px;border:1px solid #ddd;text-align:left}table{border-collapse:collapse;font-size:12px}th{cursor:pointer;background:#e7f0f3}section{margin:35px 0}.scroll{overflow:auto}</style>",
            "<h1>Round 1 follow-up evidence</h1><p>Evidence for the recorded Maya and Jordan requests. No Round 2 replies have been generated here.</p>",
            "<p>"+html.escape(PHASE42_NOTE)+"</p><h2>Sortable recovery table</h2><p>Click a heading to sort. Exact published-rate recovery and the ±0.1 display band are separate. Annual rates are unadjusted; monthly peaks are adjusted. BLS uncertainty estimates are not provided.</p><div class='scroll'>",table,"</div>"]
        for r in self.records:
            encoded=base64.b64encode((self.charts/r["file"]).read_bytes()).decode()
            page.append(f"<section><h2>{html.escape(r['title'])}</h2><img alt='{html.escape(r['title'],quote=True)}' src='data:image/png;base64,{encoded}'><p>{html.escape(r['caption'])}</p></section>")
        page.append("""<script>document.querySelectorAll('#recovery th').forEach((h,k)=>{let asc=true;h.onclick=()=>{const b=document.querySelector('#recovery tbody');const rows=Array.from(b.rows);rows.sort((a,c)=>{const x=a.cells[k].textContent,y=c.cells[k].textContent;const nx=Number(x),ny=Number(y);const d=x.trim()!==''&&y.trim()!==''&&Number.isFinite(nx)&&Number.isFinite(ny)?nx-ny:x.localeCompare(y);return asc?d:-d});rows.forEach(r=>b.appendChild(r));asc=!asc}})</script></html>""")
        (self.output/"state_profile_focus.html").write_text("\n".join(page),encoding="utf8")
        focus=self.hps.loc[self.hps.state_fips.eq(self.state)&self.hps.cycle.eq(self.cycle)&self.hps.dimension.eq("work_income")]
        summary=dict(focus_state=self.state,focus_cycle=self.cycle,charts=len(self.records),state_cycle_rows=len(self.state_table),recovery_states=len(self.recovery),focus_work_income_suppressed=int(focus.hardship_suppressed.sum()),exact_rate_at_or_below_count=int(self.recovery.published_rate_at_or_below_2019.sum()),within_point1_count=int(self.recovery.rounding_band.eq("Within +/-0.1 pp").sum()),round1_followup_analysis="completed",round2_persona_responses="not generated")
        (self.output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf8");return summary

    def run(self):
        self.tables()
        for method in [self.chart_profile,self.chart_counts,self.chart_timeline,self.chart_reliability,self.chart_national_trends,self.chart_quadrants]:method()
        self.chart_reliability(age=True)
        return self.export()


def main(compatibility=False):
    plt.switch_backend("Agg")
    root=Path(__file__).resolve().parents[1]
    load=lambda name:pd.read_csv(root/"data/processed"/name,dtype={"state_fips":str})
    builder=Round1Followup(load("hps_2024_aggregates.csv"),load("joined_state_cycle_2024.csv"),load("laus_state_month_2019_2024.csv"),load("laus_state_annual_2019_2024.csv"),pd.read_csv(root/"audit/step0/hps_missingness.csv"),root/"reports/round1_followup")
    summary=builder.run()
    if compatibility:
        target=root/"reports/step0/persona_round2";target.mkdir(parents=True,exist_ok=True)
        shutil.copytree(builder.charts,target/"charts",dirs_exist_ok=True)
        for name in ["state_profile_focus.html","state_recovery_table_with_flags.csv"]:shutil.copy2(builder.output/name,target/name)
        shutil.copy2(builder.output/"chart_captions.csv",target/"chart_captions_round2.csv")
        (target/"round2_summary.json").write_text(json.dumps({**summary,"preparation_only":True,"canonical_directory":"reports/round1_followup"},indent=2))
    print(json.dumps(summary,indent=2))


if __name__=="__main__":main()
