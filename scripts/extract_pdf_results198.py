"""Visually checked specified clinical comparisons from three PDF originals.

Values transcribed after inspecting rendered pages. This is not independent
review or completed whole-report extraction. Source misprints remain holds.
"""
import csv,json,hashlib,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/extraction198';D.mkdir(exist_ok=True);O=R.parents[1]/'outputs'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src={x['record_id']:x for x in read(R/'data/active_original_extraction_194.csv')};out=[]
def add(rid,page,table,**kw):
 s=src[rid];assert sha(R/s['source_file'])==s['source_sha256']
 image=R/'data/extraction196/pdf_visual_checks'/(rid+'_p'+str(page)+('.png' if rid!='SR141-0214' else '_rotated.png'))
 assert image.exists()
 row=dict(record_id=rid,outcome='',exposure='',contrast='',timepoint='',model='',effect_measure='',estimate='',ci_lower='',ci_upper='',p_value='',p_group_time='',group1_baseline='',group1_followup='',unit='',denominator_context='',caution='',quantitative_hold='',original_file=s['source_file'],original_sha256=s['source_sha256'],source_locator=f'PDF page{page}; {table}',visual_check_image=str(image.relative_to(R)),visual_check_image_sha256=sha(image),source_check='Selected source table visually inspected; not independent verification',full_report_extraction_complete=False,independent_review='Outstanding',quantitative_synthesis_approved=False)
 row.update(kw)
 if row['ci_lower'] and not float(row['ci_lower'])<=float(row['estimate'])<=float(row['ci_upper']):row['quantitative_hold']='Printed CI malformed or point outside interval; retained without guessed repair'
 out.append(row)
# Viester: baseline-corrected modelI and additionally adjusted modelII.
values=[('Waist circumference','cm',6,1,-1.38,-2.58,-.18,'.024'),('Waist circumference','cm',6,2,-1.38,-2.63,-.12,'.032'),('Waist circumference','cm',12,1,-.95,-2.23,.32,'.142'),('Waist circumference','cm',12,2,-.91,-2.25,.44,'.187'),('Systolic blood pressure','mmHg',6,1,-.50,-3.90,2.90,'.770'),('Systolic blood pressure','mmHg',6,2,-1.12,-4.63,2.40,'.532'),('Systolic blood pressure','mmHg',12,1,.50,-3.07,4.07,'.783'),('Systolic blood pressure','mmHg',12,2,.16,-3.49,3.81,'.932'),('Diastolic blood pressure','mmHg',6,1,-.05,-2.34,2.24,'.967'),('Diastolic blood pressure','mmHg',6,2,.25,-2.10,2.61,'.832'),('Diastolic blood pressure','mmHg',12,1,2.02,-.41,4.45,'.102'),('Diastolic blood pressure','mmHg',12,2,2.22,-.28,4.71,'.081')]
for outcome,unit,time,model,point,lo,hi,p in values:
 add('SR141-0104',6,'Table2' if outcome=='Waist circumference' else 'Table3',outcome=outcome,unit=unit,timepoint=f'{time}months',exposure='Workplace diet/activity counselling',contrast='Intervention versus control',effect_measure='Between-group regression coefficient',estimate=str(point),ci_lower=str(lo),ci_upper=str(hi),p_value=p,model='ModelI baseline-outcome corrected' if model==1 else 'ModelII baseline-outcome,age,education,maritalstatus,smoking adjusted',denominator_context='314allocated162/152; tablewaistN119/114; BPN128/129; exacttime/model Ns needverification',caution='Authors stateITT but useavailable follow-up completecases; noallrandomizeddata imputed here. Two models/times shareparticipants; notindependent studies. Table2upperwaistCI-.12 retained,not narrative-rounded-.1. Full extraction andtrialfamilyverification outstanding.')
# Geaney: active-condition versus sharedcontrol,not within-arm changes.
values=[('Waist circumference','cm','Education',-1.2,1.8,.5,'.480'),('Waist circumference','cm','Environment',.5,-3.2,4.2,'.796'),('Waist circumference','cm','Combined',-1.,-4.3,2.2,'.530'),('Systolic blood pressure','mmHg','Education',-3.7,-7.8,.4,'.080'),('Systolic blood pressure','mmHg','Environment',1.3,-3.1,5.8,'.558'),('Systolic blood pressure','mmHg','Combined',-2.4,-6.7,1.4,'.218'),('Diastolic blood pressure','mmHg','Education',-1.3,-4.1,1.4,'.331'),('Diastolic blood pressure','mmHg','Environment',2.,-.9,5.,'.176'),('Diastolic blood pressure','mmHg','Combined',.6,-1.9,3.2,'.633')]
for outcome,unit,group,point,lo,hi,p in values:
 add('SR141-0198',25,'Table4',outcome=outcome,unit=unit,timepoint='7–9months',exposure='Workplace food education/environment modification',contrast=group+' versuscontrol',effect_measure='Reported adjusted between-condition mean difference',estimate=str(point),ci_lower=str(lo),ci_upper=str(hi),p_value=p,model='MANCOVA;Methods age,sex,education,workinghours andotherbaseline factors; exactendpointmodel mapping toverify',denominator_context='Workplace-level conditions;endpointfittedNs nottranscribed; sharedcontrolacrossconditions',caution='Nonrandom/siteconfounded comparison; noindependentcontrol foreachcontrast. Table4educationwaistCI printed(1.8,0.5),reversedandoutsidepoint; no fabricatednegative sign. Table3within-group p notused ascontrolled effect.')
# Rusali: marginal means/SD and genuine interactionp; no invented treatment CI.
values=[('Waist circumference','cm','0.000',[('Control',39,'96.4 (8.7)','97.4 (10.2)'),('Online',31,'100.7 (13.8)','96.3 (12.4)'),('Face-to-face',38,'98.4 (11.3)','90.5 (10.0)')]),('Triglycerides','mmol/L','0.000',[('Control',39,'1.2 (0.60)','1.2 (0.66)'),('Online',31,'1.4 (0.64)','1.3 (0.64)'),('Face-to-face',38,'1.7 (1.14)','1.1 (0.58)')]),('HDL cholesterol','mmol/L','0.002',[('Control',39,'1.4 (0.35)','1.3 (0.32)'),('Online',31,'1.34 (0.31)','1.33 (0.32)'),('Face-to-face',38,'1.3 (0.26)','1.4 (0.30)')]),('Fasting glucose','mmol/L','0.147',[('Control',39,'5.0 (0.58)','4.8 (0.42)'),('Online',31,'5.2 (0.54)','4.8 (0.53)'),('Face-to-face',38,'5.3 (0.90)','4.9 (0.62)')])]
for outcome,unit,p,groups in values:
 for group,n,pre,post in groups:
  add('SR141-0214',5,'Table2(publishedpage2441)',outcome=outcome,unit=unit,timepoint='4months',exposure='Online/face-to-face workplaceweight management',contrast=group+' within-arm marginal means; shared3arm interactiontest',effect_measure='Means(SD),not pairedchange orbetween-groupcoefficient',p_group_time=p,group1_baseline=pre,group1_followup=post,model='Two-way repeated-measures ANOVA;tablefootnote energy/protein,TG covariates;Methods saysenergy/fat/TG—covariate discrepancy retained',denominator_context=f'{n}completersinarm;108completersfrom180initialrecruits;abstract108randomizedwording conflictswithResultsflow',caution='40%dropout;completer selection; interventionandcontrolreceiveeducation. Printedp.000rounded,not exactzero. No effectCI/pairedSE manufactured. Primarysource DOI10.17576/jsm-2018-4710-20,firstauthorRusali; currentregisteridentifierfields incomplete. Waistthresholdsexlabels inMethods appearreversed; no silentcorrection.')
assert len(out)==33 and len({x['record_id'] for x in out})==3
for base in [R/'data',O]:
 with (base/'source_read_pdf_results_198.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
prior=[]
for name in ['current_numeric_extraction_audit_188.csv','source_read_clinical_results_191.csv','source_read_clinical_results_192.csv','source_read_clinical_results_193.csv','source_read_clinical_results_195.csv','recovered_existing_results_194.csv']:prior+=read(R/'data'/name)
covered={x['record_id'] for x in prior+out};assert len(covered)==162
status=dict(new_specified_rows=33,reports=3,visually_inspected_pdf_pages=3,new_rows_by_report=dict(collections.Counter(x['record_id'] for x in out)),reports_with_specified_rows_in_expanded_ledgers=len(covered),available_originals_without_specified_rows=343-len(covered),original_source_gaps_deferred=45,full_extraction_complete=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
