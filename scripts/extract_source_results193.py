"""Specified original-table findings from eight additional workplace reports.

Preserves statistical scale, time labels, endpoint Ns and source contradictions.
"""
import csv,json,hashlib,collections,re
import xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/extraction193';D.mkdir(exist_ok=True);O=R.parents[1]/'outputs'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src={x['record_id']:x for x in read(R/'data/current_source_availability_187.csv')};reg={x['record_id']:x for x in read(R/'data/current_eligible_evidence_register.csv')};roots={};packets={};out=[]
def clean(e):return ' '.join(' '.join(e.itertext()).split())
def table(rid,tid):
 if rid not in roots:
  p=R/src[rid]['source_file'];assert sha(p)==src[rid]['source_sha256'];root=ET.parse(p).getroot()
  for e in root.iter():e.tag=e.tag.split('}')[-1]
  roots[rid]=root
 key=(rid,tid)
 if key not in packets:
  t=next(t for t in roots[rid].findall('.//table-wrap') if t.get('id')==tid)
  packets[key]=dict(record_id=rid,table_id=tid,rows=[[clean(c) for c in tr if c.tag in ('th','td')] for tr in t.findall('.//tr')],caption=' '.join(clean(e) for e in t.findall('./caption')),footnotes=' '.join(clean(e) for e in t.findall('./table-wrap-foot')),original_file=src[rid]['source_file'],original_sha256=src[rid]['source_sha256'])
 return packets[key]['rows']
def add(rid,tid,line,**kw):
 c=table(rid,tid)[line-1];s=src[rid];p=packets[(rid,tid)]
 x=dict(record_id=rid,provisional_study_id=reg[rid]['provisional_study_id'],outcome='',exposure='',contrast='',stratum='All',timepoint='',effect_measure='',estimate='',ci_lower='',ci_upper='',p_between_groups='',p_group_time='',p_within_group='',p_value='',group1_summary='',group2_summary='',unit='',denominator_context='',model='',caution='',quantitative_hold='',original_file=s['source_file'],original_sha256=s['source_sha256'],doi_or_pmid=reg[rid]['doi_or_pmid'],source_url=reg[rid]['source_url'],source_locator=f'{tid}; XML row {line} including headers',source_row_cells_json=json.dumps(c,ensure_ascii=False),source_caption=p['caption'],source_footnotes=p['footnotes'],full_report_extraction_complete=False,independent_review='Outstanding',quantitative_synthesis_approved=False)
 x.update(kw);out.append(x);return x
# All are shift workers; percentage contrasts do not estimate night versus day.
rid='FC143-00017';tid='jcm-15-04028-t005'
for line in [3,4,5,6]:
 c=table(rid,tid)[line-1]
 for j,sex in [(1,'Men'),(2,'Women')]:
  add(rid,tid,line,outcome='Arterial hypertension',exposure='Years of shift work',contrast=c[0]+' years; descriptive duration category',stratum=sex,effect_measure='Reported hypertension prevalence',estimate=c[j].replace('*','').strip(),unit='Percent',denominator_context='Sex/duration cell denominators not supplied in selected table; all are shift-working HCWs',model='Unadjusted descriptive Table5; stars compare men with women,not duration trend',caution='Cross-sectional age confounding; no day-worker comparator. CUORE composite-risk ORs are not hypertension ORs; no significance assigned to duration trend. Cohort/institution overlap unresolved.')
# Eating-disorder case groups: counts, percentages and prevalence CIs as printed.
rid='FC143-00020';tid='ijerph-22-01221-t002'
for line in range(2,8):
 c=table(rid,tid)[line-1]
 for j,group in [(1,'Eating-disorder cases'),(2,'Other workers')]:
  add(rid,tid,line,outcome=c[0],exposure='EDE-QS eating-disorder case status',contrast=group,effect_measure='Reported count,percentage and percentage CI; not OR',group1_summary=c[j],unit='n (%) and95%CI for percentage',denominator_context='1215participants;63ED cases and1152other nominal workers; endpoint-specific denominator/missingness to verify',model='Unadjusted Pearson chi-square comparison; source significance stars retained,not converted to exact p',caution='Cross-sectional; eating scale screening does not establish causation. Violence/stress regression predicts ED symptoms,not MetS; no model inversion. Some printed percentages may imply endpoint-specific missingness. Other-worker HDL percentage needs denominator check.')
# Matched EMMs and group*time test are distinct from endpoint group p.
rid='FC143-00087';tid='T2'
for first,outcome,unit in [(4,'Systolic blood pressure','mmHg'),(8,'Diastolic blood pressure','mmHg'),(12,'Fasting glucose','mg/dL'),(24,'Triglycerides','mg/dL'),(32,'HDL cholesterol','mg/dL')]:
 for j,cohort,denom in [(1,'Hypertension','30intervention/60control'),(4,'Diabetes','26intervention/52control'),(7,'Obesity','44intervention/88control')]:
  interaction=table(rid,tid)[first+1][j+2]
  for line,year in [(first,'2019'),(first+1,'2023')]:
   c=table(rid,tid)[line-1]
   add(rid,tid,line,outcome=outcome,exposure='Voluntary12-week mobile chronic-disease programme implemented2021',contrast='Programme participants versus propensity-matched controls',stratum=cohort,timepoint=year,effect_measure='Estimated marginal means (SE),not SD; separate group and interaction p',p_between_groups=c[j+2],p_group_time=interaction,group1_summary=c[j],group2_summary=c[j+1],unit=unit,denominator_context=denom+' in this matched cohort; cohorts may overlap,do not sum Ns',model='Linear mixed-effects models adjusted for covariates with residualASD>=0.1 after matching; repeated interaction p same test on both rows',caution='Nonrandom voluntary programme;2019baseline precedes2021programme;2023follow-up not four continuous years of treatment. Selective survivor/checkup inclusion; residual confounding. Follow-up group p alone is not group*time effect. No paired uncertainty calculated from marginal SEs.')
# Spanish diet programme: no concurrent control; sex groups share time points.
rid='FC143-00167';tid='nutrients-16-01082-t002'
for line,outcome,unit in [(5,'Waist circumference','cm'),(7,'Systolic blood pressure','mmHg'),(8,'Diastolic blood pressure','mmHg'),(10,'HDL cholesterol','Source concentration scale; verify unit before pooling'),(12,'Triglycerides','Source concentration scale; verify unit before pooling'),(13,'Glycaemia','Source concentration scale; fasting definition to verify')]:
 c=table(rid,tid)[line-1]
 for j,sex,n in [(1,'Men',4038),(4,'Women',2996)]:
  add(rid,tid,line,outcome=outcome,exposure='Mediterranean-diet adherence programme',contrast='Same participants pre/post; no control',stratum=sex,effect_measure='Reported pre/post means(SD)',group1_summary=c[j],group2_summary=c[j+1],p_within_group=c[j+2],unit=unit,denominator_context=f'{n}reported in this sex group;7034workers total; paired endpoint missingness to verify',model='Uncontrolled pre/post participant analysis; January–June2022',caution='Selected low-adherence volunteers; no concurrent control,regression to mean andconfounding. Marginal pre/post SDs do not provide paired-change SE. Potential Spanish-worker companion overlap remains.')
for tid,lines in [('nutrients-16-01082-t003',[18]),('nutrients-16-01082-t004',[23,24])]:
 for line in lines:
  c=table(rid,tid)[line-1]
  for j,sex,n in [(1,'Men',4038),(5,'Women',2996)]:
   add(rid,tid,line,outcome=c[0],exposure='Mediterranean-diet adherence programme',contrast='Uncontrolled pre/post',stratum=sex,effect_measure='Reported mean(SD) component count' if line==18 else 'Reported pre/post syndrome prevalence',group1_summary=c[j],group2_summary=c[j+1],p_within_group=c[j+3],unit='Component count' if line==18 else 'Percent prevalence',denominator_context=f'{n} in this sex group;same workers underbothNCEP/IDF criteria',model='Paired before/after as reported; source Difference column not interpreted as percentage-point change',caution='No randomized orconcurrent control; different syndrome definitions notindependent populations. No fabricated numerator from rounded prevalence; no pairedriskratio orcausal effect inferred.')
# Retain adjusted activity,diet andstress estimates under explicit whole-source hold.
rid='FC143-00186';tid='table4-22799036251388562'
choices=[(21,'Physical exercise','No versusYes'),(29,'Eating frequency','Three versusTwo times'),(30,'Eating frequency','Four ormore versusTwo times'),(33,'Soda frequency','Rarely versusNever'),(34,'Soda frequency','Sometimes versusNever'),(35,'Soda frequency','Always versusNever'),(38,'Red-meat frequency','1–2/week versusNever'),(41,'Fasting frequency','Once/week versusNone'),(42,'Fasting frequency','Twice/week versusNone'),(43,'Fasting frequency','Four/week versusNone'),(49,'Work stress','No versusYes asreported')]
for line,exposure,contrast in choices:
 c=table(rid,tid)[line-1];m=re.fullmatch(r'([0-9.]+) \(([0-9.]+), ([0-9.]+)\)',c[4]);assert m
 add(rid,tid,line,outcome='Central obesity',exposure=exposure,contrast=contrast,effect_measure='Reported adjusted logistic OR',estimate=m[1],ci_lower=m[2],ci_upper=m[3],p_value=c[5],group1_summary=c[1]+' withcentralobesity; '+c[2]+' without',unit='Odds ratio',denominator_context='Table4 claims623participants;exercise cells69Yes+614No=683,conflicts withsample623',model='Multivariable Table4; exact complete-case N andcovariates requireconfirmation',caution='Source count/percentage inconsistencies; exerciseNo244+370=614,Yes22+47=69; no silentcorrection tocounts orOR. StressNo isreferencecontrastwithYes; do notinvert orlabel asoccupationalstress increasingrisk fromthisrow alone.',quantitative_hold='Denominator/cell inconsistency in original; source-specific model/result verification required before quantitative use')
# Iranian records: keep 2022 and10-Years headers asprinted,not baseline/follow-up.
rid='FC143-00207';tid='Tab4'
for line,outcome in [(9,'Fasting glucose'),(12,'Triglycerides'),(15,'Systolic blood pressure'),(16,'Diastolic blood pressure')]:
 c=table(rid,tid)[line-1]
 for j,time,pcol in [(2,'2022 aslabelled',6),(3,'10-Years aslabelled (aggregation requiresconfirmation)',7)]:
  add(rid,tid,line,outcome=outcome,exposure='Shift work',contrast='Shift versusdaywork',timepoint=time,effect_measure='Reported group means(SD); no derived longitudinal effect',p_between_groups=c[pcol],group1_summary=c[j],group2_summary=c[j+2],unit=c[1],denominator_context='204shift/204dayworkers; repeatedtenyearrecords notindependent participants',model='Reported Table4 comparison; exact interpretation of10-Years summary notcertified',caution='Healthy-worker survivor selection,baselineBMI matching andcoexposures. 10-Years values are not labelled anend-of-follow-up measurement; do not reconstruct achange score. LogisticTable6outcome direction remainsuncertain,notusedhere. Table1SBP/DBPreference labels areinconsistent.')
for line,outcome in [(8,'Fasting glucose'),(11,'Triglycerides'),(14,'Systolic blood pressure'),(15,'Diastolic blood pressure')]:
 for j,group in [(1,'Shiftworkers'),(4,'Dayworkers')]:
  c=table(rid,'Tab5')[line-1]
  add(rid,'Tab5',line,outcome=outcome,exposure='Shift work',contrast=group+' within-group time trend; notbetween-group interaction',effect_measure='Reported repeated-measures trend p; no effect estimate',p_within_group=c[j+2],group1_summary='df='+c[j]+', statisticlabelledt='+c[j+1],denominator_context='204pergroup;same workers asTable4',model='Repeated-measures ANOVA as source; Table5statistic labelledt despite fractionaldf; statistical quantity notcorrected',caution='Significant within-group trend inonegroup andnotother doesnot establish groupsdiffer. No group*timecoefficient orinteractionp inferred; noindependentstudy count.')
# Chemical plant: direct unadjusted components,not TyG adjusted OR.
rid='FC143-00208';tid='T2'
for line,outcome in [(2,'Systolic blood pressure'),(3,'Diastolic blood pressure'),(4,'Fasting glucose'),(7,'Triglycerides'),(8,'HDL cholesterol')]:
 c=table(rid,tid)[line-1]
 add(rid,tid,line,outcome=outcome,exposure='Shift work',contrast='1932shiftworkers versus1094dayworkers',effect_measure='Reported means(SD),unadjusted t-test',p_between_groups=c[4],group1_summary=c[3],group2_summary=c[2],unit='mmHg' if line in [2,3] else 'mg/dL',denominator_context='3026male chemical-plant workers; disease/medication/acetonitrile exclusions',model='Unadjusted Student t-test pertablefootnote',caution='Cross-sectional confounding andchemical coexposures. Adjusted TyG OR1.220 isnot anadjustedcomponent effect orMetSdiagnosis. Glucose andHDL nullcomparisons retained; no causalclaim.')
# Salt-education clinical completers: marginal medians/IQR,notmedian change.
rid='FC143-00217';tid='ijerph-20-05478-t005'
for line,outcome,unit in [(4,'Systolic blood pressure','mmHg'),(5,'Diastolic blood pressure','mmHg'),(6,'Abdominal circumference','cm')]:
 c=table(rid,tid)[line-1]
 add(rid,tid,line,outcome=outcome,exposure='Dietary sodium reduction education',contrast='Paired uncontrolled baseline/follow-up',effect_measure='Reported marginal medians(IQR),notmedianchange',p_within_group=c[3],group1_summary=c[1],group2_summary=c[2],unit=unit,denominator_context='95clinicalphasecompleters selected afterscreening workforce4911; notrepresentative4911treatedsample',model='Wilcoxon signed-rank pairedtest',caution='Voluntary two-stage recruitment,no control,selection andregressiontomean;selfreported sodium. Difference of medians isnot medianpairedchange; no pairedCI orcausaleffect manufactured.')
assert len(out)==103 and len(roots)==8
for x in out:
 if x['ci_lower']:assert float(x['ci_lower'])<=float(x['estimate'])<=float(x['ci_upper']) and float(x['ci_lower'])>0
for base in [R/'data',O]:
 with (base/'source_read_clinical_results_193.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
(D/'original_table_packets.json').write_text(json.dumps(list(packets.values()),indent=2,ensure_ascii=False),encoding='utf-8')
prior=[]
for name in ['current_numeric_extraction_audit_188.csv','source_read_clinical_results_191.csv','source_read_clinical_results_192.csv']:prior+=read(R/'data'/name)
covered={x['record_id'] for x in prior+out};remaining=sorted(set(reg)-covered)
with (O/'remaining_numeric_coverage_193.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['record_id','title','status']);w.writeheader();w.writerows(dict(record_id=rid,title=reg[rid]['title'],status='No specified row in188/191/192/193ledgers; notproof ofno prior extractionelsewhere') for rid in remaining)
status=dict(new_specified_clinical_rows=len(out),new_reports_with_specified_rows=len(roots),new_rows_by_report=dict(collections.Counter(x['record_id'] for x in out)),reports_with_rows_across_audit188_191_192_193=len(covered),reports_without_rows_in_these_sources=len(remaining),original_source_hashes_verified=len(roots),explicit_quantitative_hold_rows=sum(bool(x['quantitative_hold']) for x in out),full_extraction_certified=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
