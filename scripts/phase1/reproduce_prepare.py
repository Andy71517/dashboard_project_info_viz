"""Audit public source files; create aggregate-only research samples.
Python 3.12; dependencies: numpy, pandas. See README for download instructions.
"""
from pathlib import Path
import argparse,zipfile,json,re,io,unicodedata,csv
from html.parser import HTMLParser
import numpy as np
import pandas as pd

PERIODS={1:('2024-01-09','2024-02-05'),2:('2024-02-06','2024-03-04'),3:('2024-03-05','2024-04-01'),4:('2024-04-02','2024-04-29'),5:('2024-04-30','2024-05-27'),6:('2024-05-28','2024-06-24'),7:('2024-06-25','2024-07-22'),8:('2024-07-23','2024-08-19'),9:('2024-08-20','2024-09-16')}
METRICS={'hardship':('EXPNS_DIF',[1,2,3,4],[3,4]),'lonely':('SOCIAL2',[1,2,3,4,5],[1,2]),'lack_support':('SOCIAL1',[1,2,3,4,5],[3,4,5]),'frequent_anxiety':('ANXIOUS',[1,2,3,4],[3,4])}
SELECT=['SCRAM','CYCLE','WEEK','EST_ST','REGION','EST_MSA','PWEIGHT','HWEIGHT','TBIRTH_YEAR','ABIRTH_YEAR','INCOME','EEDUC','ANYWORK','EXPNS_DIF','SOCIAL1','SOCIAL2','FDBENEFIT1','FOODSTMP','ANXIOUS','WORRY','INTEREST','DOWN','WRKLOSSRV','WRKLOSS']

class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['style','script']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['style','script']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d.strip())

def jsonwrite(path,obj):path.write_text(json.dumps(obj,indent=2,default=str,allow_nan=False),encoding='utf8')
def numeric_json(x):
 if pd.isna(x):return None
 return float(x) if isinstance(x,(np.floating,float)) else int(x)
def metric_row(d,w,rw=None):
 row={'sample_n':len(d)}
 for metric,(var,validcodes,yescodes) in METRICS.items():
  if var not in d:continue
  valid=d[var].isin(validcodes).to_numpy() & np.isfinite(w) & (w>0)
  yes=d[var].isin(yescodes).to_numpy() & valid
  den=float(w[valid].sum()); num=float(w[yes].sum()); n=int(valid.sum())
  p=num/den if den else np.nan
  neff=den**2/float((w[valid]**2).sum()) if den else 0
  # A project rule, not an official NCHS reliability certification.
  suppress=n<100 or neff<30
  row.update({metric+'_valid_n':n,metric+'_missing_n':len(d)-n,metric+'_effective_n':neff,metric+'_weighted_denominator':den,metric+'_weighted_numerator':np.nan if suppress else num,metric+'_pct':np.nan if suppress else 100*p,metric+'_suppressed':suppress})
  if rw is not None:
   rden=rw[valid].sum(axis=0);rnum=rw[yes].sum(axis=0)
   rp=np.divide(rnum,rden,out=np.full(80,np.nan),where=rden>0)
   se=float(np.sqrt((4/80)*np.sum((rp-p)**2))) if np.isfinite(rp).all() else np.nan
   row[metric+'_se_pp']=np.nan if suppress else 100*se
   row[metric+'_ci90_lower']=np.nan if suppress else max(0,100*(p-1.645*se))
   row[metric+'_ci90_upper']=np.nan if suppress else min(100,100*(p+1.645*se))
 return row

def hps_audit(raw,out,audit):
 records=[]; missing=[]; schemas={}; presence=[]; estimates=[]; repchecks=[]
 for path in sorted(list(raw.glob('HPS_*.zip'))+list(raw.glob('HTOPS_*.zip'))):
  with zipfile.ZipFile(path) as z:
   names=[n for n in z.namelist() if n.lower().endswith('.csv') and 'repwgt' not in n.lower() and 'repweight' not in n.lower()]
   if not names:continue
   n=names[0]
   with z.open(n) as f:header=pd.read_csv(f,nrows=0).columns.tolist()
   with z.open(n) as f:d=pd.read_csv(f,usecols=lambda c:c in SELECT,dtype={'SCRAM':'string'},low_memory=False)
   schemas[path.name]={'inner_file':n,'columns':header,'selected_dtypes':{k:str(v) for k,v in d.dtypes.items()}}
   count=len(d); cycle=int(d.CYCLE.iloc[0]) if 'CYCLE' in d else None
   row={'archive':path.name,'inner_file':n,'measured_rows':count,'columns':len(header),'states':int(d.EST_ST.nunique()) if 'EST_ST' in d else None,'cycle':cycle}
   records.append(row)
   for var in ['EXPNS_DIF','SOCIAL1','SOCIAL2','ANYWORK','INCOME','FDBENEFIT1','FOODSTMP','TBIRTH_YEAR','EST_ST','PWEIGHT','HWEIGHT']:
    presence.append({'archive':path.name,'variable':var,'present':var in header})
    if var not in d:continue
    s=d[var];freq={str(k):int(v) for k,v in s.value_counts(dropna=False).sort_index().items()}
    valid={'EXPNS_DIF':range(1,5),'SOCIAL1':range(1,6),'SOCIAL2':range(1,6),'ANYWORK':[1,2],'INCOME':range(1,9),'FDBENEFIT1':[1,-99]}.get(var)
    missing.append({'archive':path.name,'variable':var,'dtype':str(s.dtype),'rows':count,'blank_n':int(s.isna().sum()),'negative_n':int((pd.to_numeric(s,errors='coerce')<0).sum()),'outside_valid_codes_n':int((~s.isin(valid)).sum()) if valid else None,'observed_counts':json.dumps(freq) if s.nunique()<100 else json.dumps({'min':numeric_json(s.min()),'max':numeric_json(s.max())})})
   if 'Phase4' not in path.name:continue
   assert set(METRICS[m][0] for m in METRICS)<=set(d)
   assert d.SCRAM.is_unique and d.EST_ST.notna().all()
   repname=next(n for n in z.namelist() if 'repwgt' in n.lower())
   with z.open(repname) as f:rh=pd.read_csv(f,nrows=0).columns.tolist()
   rwcols=[c for c in rh if re.fullmatch(r'PWEIGHT\d+',c)]
   assert len(rwcols)==80,(repname,rh)
   with z.open(repname) as f:r=pd.read_csv(f,usecols=['SCRAM']+rwcols,dtype={'SCRAM':'string'})
   assert r.SCRAM.is_unique
   j=d.merge(r[['SCRAM']],on='SCRAM',how='left',validate='one_to_one',indicator=True)
   assert j['_merge'].eq('both').all()
   repchecks.append({'cycle':cycle,'respondent_rows':count,'replicate_rows':len(r),'matched':len(j),'unmatched':int(j['_merge'].ne('both').sum()),'replicate_weights':80})
   d=j.drop(columns='_merge'); w=d.PWEIGHT.to_numpy(float);rw=r.set_index('SCRAM').loc[d.SCRAM,rwcols].to_numpy(float)
   assert np.isfinite(w).all() and (w>0).all() and np.isfinite(rw).all() and (rw>=0).all()
   age=2024-d.TBIRTH_YEAR
   dimensions={
    'all':pd.Series('All adults',index=d.index),
    'age':pd.Series(np.select([age.between(18,34),age.between(35,64),age>=65],['18-34','35-64','65+'],default='Unknown'),index=d.index),
    'work':d.ANYWORK.map({1:'Worked in last 7 days',2:'Did not work in last 7 days'}).fillna('Unknown'),
    'income':pd.Series(np.select([d.INCOME.isin([1,2,3]),d.INCOME.isin([4,5]),d.INCOME.isin([6,7,8])],['Under $50k','$50k-$99,999','$100k+'],default='Unknown'),index=d.index),
    'hardship':pd.Series(np.select([d.EXPNS_DIF.isin([3,4]),d.EXPNS_DIF.isin([1,2])],['Somewhat/very difficult','Not at all/a little difficult'],default='Unknown'),index=d.index),
    'support':pd.Series(np.select([d.SOCIAL1.isin([1,2]),d.SOCIAL1.isin([3,4,5])],['Always/usually support','Sometimes/rarely/never support'],default='Unknown'),index=d.index)
   }
   dimensions['work_income']=dimensions['work']+' / '+dimensions['income']
   # National totals are direct PWEIGHT estimates, never averages of state percentages.
   for dim,groups in dimensions.items():
    for state in ['US']+sorted(d.EST_ST.astype(int).unique().tolist()):
     statemask=np.ones(len(d),bool) if state=='US' else d.EST_ST.eq(state).to_numpy()
     for label in sorted(groups.unique()):
      if 'Unknown' in label:continue
      mask=statemask & groups.eq(label).to_numpy()
      if not mask.any():continue
      row={'state_fips':str(state).zfill(2),'cycle':cycle,'start_date':PERIODS[cycle][0],'end_date':PERIODS[cycle][1],'dimension':dim,'group':label}
      row.update(metric_row(d.loc[mask],w[mask],rw[mask]));estimates.append(row)
   print('HPS audited',path.name,count,flush=True)
 pd.DataFrame(records).to_csv(audit/'raw_row_counts.csv',index=False)
 pd.DataFrame(missing).to_csv(audit/'missingness.csv',index=False)
 pd.DataFrame(presence).to_csv(audit/'variable_presence.csv',index=False)
 jsonwrite(audit/'schemas.json',schemas);jsonwrite(audit/'replicate_join_validation.json',repchecks)
 est=pd.DataFrame(estimates);est.to_csv(out/'hps_2024_aggregates.csv',index=False,float_format='%.6f')
 return records,est

def bls_prepare(raw,out,audit):
 series=pd.read_csv(raw/'la.series',sep='\t',dtype=str).map(lambda x:x.strip() if isinstance(x,str) else x)
 series.columns=series.columns.str.strip()
 logs=[];kept=[]
 for season,filename in [('U','la.data.2.AllStatesU'),('S','la.data.3.AllStatesS')]:
  data=pd.read_csv(raw/filename,sep='\t',dtype=str);data.columns=data.columns.str.strip();data=data.map(lambda x:x.strip() if isinstance(x,str) else x)
  data['year']=pd.to_numeric(data.year);data['value']=pd.to_numeric(data.value,errors='coerce')
  m=data.merge(series[['series_id','area_type_code','area_code','measure_code','seasonal','series_title']],on='series_id',how='left',validate='many_to_one',indicator=True)
  assert m['_merge'].eq('both').all()
  state=m.area_type_code.eq('A') & m.area_code.str.startswith('ST')
  sf=m.area_code.str[2:4]
  sel=m[state & ~sf.isin(['72','78','66']) & m.year.between(2019,2025) & m.measure_code.isin(['03','04','05','06'])].copy()
  sel['state_fips']=sel.area_code.str[2:4]
  logs.append({'file':filename,'measured_raw_rows':len(data),'min_year':int(data.year.min()),'max_year':int(data.year.max()),'periods_latest_year':sorted(data.loc[data.year.eq(data.year.max()),'period'].unique().tolist()),'selected_2019_2025_rows':len(sel),'missing_values_selected':int(sel.value.isna().sum()),'selected_footnote_counts':sel.footnote_codes.fillna('').value_counts().to_dict(),'duplicate_keys':int(sel.duplicated(['state_fips','year','period','measure_code']).sum())})
  assert not sel.duplicated(['state_fips','year','period','measure_code']).any()
  missing=sel.value.isna()
  assert (sel.loc[missing,'year'].eq(2025) & sel.loc[missing,'period'].eq('M10') & sel.loc[missing,'footnote_codes'].eq('X')).all()
  p=sel.pivot(index=['state_fips','year','period','seasonal'],columns='measure_code',values='value').reset_index().rename(columns={'03':'unemployment_rate_pct','04':'unemployment_persons','05':'employment_persons','06':'labor_force_persons'})
  p.columns.name=None
  p['incomplete_2025']=p.year.eq(2025)
  p['missing_october_shutdown']=p.year.eq(2025)&p.period.eq('M10')
  # Published count estimates may differ by a person due to rounding.
  p['count_identity_error']=p.employment_persons+p.unemployment_persons-p.labor_force_persons
  assert p.count_identity_error.abs().max()<=2
  kept.append(p)
 allbls=pd.concat(kept,ignore_index=True)
 mon=allbls[allbls.period.ne('M13')].copy(); mon['month']=mon.period.str[1:].astype(int)
 assert len(mon)==51*7*12*2
 mon.to_csv(out/'laus_state_month_2019_2025.csv',index=False)
 annual=allbls[allbls.period.eq('M13')].copy();annual.to_csv(out/'laus_state_annual_2019_2025.csv',index=False)
 assert len(annual)==51*7
 jsonwrite(audit/'bls_validation.json',logs)
 # Day overlap is an explicit alignment approximation: no daily unemployment observed.
 aligned=[];bridges=[]
 u=mon[mon.seasonal.eq('U')]
 for cycle,(start,end) in PERIODS.items():
  dates=pd.date_range(start,end); days=pd.Series(dates.month).value_counts().sort_index()
  for month,ndays in days.items():bridges.append({'cycle':cycle,'year':2024,'month':int(month),'overlap_days':int(ndays),'cycle_days':len(dates),'fraction':ndays/len(dates)})
  for state,g0 in u[u.year.isin([2019,2024])].groupby('state_fips'):
   row={'state_fips':state,'cycle':cycle}
   for year in [2019,2024]:
    g=g0[g0.year.eq(year)].set_index('month');den=0;num=0;emp=0
    for month,ndays in days.items():
     num+=g.loc[month,'unemployment_persons']*ndays
     den+=g.loc[month,'labor_force_persons']*ndays
     emp+=g.loc[month,'employment_persons']*ndays
    prefix='laus_aligned_' if year==2024 else 'laus_2019_same_months_'
    row.update({prefix+'unemployment_rate_pct':100*num/den,prefix+'unemployment_persons':num/len(dates),prefix+'employment_persons':emp/len(dates),prefix+'labor_force_persons':den/len(dates)})
   row['laus_unemployment_change_from_2019_pp']=row['laus_aligned_unemployment_rate_pct']-row['laus_2019_same_months_unemployment_rate_pct']
   aligned.append(row)
 pd.DataFrame(bridges).to_csv(out/'period_month_bridge.csv',index=False)
 return mon,annual,pd.DataFrame(aligned),logs

def brfss_audit(raw,out,audit):
 zipname='codebook25_llcp-v2-508.zip'
 with zipfile.ZipFile(raw/zipname) as z:
  h=Plain();h.feed(z.read(z.namelist()[0]).decode('utf8'));text=unicodedata.normalize('NFKC','\n'.join(h.parts))
 layouts={}
 for match in re.finditer(r'Column:\s*(\d+)(?:\s*[-–]\s*(\d+))?\s*Type of Variable:\s*(Num|Char)\s*SAS Variable Name:\s*(\w+)',text):
  a,b,typ,var=match.groups();layouts[var]=(int(a)-1,int(b or a),typ)
 wanted=['_STATE','FMONTH','MENTHLTH','EMPLOY1','INCOME3','_AGEG5YR','SDLONELY','EMTSUPRT','_LLCPWT','_STSTR','_PSU','_METSTAT','_URBSTAT']
 assert all(k in layouts for k in wanted),(set(wanted)-set(layouts))
 logs=[]
 for year in [2019,2025]:
  p=raw/('LLCP2019ASC.zip' if year==2019 else 'LLCP2025ASC.ZIP')
  cols={k:layouts[k] for k in wanted} if year==2025 else {'_STATE':(0,2,'Num'),'FMONTH':(16,18,'Num'),'MENTHLTH':(103,105,'Num')}
  rows=[];lengths={}
  with zipfile.ZipFile(p) as z:
   inner=z.namelist()[0]
   with z.open(inner) as f:
    for line in f:
     line=line.rstrip(b'\r\n');lengths[len(line)]=lengths.get(len(line),0)+1
     rows.append([line[a:b].decode('ascii').strip() for a,b,t in cols.values()])
  d=pd.DataFrame(rows,columns=cols).apply(pd.to_numeric,errors='coerce')
  valid=d.MENTHLTH.between(1,30)|d.MENTHLTH.eq(88)
  d['mental_days']=d.MENTHLTH.where(valid).replace({88:0})
  rec={'archive':p.name,'year':year,'inner_file':inner,'measured_raw_rows':len(d),'record_lengths':lengths,'state_codes':sorted(d._STATE.astype(int).unique().tolist()),'menthlth_missing_or_invalid_n':int((~valid).sum()),'menthlth_codes':{str(k):int(v) for k,v in d.MENTHLTH.value_counts(dropna=False).items()}}
  if year==2025:
   rec['selected_missing_or_invalid']={v:int((~d[v].isin(codes)).sum()) for v,codes in {'EMPLOY1':range(1,9),'INCOME3':range(1,12),'SDLONELY':range(1,6),'EMTSUPRT':range(1,6)}.items()}
   g=d.groupby('_STATE').apply(lambda x:pd.Series({'sample_n':len(x),'mental_days_valid_n':int(x.mental_days.notna().sum()),'weighted_mean_mental_days':np.average(x.loc[x.mental_days.notna(),'mental_days'],weights=x.loc[x.mental_days.notna(),'_LLCPWT'])}),include_groups=False).reset_index()
   g.rename(columns={'_STATE':'state_fips'}).to_csv(out/'brfss_2025_state_sample.csv',index=False)
  else:
   # A safe representative slice with no respondent IDs or exact interview dates.
   d.head(100)[['_STATE','FMONTH','MENTHLTH','mental_days']].to_csv(out/'brfss_2019_selected_fields_sample.csv',index=False)
  logs.append(rec);print('BRFSS audited',year,len(d),flush=True)
 jsonwrite(audit/'brfss_validation.json',logs);jsonwrite(audit/'brfss_2025_layout_selected.json',{v:layouts[v] for v in wanted})
 return logs

def main():
 p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--audit-dir',type=Path,required=True);a=p.parse_args()
 a.output_dir.mkdir(parents=True,exist_ok=True);a.audit_dir.mkdir(parents=True,exist_ok=True)
 records,est=hps_audit(a.raw_dir,a.output_dir,a.audit_dir)
 mon,annual,aligned,blslog=bls_prepare(a.raw_dir,a.output_dir,a.audit_dir)
 state=est[(est.dimension=='all') & (est.state_fips!='US')]
 j=state.merge(aligned,on=['state_fips','cycle'],how='left',validate='one_to_one',indicator=True)
 assert len(state)==459 and j['_merge'].eq('both').all()
 j.drop(columns='_merge').to_csv(a.output_dir/'joined_state_cycle_2024.csv',index=False,float_format='%.6f')
 groups=est[est.state_fips!='US'].merge(aligned,on=['state_fips','cycle'],how='left',validate='many_to_one',indicator=True)
 assert groups['_merge'].eq('both').all()
 br=brfss_audit(a.raw_dir,a.output_dir,a.audit_dir)
 primaryrows=sum(x['measured_rows'] for x in records if 'Phase4' in x['archive'])
 validation={'hps_2024_raw_rows':primaryrows,'laus_2019_2025_nsa_selected_long_observations':blslog[0]['selected_2019_2025_rows'],'selected_raw_total_without_double_counting_sa':primaryrows+blslog[0]['selected_2019_2025_rows'],'join_left_rows':len(state),'join_right_rows':len(aligned),'joined_rows':len(j),'join_type':'left, one_to_one','unmatched_left':int(j['_merge'].ne('both').sum()),'unmatched_right':len(aligned.merge(state[['state_fips','cycle']],how='left',indicator=True).query('_merge=="left_only"')),'demographic_join_rows':len(groups),'demographic_join_unmatched':int(groups['_merge'].ne('both').sum()),'hps_aggregate_rows':len(est),'brfss_records':sum(x['measured_raw_rows'] for x in br),'privacy':'HPS aggregate-only exports; BRFSS selected-field sample has no ID, birthyear, or exact interview date','causal_claims':False}
 jsonwrite(a.audit_dir/'validation.json',validation);print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
