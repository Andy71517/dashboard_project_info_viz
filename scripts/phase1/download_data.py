"""Download the audited official inputs with SHA-256 verification.
Usage: python download_data.py --raw-dir data/raw [--scope all]
Default scope includes the 9 HPS 2024 files, BLS inputs, and two BRFSS audit files.
The complete --scope all also downloads historical HPS samples and documentation.
No API key or private information is needed.
"""
from pathlib import Path
import argparse,json,hashlib,urllib.request,time

REQUIRED={'la.data.2.AllStatesU','la.data.3.AllStatesS','la.series','la.measure','la.area','la.footnote','LLCP2019ASC.zip','LLCP2025ASC.ZIP','codebook25_llcp-v2-508.zip'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,default=Path('data/raw'));p.add_argument('--scope',choices=['analysis','all'],default='analysis');a=p.parse_args();a.raw_dir.mkdir(parents=True,exist_ok=True)
 manifest=json.loads(Path(__file__).with_name('download_manifest.json').read_text(encoding='utf8'))
 results=[]
 for item in manifest:
  name=item['file']
  if a.scope!='all' and not(name in REQUIRED or (name.startswith('HPS_Phase4') and name.endswith('.zip'))):continue
  dest=a.raw_dir/name;url=item['url']
  if not dest.exists():
   for attempt in range(3):
    try:
     req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; UniversityDataResearch/1.0)','Accept':'*/*'})
     with urllib.request.urlopen(req,timeout=180) as r: data=r.read()
     dest.write_bytes(data);break
    except Exception:
     if attempt==2:raise
     time.sleep(2+attempt)
  digest=hashlib.sha256(dest.read_bytes()).hexdigest()
  same=digest==item['sha256']
  results.append({'file':name,'url':url,'sha256':digest,'matches_audited_snapshot':same})
  print(name,'snapshot matches' if same else 'SOURCE CHANGED: re-audit before using')
 (a.raw_dir/'download_verification.json').write_text(json.dumps(results,indent=2))
 if not all(r['matches_audited_snapshot'] for r in results):raise SystemExit('At least one publisher file changed. Preserve the old snapshot and review the new data and documentation.')
if __name__=='__main__':main()
