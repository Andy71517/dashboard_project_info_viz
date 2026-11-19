"""Check Round 1 edge cases against original aggregate inputs, not chart pixels."""
from pathlib import Path
from decimal import Decimal
import csv,json,math

ROOT=Path(__file__).resolve().parents[1]
def rows(p):
    with (ROOT/p).open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))
checks=0
def require(value,message):
    global checks
    assert value,message
    checks+=1
annual={(r['state_fips'],int(r['year'])):r for r in rows('data/processed/laus_state_annual_2019_2024.csv')}
monthly=rows('data/processed/laus_state_month_2019_2024.csv')
for r in rows('reports/round1_followup/state_recovery_table_with_flags.csv'):
    state=r['state_fips'];a,b=annual[(state,2019)],annual[(state,2024)]
    change=Decimal(b['unemployment_rate_pct'])-Decimal(a['unemployment_rate_pct'])
    require(Decimal(r['change_2019_2024_pp'])==change,state+' exact decimal change')
    require((r['published_rate_at_or_below_2019']=='True')==(change<=0),state+' exact recovery')
    expected='Within +/-0.1 pp' if abs(change)<=Decimal('.1') else 'Below by more than 0.1 pp' if change<0 else 'Above by more than 0.1 pp'
    require(r['rounding_band']==expected,state+' rounding band')
    data=[v for v in monthly if v['state_fips']==state and v['year']=='2020' and v['seasonal']=='S']
    peak=max(Decimal(v['unemployment_rate_pct']) for v in data)
    months=';'.join(f"{int(v['month']):02d}" for v in sorted(data,key=lambda x:int(x['month'])) if Decimal(v['unemployment_rate_pct'])==peak)
    require(Decimal(r['peak_2020_monthly_sa_pct'])==peak and r['peak_2020_months']==months,state+' all peak ties')
    for variable,label in [('employment_persons','employment'),('labor_force_persons','labor_force')]:
        delta=Decimal(b[variable])-Decimal(a[variable])
        require(Decimal(r[label+'_change_persons'])==delta,state+' '+label+' count change')
        require((r['rate_down_but_'+label+'_down']=='True')==(change<0 and delta<0),state+' '+label+' decline flag')

hps=rows('data/processed/hps_2024_aggregates.csv')
suppressed=next(r for r in hps if r['state_fips']=='51' and r['cycle']=='9' and r['dimension']=='work_income' and r['group']=='Worked in last 7 days / Under $50k')
require(suppressed['hardship_valid_n']=='98' and suppressed['hardship_suppressed']=='True' and not suppressed['hardship_pct'],'Virginia n=98 remains missing/suppressed')
all_states=rows('reports/round1_followup/state_hardship_by_cycle.csv')
require(len(all_states)==459 and len({(r['state_fips'],r['cycle']) for r in all_states})==459,'all state-cycle keys preserved')
source={(r['state_fips'],r['cycle']):r for r in rows('data/processed/joined_state_cycle_2024.csv')}
for r in all_states:
    s=source[(r['state_fips'],r['cycle'])]
    for col in ['hardship_pct','hardship_ci90_lower','hardship_ci90_upper','hardship_valid_n','hardship_effective_n','hardship_missing_n','hardship_weighted_numerator']:
        require(math.isclose(float(r[col]),float(s[col]),rel_tol=1e-12,abs_tol=1e-7),str((r['state_fips'],r['cycle'],col)))
require(len(rows('reports/round1_followup/state_work_income_by_cycle.csv'))==51*9*6,'all work/income cells and cycles')
require(len(rows('reports/round1_followup/state_age_by_cycle.csv'))==51*9*3,'all age cells and cycles')
for state in ['06','36','48','51']:
    require(len([r for r in monthly if r['state_fips']==state and r['seasonal']=='S'])==72,'timeline '+state+' not empty')
statuses=rows('personas/round1_request_status.csv')
require(len(statuses)==17,'17 recorded requests')
require(next(r for r in statuses if r['id']=='15')['requested_by'].startswith('Analyst'),'analyst proposal not attributed to personas')
summary=json.loads((ROOT/'reports/round1_followup/summary.json').read_text())
require(summary['round2_persona_responses']=='not generated','no invented Round 2 replies')
print(f'Passed {checks} Round 1 data, rounding, tie, suppression, key and scope checks.')
