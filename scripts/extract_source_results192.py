"""Specified source-read clinical findings from eleven further originals.

Original cells/headers and file hashes are retained. Malformed values are held,
not repaired. Qualifying selected findings do not certify full extraction.
"""
import csv,json,hashlib,re,html,collections
import xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/extraction192';D.mkdir(exist_ok=True);O=R.parents[1]/'outputs'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src={x['record_id']:x for x in read(R/'data/current_source_availability_187.csv')};reg={x['record_id']:x for x in read(R/'data/current_eligible_evidence_register.csv')};cache={};out=[]
def clean(x):return ' '.join(' '.join(x.itertext()).split())
def table(rid,tid):
 key=(rid,tid)
 if key in cache:return cache[key]
 s=src[rid];p=R/s['source_file'];assert sha(p)==s['source_sha256']
 if p.suffix=='.xml':
  root=ET.parse(p).getroot()
  for e in root.iter():e.tag=e.tag.split('}')[-1]
  t=next(t for t in root.findall('.//table-wrap') if t.get('id')==tid)
  rows=[[clean(c) for c in tr if c.tag in ('td','th')] for tr in t.findall('.//tr')]
  desc=' '.join(clean(e) for e in t.findall('./caption')+t.findall('./table-wrap-foot'))
 else:
  text=p.read_text(encoding='utf-8');tables=list(re.finditer(r'<table\b.*?</table>',text,re.S|re.I));t=tables[int(tid)][0]
  assert len(re.findall(r'<table\b',t,re.I))==1,'Nested HTML table needs separate parser'
  rows=[[' '.join(html.unescape(re.sub('<[^>]+>',' ',c)).split()) for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',tr,re.S|re.I)] for tr in re.findall(r'<tr\b.*?</tr>',t,re.S|re.I)]
  desc='HTML table index is zero-based; text cells decoded from nonnested original table. Headers retained in source packet.'
 cache[key]=(rows,desc);return cache[key]
def norm(x):return x.replace('−','-').replace('·','.').strip()
def interval(text):
 text=norm(text);m=re.fullmatch(r'\s*([+-]?[\d.]+)\s*\(\s*([+-]?[\d.]+)\s*(?:,|–|to)\s*([+-]?[\d.]+)\s*\)',text)
 if not m:return ('','','','Unparsed printed estimate/interval; retain source cells')
 try:
  a,b,c=map(float,m.groups())
 except ValueError:return (m[1],'','','Malformed printed confidence bound; no guessed correction')
 return (m[1],m[2],m[3],'' if b<=a<=c else 'Point outside printed CI; no guessed correction')
def add(rid,tid,line,**kw):
 rows,desc=table(rid,tid);s=src[rid]
 x=dict(record_id=rid,provisional_study_id=reg[rid]['provisional_study_id'],outcome='',exposure='',contrast='',stratum='All',timepoint='',effect_measure='',estimate='',ci_lower='',ci_upper='',p_value='',multiplicity_adjusted_p='',group1_summary='',group2_summary='',unit='',denominator_context='',model='',caution='',quantitative_hold='',original_file=s['source_file'],original_sha256=s['source_sha256'],doi_or_pmid=reg[rid]['doi_or_pmid'],source_url=reg[rid]['source_url'],source_locator=f'Table {tid}; source row {line}, including headers',source_row_cells_json=json.dumps(rows[line-1],ensure_ascii=False),source_table_context=desc,full_report_extraction_complete=False,independent_review='Outstanding',quantitative_synthesis_approved=False)
 x.update(kw);out.append(x);return x
def effect(rid,tid,line,text,**kw):
 point,lo,hi,hold=interval(text);hold='; '.join(x for x in [hold,kw.pop('quantitative_hold','')] if x);return add(rid,tid,line,estimate=point,ci_lower=lo,ci_upper=hi,quantitative_hold=hold,**kw)
# Occupational cohort's actual exercise terms, not radiation dose effects.
for line in [32,33]:
 c=table('PM03222','Tab3')[0][line-1]
 effect('PM03222','Tab3',line,c[-1],outcome='Incident MetS',exposure='Reported exercise frequency',contrast=c[0]+' versus not at all',effect_measure='Poisson relative risk',unit='Relative risk',denominator_context='129802 workers,40369 cases in full cohort; exercise-specific model denominator not established',model='Grouped Poisson risk-factor model in Table3; source Methods describe demographic/occupational/lifestyle factors',caution='Exercise from check-up closest to entry; not radiation-dose or SIR estimate. Some exercise category totals/percentages inconsistent. Exact risk-factor model coding and missingness require verification. Do not infer a radiation model coefficient for exercise.')
# Longitudinal item counts at ages30/35 versus MetS at40; no derived causal OR.
behaviours=[('Having breakfast',46,47,71,72),('Attention to nutritional balance',48,49,73,74),('Walking >1hour/day',50,51,75,76),('Eating too fast',60,61,85,86),('Exercise >twice/week',66,67,91,92)]
rows=table('PM03838','tbl_001')[0]
for exposure,my,mn,fy,fn in behaviours:
 for sex,yes,no in [('Men',my,mn),('Women',fy,fn)]:
  for age,start in [(30,0),(35,3)]:
   p=rows[yes-1][-9:][start+2]
   for line,category in [(yes,'Yes'),(no,'No')]:
    c=rows[line-1];v=c[-9:];assert len(v)==9 and all(re.search(r'\d',v[start+i]) for i in (0,1))
    add('PM03838','tbl_001',line,outcome='MetS status at age40 (Japanese criteria)',exposure=exposure,contrast=category+' versus other response; bivariate counts only',stratum=sex,timepoint=f'Exposure at age{age}; outcome at40',effect_measure='Reported n (%) by later MetS status; no derived OR',p_value=p,group1_summary=v[start+1]+' among later MetS cases',group2_summary=v[start]+' among later noncases',unit='n (%) within later outcome group',denominator_context='Age30 risk set men2342/women656; age35 men3098/women947; item-specific missingness,do not substitute full set N for observed item denominators',model='Table1 categorical comparisons,chi-square footnote; same p shared across Yes/No rows',caution='Age30/35 datasets potentially overlap within single-company workforce; never add Ns. Participant-selection prose internally contradictory. Age40 contemporaneous exposures omitted from this longitudinal selection. Conditional exposure percentages are not incident risks. Prediction AUC/feature importance not a causal effect.')
# Same multivariable logistic model and actual Table6 reference coding.
coding=table('PM04205','Tab6')[0];assert coding[9][2]=='1 = No,2 = Yes'
for line,exposure,ref in [(7,'Salt preference','light'),(8,'Salt preference','light'),(9,'Dairy intake','never (verify omitted regular category)'),(10,'Dairy intake','never (verify omitted regular category)'),(11,'Carbonated beverage intake','never (verify omitted occasional/regular categories)'),(12,'Physical exercise','No (coded1; Yes coded2)'),(14,'Shift-work history','never'),(15,'Shift-work history','never')]:
 c=table('PM04205','Tab5')[0][line-1];text=c[5]+' ('+c[6]+')'
 effect('PM04205','Tab5',line,text,outcome='MetS',exposure=exposure,contrast=c[0]+' versus '+ref,effect_measure='Multivariable logistic OR',p_value=c[4],unit='Odds ratio',denominator_context='1468 oil-company workers aged18–60 with complete questionnaire/examination data; fitted complete-case N to verify',model='Table5 joint logistic model with age,income,BMI,diabetes family history,salt,dairy,carbonated beverages,exercise,smoking,shift history,heat,UA,ALT; candidate entry p<=.05',caution='Cross-sectional predictor-selected model; no causal or treatment inference. Table6 coding preserved. Missing intermediate dietary-category coefficients/reference coding need confirmation. Printed p0.000 is rounded source text,not a probability exactly zero. Company-cohort overlap unresolved.')
# Preserve published null PA and shift coefficients, with coding hold.
for line,exposure in [(14,'Lack of physical activity'),(35,'Shift work')]:
 c=table('PM04560','T1')[0][line-1]
 for j,model in [(5,'Crude'),(6,'Adjusted')]:
  effect('PM04560','T1',line,c[j],outcome='MetS',exposure=exposure,contrast='Yes versus No as table-labelled; direction not certified',effect_measure='Reported logistic OR',model=model+'; Methods demographic/lifestyle adjustment, exact PA/shift covariates not completely specified',unit='Odds ratio',denominator_context='Table1 analytic1297 (257MetS/1040noMetS); initial total1334/1337 conflicting',caution='Table shift total/category counts reversed relative to MetS/nonMetS columns; PA labels and coding require confirmation. Null CIs retained; no protective claim.',quantitative_hold='Exposure direction/coding and denominators require source reconciliation')
# Full time-course component contrasts; source misprints retained.
rows=table('SR141-0108','pone.0160343.t006')[0]
for offset,time in [(0,'0–12weeks'),(12,'13–24weeks'),(24,'0–24weeks'),(36,'25–36weeks follow-up')]:
 for base,outcome,unit in [(6,'Waist circumference','cm'),(8,'Systolic blood pressure','mmHg'),(9,'Diastolic blood pressure','mmHg'),(10,'Triglycerides','mmHg as printed; lipid unit unresolved'),(12,'HDL cholesterol','mmHg as printed; lipid unit unresolved'),(14,'Fasting blood glucose','mmHg as printed; glucose unit unresolved')]:
  line=base+offset;c=rows[line-1]
  x=effect('SR141-0108','pone.0160343.t006',line,c[3],outcome=outcome,exposure='GSLiM lifestyle support',contrast='GSLiM versus comparison,Table6 mean-difference column',timepoint=time,effect_measure='Reported between-group mean difference (not Cohen d)',p_value=c[5],group1_summary=c[1],group2_summary=c[2],unit=unit,denominator_context='Table6ITT n97perarm; LOCF missingness; endpoint fitted N requires confirmation',model='Repeated-measures ANOVA; column4 mean difference,column5 Cohen d,column6 p; not within-group stars',caution='Open behavioural intervention; LOCF; multiple phases/endpoints overlap. Mean differences do not consistently equal simple arm-change subtraction; model/contrast confirmation required. Printed lipid/glucose units mmHg not silently changed. 0–24weekDBP lower bound printed -3.4.1,retained unresolved.')
  if 'unit unresolved' in unit:x['quantitative_hold']='Printed clinical unit unresolved; '+x['quantitative_hold']
# Percent changes from log models, never describe as centimetres.
c=table('SR141-0183','Tab3')[0][9]
for col,time in [(3,'6months'),(7,'12months')]:
 x=effect('SR141-0183','Tab3',10,c[col].replace('%',''),outcome='Waist circumference',exposure='Go! hospital environmental/behaviour programme',contrast='Intervention versus clinic comparison change',timepoint=time,effect_measure='Between-group percent change from log-transformed waist analysis',p_value=c[col+1],unit='Percent change,not cm or percentage points',denominator_context='Baseline407intervention/93comparison; eligibility exclusions andmultiple imputation; fitted waist Nnotestablished',model='Covariate-adjusted multiply imputed repeated measures; age,sex,education,income,smoking,jobcategory,jobflexibility,weightgoal,medications',caution='Nonrandomized unequal worksite groups andbaseline differences. Natural-log waist analysis; percentage change notabsolute cm. Six-month comparison favoured comparison arm; twelve-month CIincludes0.')
# HTML original: availability effect only, not participation/LATE column.
rows=table('SR141-0219','2')[0]
for line,outcome,unit in [(5,'HDL cholesterol','mg/dL'),(6,'Glucose (fasting status not confirmed here)','mg/dL'),(8,'Systolic blood pressure','mmHg'),(9,'Diastolic blood pressure','mmHg'),(13,'Low HDL (<40mg/dL)','Percentage points'),(14,'Hypertension >=140/90mmHg','Percentage points')]:
 c=rows[line-1]
 effect('SR141-0219','2',line,c[3],outcome=outcome,exposure='Worksite wellness programme availability',contrast='Treatment versus control programme availability; population with available biometric data',timepoint='18months',effect_measure='Programme-availability difference (not participant LATE)',p_value=c[4],multiplicity_adjusted_p=c[5],group1_summary=c[1],group2_summary=c[2],unit=unit,denominator_context='32974 administrative employees is not biometric analysis N; voluntary biometrics/endpoint Ns require verification',model='Primary availability column in original clinical outcomes table; adjusted p copied separately; local participation effect excluded',caution='Cluster-randomized worksite programme; selective biometrics participation. Preserve correction notice. Low-HDL cutoff<40bothsexes andhypertension140/90 differ from someMetScriteria; glucose fasting status needs confirmation. No syndrome diagnosis inferred.')
# Active versus active intervention, Model I and weight-adjusted Model III.
for line,offset,outcomes in [(4,0,['Systolic blood pressure','Diastolic blood pressure']),(9,0,['Triglycerides'])]:
 c=table('SR141-0230','tbl4')[0][line-1]
 for k,outcome in enumerate(outcomes):
  for j,model in [(1+3*k,'ModelI'),(3+3*k,'ModelIII (includes body-weight change)')]:
   effect('SR141-0230','tbl4',line,c[j],outcome=outcome,exposure='Diet-plus-exercise programme',contrast='Diet-plus-exercise versus exercise-only',timepoint='3months',effect_measure='Adjusted linear coefficient for pre-minus-post change',unit='mmHg' if 'pressure' in outcome else 'Clinical unit per original report; confirm before pooling',denominator_context='904workers:213diet-plus-exercise and691exercise; endpoint regression Ns notestablished',model=model+'; age,sex,smoking,alcohol,regular exercise,MetS adjustment',caution='Self-selected programmes across14factories; no untreated control. Delta=preminuspost so sign is not postminuspre. ModelIII weight-change adjustment is not same estimand asModelI; no independent sample counts.')
# Walking trial: within-arm changes; no invented group-by-time coefficient.
rows=table('SR141-0243','Tab3')[0]
for line,time in [(6,'12weeks'),(7,'12weeks'),(8,'12weeks'),(15,'24weeks'),(16,'24weeks'),(17,'24weeks')]:
 c=rows[line-1];outcome={'WC':'Waist circumference','SBP':'Systolic blood pressure','DBP':'Diastolic blood pressure'}[c[0]]
 for j,group in [(3,'Intervention'),(7,'Control')]:
  x=effect('SR141-0243','Tab3',line,c[j],outcome=outcome,exposure='Pedometer walking programme',contrast=group+' within-arm change only',timepoint=time,effect_measure='Within-arm change as printed (not between-arm effect)',p_value=c[j+1],group1_summary=c[j-2],group2_summary=c[j-1],unit='cm' if c[0]=='WC' else 'mmHg',denominator_context='29randomizedperarm;53completed;five missing replaced by groupmeans',model='Source table within-group estimates; not group*time coefficient',caution='Feasibility trial; mean imputation; multiple outcomes. Some source CIs include0 while reported p<.05; retain conflicts. No clinical efficacy inference from within-arm change. Baseline/follow-up means may not exactly subtract to printed change.')
  if x['ci_lower'] and float(x['ci_lower'])<=0<=float(x['ci_upper']) and float(x['p_value'])<.05:x['quantitative_hold']='Printed within-arm CI includes0 but p<.05; no correction inferred'
# Completers main/subgroup separate, with endpoint-specific Ns.
rows=table('SR141-0258','table2')[0]
for line,outcome,time,unit in [(6,'Waist circumference','16weeks','cm'),(7,'Waist circumference','38weeks','cm'),(8,'Systolic blood pressure','16weeks','mmHg'),(9,'Systolic blood pressure','38weeks','mmHg'),(10,'Diastolic blood pressure','16weeks','mmHg'),(11,'Diastolic blood pressure','38weeks','mmHg')]:
 c=rows[line-1]
 for j,group,nidx in [(8,'Main SoSu-life group',2),(10,'Weight-loss pledge subgroup',4)]:
  effect('SR141-0258','table2',line,c[j],outcome=outcome,exposure='Web/app SoSu-life programme',contrast=group+' versus shared control',timepoint=time,effect_measure='Adjusted between-group difference,completers',p_value=c[j+1],group1_summary=c[nidx+1],group2_summary=c[7],unit=unit,denominator_context='Reported endpoint n='+c[nidx]+' active and'+c[6]+' control; subgroup nested,not separate trial',model='Multilevel mixed-effects linear regression with municipality random effect; completers analysis,notITT',caution='20nursinghomes allocated12/8; municipality rather than eachhome as statedrandom effect. Attrition andvoluntarypledges; weight-loss subgroupselfselected. Waistanalysisexcludessmokingpledges perfootnote; exactmodel/covariates andclusterstructure requireconfirmation. DistinctNsretained.')
# Peer-modelling pilot: pre/post means, not unreported treatment differences.
rows=table('SR141-0264','2')[0]
for line,outcome in [(11,'Glucose (fasting status to verify)'),(13,'Triglycerides'),(15,'HDL cholesterol')]:
 c=rows[line-1]
 for j,group,n in [(1,'Attention control',23),(6,'Intervention',17)]:
  add('SR141-0264','2',line,outcome=outcome,exposure='Peer-modelling physical activity programme',contrast=group+' descriptive pre/post only',effect_measure='Pre/post means andSD; no inferred between-group effect',group1_summary=c[j]+' (SD '+c[j+1]+') baseline',group2_summary=c[j+2]+' (SD '+c[j+3]+') follow-up',unit='mg/dL',denominator_context=f'{n}completers in this group; initial24control/26intervention',model='Original descriptive outcomes table; no source p/CI in selected cells',caution='Pilot with unequal completion; no calculated pairedSE orsyntheticgroupcontrast. HDLdecreased inintervention; notuniversal favourablelipid effect. Fastingstatus andtrialfamily requireverification.')
assert len(out)==122 and len({x['record_id'] for x in out})==11
for x in out:
 if x['ci_lower'] and not x['quantitative_hold']:assert float(x['ci_lower'])<=float(x['estimate'])<=float(x['ci_upper'])
for base in [R/'data',O]:
 with (base/'source_read_clinical_results_192.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
packets=[dict(record_id=rid,table_id=tid,rows=rows,caption_and_footnotes=desc,original_file=src[rid]['source_file'],original_sha256=src[rid]['source_sha256']) for (rid,tid),(rows,desc) in cache.items()]
(D/'original_table_packets.json').write_text(json.dumps(packets,indent=2,ensure_ascii=False),encoding='utf-8')
old=read(R/'data/current_numeric_extraction_audit_188.csv')+read(R/'data/source_read_clinical_results_191.csv');covered={x['record_id'] for x in old+out};remaining=sorted(set(reg)-covered)
with (O/'remaining_numeric_coverage_192.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['record_id','title','status']);w.writeheader();w.writerows(dict(record_id=rid,title=reg[rid]['title'],status='No rows in audited188/191/192 result ledgers; not proof of no extraction elsewhere') for rid in remaining)
status=dict(new_specified_clinical_rows=len(out),new_reports_with_specified_rows=len({x['record_id'] for x in out}),new_rows_by_report=dict(collections.Counter(x['record_id'] for x in out)),reports_with_rows_across_audit188_191_192=len(covered),reports_without_rows_in_these_sources=len(remaining),original_source_hashes_verified=len({rid for rid,tid in cache}),explicit_quantitative_hold_rows=sum(bool(x['quantitative_hold']) for x in out),full_extraction_certified=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
