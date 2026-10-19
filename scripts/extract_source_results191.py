"""Source-read extraction of specified clinical comparisons from six originals.

No inferred corrections, calculated ORs, independent review, or pooling approval.
The selected source row, cells and original hash travel with every finding.
"""
import csv,json,hashlib,re,collections
import xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/extraction191';D.mkdir(exist_ok=True);O=R.parents[1]/'outputs'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={r['record_id']:r for r in read(R/'data/current_source_availability_187.csv')}
reg={r['record_id']:r for r in read(R/'data/current_eligible_evidence_register.csv')}
roots={};out=[]
def table(rid,tid):
 if rid not in roots:
  s=sources[rid];p=R/s['source_file'];assert sha(p)==s['source_sha256']
  root=ET.parse(p).getroot()
  for e in root.iter():e.tag=e.tag.split('}')[-1]
  roots[rid]=root
 t=next(t for t in roots[rid].findall('.//table-wrap') if t.get('id')==tid)
 return t,[[' '.join(' '.join(c.itertext()).split()) for c in tr if c.tag in ('td','th')] for tr in t.findall('.//tr')]
def add(rid,tid,row,**kw):
 t,rows=table(rid,tid);c=rows[row-1];s=sources[rid]
 item=dict(record_id=rid,provisional_study_id=reg[rid]['provisional_study_id'],effect_measure='',outcome='',exposure='',contrast='',stratum='All',estimate='',ci_lower='',ci_upper='',se='',p_value='',group1_summary='',group2_summary='',unit='',denominator_context='',model='',caution='',original_file=s['source_file'],original_sha256=s['source_sha256'],source_locator=f'{tid}; XML table row {row} (including header rows)',source_row_cells_json=json.dumps(c,ensure_ascii=False),source_caption=' '.join(' '.join(e.itertext()).strip() for e in t.findall('./caption')),source_footnotes=' '.join(' '.join(e.itertext()).strip() for e in t.findall('./table-wrap-foot')),field_verification='Specified cells and clinical contrast inspected in original XML; full report extraction incomplete',independent_review='Outstanding',quantitative_synthesis_approved=False)
 item.update(kw);item['doi_or_pmid']=reg[rid]['doi_or_pmid'];item['source_url']=reg[rid]['source_url'];out.append(item);return c
def norm(x):return x.replace('·','.').replace('−','-').replace(' ','')
# GEE treatment-by-time contrasts, not intervention-arm change scores.
for row,outcome,unit,point,lo,hi in [(5,'Waist circumference','cm','-1.501','-4.052','1.049'),(9,'Systolic blood pressure','mmHg','-2.453','-6.289','1.382'),(13,'Diastolic blood pressure','mmHg','-0.620','-3.181','1.941'),(21,'HDL cholesterol','mg/dL','-5.055','-7.805','-2.306'),(29,'Triglycerides','mg/dL','-16.281','-38.565','6.003'),(33,'Fasting blood glucose','mg/dL','-1.714','-9.417','5.990')]:
 c=table('PM00201','Tab4')[1][row-1];assert [norm(c[i]) for i in (1,4,5)]==[point,lo,hi]
 add('PM00201','Tab4',row,effect_measure='GEE intervention*time coefficient',outcome=outcome,exposure='Healthy lifestyle education',contrast='Intervention*time; intervention coded 1 vs control 0',estimate=point,ci_lower=lo,ci_upper=hi,se=norm(c[2]),p_value=norm(c[3]),unit=unit,denominator_context='226 allocated 113/113; 207 retained 105/102; fitted endpoint N not separately established',model='Gaussian identity GEE, unstructured correlation, robust SE; reported adjustment age,sex,marital status,work experience,income,education,background diabetes/hypertension/cholesterol',caution='Two geographical allocation clusters,one per arm; recruitment after allocation; loss-to-follow-up exclusions conflict with ITT claim. Cluster-level treatment variance not independently established. HDL decrease is adverse direction. Table2 within-arm changes are not these effects. Exact follow-up duration/coding requires reconciliation with intervention dates.')
# Retain null PA comparison; vitamin D blood-level models are not dietary effects.
for row,level in [(26,'Low (<600 MET-min/week)'),(27,'Moderate/high (>=600 MET-min/week)')]:
 c=table('PM00823','Tab2')[1][row-1]
 for stratum,j,p in [('All',1,'0.698'),('Men',4,'0.477'),('Women',7,'0.841')]:
  no=int(c[j].split()[0]);yes=int(c[j+1].split()[0])
  add('PM00823','Tab2',row,effect_measure='MetS cases and noncases as reported; no derived OR',outcome='NCEP-ATP III MetS',exposure='IPAQ short-form activity level',contrast=level,stratum=stratum,estimate=str(yes),p_value=p,group1_summary=c[j+1],group2_summary=c[j],unit='MetS cases',denominator_context=f'{yes} cases + {no} noncases = {yes+no} in this activity/sex stratum; whole sample344',model='Unadjusted categorical PA comparison; reported chi-square/Fisher testing; p is shared across two PA categories in each sex stratum',caution='Cross-sectional volunteer employees; no adjusted PA estimate. Denominators shown are sums of reported case/noncase counts. Both categories and all/sex strata overlap; no independent study counts. Serum vitamin-D findings not substituted for dietary intake.')
assert out[-6]['estimate']=='54' and out[-3]['estimate']=='27'
# Worker joint categories only. Full fitted model includes nonworkers.
for row in [3,4,6,8,9,10,11]:
 c=table('PM00934','Tab3')[1][row-1]
 assert 'Unemployed' not in c[0]
 for stratum,j in [('All',1),('Men',3),('Women',5)]:
  bounds=re.fullmatch(r'\(([0-9.]+)–([0-9.]+)\)',c[j+1]);assert bounds
  add('PM00934','Tab3',row,effect_measure='Adjusted OR',outcome='IDF MetS (Korean WC90/85cm)',exposure='Joint occupation and total daily sitting category',contrast=c[0]+' versus agriculture/forestry/fishery and sitting<=7h/day',stratum=stratum,estimate=c[j],ci_lower=bounds[1],ci_upper=bounds[2],unit='Odds ratio',denominator_context='Full model4303 adults includes1831 nonworkers; individual joint-category fitted Ns not reported here; not a worker-only fitted model',model='Adjusted age,household income,education,physical activity,energy intake,depressive symptoms,smoking,alcohol,chronic diseases; Table3',caution='Joint category varies occupation and sitting simultaneously; not a pure within-occupation sitting effect. Total sitting is not isolated workplace sitting. Survey weighting not established by reported Methods. Table3 used where narrative differs. KNHANES companion independence unresolved; all/sex strata overlap.')
# Secondary physical-activity association, not cortisol/meal efficacy.
for row in [46,47,48,49]:
 c=table('PM01015','T2')[1][row-1]
 add('PM01015','T2',row,effect_measure='Mean (SD) MetS component count',outcome='Number of modified NCEP/AHA MetS components',exposure='Self-reported physical activity intensity',contrast=c[0]+' as labelled; quartile association',estimate=c[3],p_value='0.2112',group1_summary=c[3]+' (SD '+c[4]+')',unit='Component count',denominator_context='Quartile n='+c[1]+'; 373 currently employed police officers with complete cortisol/MetS data',model='Unadjusted descriptive activity categories; Table2 footnote specifies test for trend; same trend p shared across quartiles',caution='Cross-sectional secondary confounder-screening comparison. Activity-intensity units/instrument insufficiently documented; do not substitute Table1 activity/week METS. Quartile means are not intervention effects or adjusted contrasts. BCOPS cohort overlap unresolved. Cortisol response/protein challenge not used as diet efficacy.')
# Primary medication-free current/recent night-shift group, not former workers.
for row in [3,4,8,11,13]:
 c=table('PM02520','Tab3')[1][row-1]
 add('PM02520','Tab3',row,effect_measure='Reported group means and MANCOVA group p',outcome=c[0],exposure='Current/recent night-shift work',contrast='PRESENT versus age/sex-matched NEVER; medication-free subset',p_value=c[3],group1_summary=c[1],group2_summary=c[2],unit='mmHg' if row in [3,4] else 'mg/dL',denominator_context='69 PRESENT and69 matched NEVER without relevant medication; PRESENT includes within preceding year',model='MANCOVA with age covariate and sex/group factors; Bonferroni comparisons; group p from column4,not sex*group p from column5',caution='No SD/SE/CI for selected means in this table; no calculated standardized effect. Never-shift comparator employment not established; PRESENT includes previous-year exposure. Matching and source control-count discrepancies unresolved. Former-worker and125-per-group sensitivity estimates not substituted. No equivalence conclusion from nonsignificant p.')
c=table('PM02602','medicina-55-00186-t002')[1][9];assert c==['Fasting glucose (mg/dL)','94.7 ± 5.4','87.3 ± 6.2','<0.001']
add('PM02602','medicina-55-00186-t002',10,effect_measure='Reported group mean (SD); no adjusted clinical effect',outcome='Fasting glucose',exposure='Healthcare rotating/night-shift work >=5years',contrast='137 shift versus135 nonshift healthcare workers',p_value='<0.001',group1_summary=c[1],group2_summary=c[2],unit='mg/dL',denominator_context='137 shift and135 nonshift; selected disease/medication-free sample272',model='Unadjusted two-group t-test; Methods describe means/SD and tests; do not substitute HOMA-IR predicting employment regression',caution='Cross-sectional; diabetes/systemic disease/medication exclusions; blood collected >=3days after last night shift. Glucose is eligible component; insulin/HOMA-IR are not substituted as syndrome effects. No causal inference.')
assert len(out)==43 and len({x['record_id'] for x in out})==6
for x in out:
 if x['ci_lower']:
  assert float(x['ci_lower'])<=float(x['estimate'])<=float(x['ci_upper'])
  if x['effect_measure']=='Adjusted OR':assert float(x['ci_lower'])>0
for p in [R/'data/source_read_clinical_results_191.csv',O/'source_read_clinical_results_191.csv']:
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
prior=read(R/'data/current_numeric_extraction_audit_188.csv');covered={x['record_id'] for x in prior}|{x['record_id'] for x in out}
remaining=sorted(set(reg)-covered)
with (O/'remaining_numeric_coverage_191.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['record_id','title','status']);w.writeheader();w.writerows(dict(record_id=rid,title=reg[rid]['title'],status='No rows in14 audited ledgers or191 specified findings; not proof of no extraction elsewhere') for rid in remaining)
status=dict(new_specified_clinical_rows=len(out),new_reports_with_specified_rows=len({x['record_id'] for x in out}),new_rows_by_report=dict(collections.Counter(x['record_id'] for x in out)),reports_with_rows_across_audit188_and191=len(covered),reports_without_rows_in_these_sources=len(remaining),original_source_hashes_verified=len(roots),full_extraction_certified=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
