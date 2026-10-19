"""Source-read comparisons for nine reports previously present only in notes.

Uses only the helper definitions preceding the extraction body of script193.
No historical extraction body is executed and no source values are repaired.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
shared=(R/'scripts/extract_source_results193.py').read_text(encoding='utf-8').split('# All are shift workers;',1)[0]
exec(compile(shared.replace("R/'data/extraction193'","R/'data/extraction195'"),'<193 XML helpers>','exec'))
def bounds(text):
 m=re.fullmatch(r'\(?\s*([0-9.]+)\s*[–;]\s*([0-9.]+)\s*\)?',text)
 assert m,text
 return m[1],m[2]
def ratio(rid,tid,line,point,ci,**kw):
 lo,hi=bounds(ci);hold=kw.pop('quantitative_hold','')
 if float(point)<=0 or float(lo)<=0 or not float(lo)<=float(point)<=float(hi):hold+=' Invalid/nonpositive/out-of-interval printed ratio; no repair.'
 return add(rid,tid,line,estimate=point,ci_lower=lo,ci_upper=hi,quantitative_hold=hold.strip(),**kw)
# Diet: distinguish central obesity adjustment from syndrome adjustment.
rid='PM00713';tid='t3'
for line,outcome in [(3,'Central obesity'),(5,'Hypertension'),(7,'MetS')]:
 c=table(rid,tid)[line-1]
 for j,sex,n in [(1,'All',23729),(2,'Women',7693),(3,'Men',16036)]:
  m=re.fullmatch(r'([0-9.]+) \(([0-9.]+); ([0-9.]+)\)(?: §)?',c[j]);assert m
  ratio(rid,tid,line,m[1],m[2]+';'+m[3],outcome=outcome,exposure='Acceptable Mediterranean-diet adherence MEDAS14>=9',contrast='Acceptable versus lower adherence as tabledescribes',stratum=sex,effect_measure='Reported adjusted OR',unit='Odds ratio',denominator_context=f'{n} sex-specific/overall sample; endpoint model completecases toverify',model='Age,gender,smoking,PA,alcohol; Tablefootnote adds BMIobesity/centralobesity forhypertension/MetS; sex-specific coding toverify',caution='Cross-sectional,forward-Wald selection; no causalinference. Sex strata overlap overall sample; notindependent cohorts. Diagnostic definitions andmodel direction/reference requirefinalverification.')
# Workstress and sleep: conditional model effects,not a demonstrated mediation.
rid='PM00760';tid='pone.0224259.t003'
for j,model in [(7,'Model3'),(10,'Model4'),(13,'Model5')]:
 c=table(rid,tid)[4]
 ratio(rid,tid,5,c[j],c[j+1],outcome='Incident MetS',exposure='Work stress',contrast='Source stress coding; unit requiresconfirmation',effect_measure='Conditional adjusted OR',p_value=c[j+2],unit='Odds ratio',denominator_context='234 incharacteristics vs242elsewhere;26incidentcases; exactriskset/modelN unresolved',model=model+' hierarchical model; originalheader/footnotes retained',caution='Models conditionsleepvariables; nottotalcausalstresseffect. Mediator timing spansoutcome interval; sparseevents,attrition andreference/unit requireverification. Source n.s. notinvented exactp.')
c=table(rid,tid)[6]
ratio(rid,tid,7,c[13],c[14],outcome='Incident MetS',exposure='Insomnia symptoms',contrast='Reported symptom coding inModel5',effect_measure='Adjusted OR',p_value=c[15],unit='Odds ratio',denominator_context='26events; sourcepopulation234/242discrepancy',model='Hierarchical Model5; averaged T1/T2sleepvariables; footnote lastmodels ambiguous',caution='WideCI,sparseevents; insomniaassociation not direct occupationalstress effect. Printed .000 isrounding,not exactzero.')
tid='pone.0224259.t004'
for line in range(3,9):
 c=table(rid,tid)[line-1]
 common=dict(outcome=c[0],exposure='Insomnia symptoms',contrast='Insomnia symptom status asreported',effect_measure='Reported Model2 adjusted OR',p_value=c[9],unit='Odds ratio',denominator_context='Outcome-labelled N inrow preserved; cannotassume exposed cases label iscasecount',model='Model2: demographics plusaveragehours,ESS,satisfaction,stress',caution='N.s./n.e. preserved; componentrisksets notsummed. RelatedMetSestimate roundsModel5result,same underlying comparison,notindependent evidence. Mediator timing/denominators outstanding.')
 if c[7]=='n.e.':add(rid,tid,line,**common,quantitative_hold='Source ratio not evaluable; no zero or missingCI imputed')
 else:ratio(rid,tid,line,c[7],c[8],**common)
# Burnout/behaviour paper: PR explicitly retained,not renamed OR.
rid='PM00774';tid='ijerph-16-02686-t003'
for line,exposure in [(2,'Physical activity (direction toverify)'),(3,'Alcohol consumption'),(5,'Burnout syndrome')]:
 c=table(rid,tid)[line-1]
 ratio(rid,tid,line,c[1],c[2],outcome='MetS',exposure=exposure,contrast='Exactcategory/reference requiresverification',effect_measure='Source-labelled adjusted prevalence ratio',unit='Prevalence ratio',denominator_context='1125recruited;MetSassessed1111;burnout1121;exactjointmodelN toverify',model='Table3jointmodel; footnote adjustedbysmoking; logistic/robustPoisson/conversiondescription requiresconfirmation',caution='Cross-sectional PHCnurses; sourcePRnot incidentrisk. SameBahia2018nursingpopulation asPM03940mayoverlap; noindependentsamplecount. Exposurecoding andmodeltype remainopen.',quantitative_hold='Exact reference coding andPR-estimation method requireconfirmation')
# Component-specific burnout/shift ORs including printed separation failure.
rid='PM00787';tid='ijerph-16-01993-t002'
for line,exposure,reference in [(5,'Emotional exhaustion T2','T1'),(6,'Emotional exhaustion T3','T1'),(9,'Depersonalization T2','T1'),(10,'Depersonalization T3','T1'),(12,'Personal accomplishment T1','T3 inbothMethodsandTable2'),(13,'Personal accomplishment T2','T3 inbothMethodsandTable2'),(17,'Midday shift','Day'),(18,'Night shift','Day')]:
 c=table(rid,tid)[line-1]
 for k,outcome in enumerate(['Central obesity','Low HDL','High triglycerides','High fasting glucose','High blood pressure']):
  j=1+3*k
  ratio(rid,tid,line,c[j],c[j+1],outcome=outcome,exposure=exposure,contrast='Versus '+reference,effect_measure='Adjusted OR',p_value=c[j+2],unit='Odds ratio',denominator_context='168femalenurses from509invited; endpointfittedN toverify',model='Adjusted age,servicearea,BMI;Table2',caution='Cross-sectional convenience sample; wideCIs andmultiplecomparisons. Component effects notfullMetS effect. OriginalMethodsandTable2bothusepersonalaccomplishmentT3reference; oldcontradictionnote withdrawn. No silentinversion.')
# All four models and all sedentary domains,not significance-selected rows.
rid='PM00936';tid='Tab2'
for base,exposure in [(5,'Total sedentary time >=1minbouts'),(10,'Non-prolonged sedentary time <30minbouts'),(15,'Prolonged sedentary time >=30minbouts')]:
 for line in range(base,base+3):
  c=table(rid,tid)[line-1]
  for model,j in [('Model1',3),('Model2',6),('Model3',9),('Model4',12)]:
   ratio(rid,tid,line,c[j],c[j+1],outcome='Incident MetS',exposure=exposure,contrast=c[0]+' versusQ1,sexspecificwear-adjustedquartiles',effect_measure='Adjusted hazard ratio',p_value=c[j+2],unit='Hazard ratio',denominator_context='430baselineMetS-freeworkers;83events; rowcases='+c[1]+', rate='+c[2]+'/1000personyears; samepeople acrossdomains/models',model=model+';1age/sex;2adds education,smoking,income;3addsMVPA;4addswaist',caution='Cohort observational; eventinterval,attrition,accelerometerwear andbaselinecomponents requireverification. Model4waist conditioning differs fromModel3. Allmodels/domains shareparticipants,not independent cohorts; CI copiedfromtable,not priornote. Tablefootnoteincludesincome inModel2butMethodsomitsit; retaincovariatereportingdiscrepancy.')
# Police PA units corrected inheader; comparisons byMetS,notplaque ORs.
rid='PM01003';tid='pone.0133750.t006'
for line in range(13,21):
 c=table(rid,tid)[line-1]
 add(rid,tid,line,outcome='MetS status',exposure=c[0]+' physicalactivity',contrast='MetS versusnonMetS participants',effect_measure='Reported PA mean(SD) by syndrome status',group1_summary=c[1],group2_summary=c[2],p_between_groups=c[3],unit='Corrected MET-minutes/week/kg bodyweight perheader',denominator_context='235police:109MetS/126nonMetS; sameparticipants acrossactivitydomains',model='Unadjusted activity comparison; MethodsMannWhitneytest',caution='Cross-sectional; PSSgeneralstressnotjob-specific. Otherregressiontables predictplaque,not theseMetS/PA effects. Unit unusual,retainasprinted; nochange ofSDtoSE orcausalinference.')
# Meal-frequency PR with genuine hierarchy,notincidentrisk.
rid='PM01018';tid='t2';c=table(rid,tid)[43]
for j,model,pval in [(4,'Crude','0.008'),(7,'Adjustedhierarchical','0.002')]:
 ratio(rid,tid,44,c[j],c[j+1],outcome='MetS',exposure='Numberofmeals/day',contrast='>3 versus<=3meals/day',effect_measure='Reported prevalence ratio',p_value=pval,unit='Prevalence ratio',denominator_context='902fixedshiftpoultryworkers:292>3meals/610<=3;cross-sectional',model=model+';demographic then socioeconomic/workshift thenbehavioural level,footnotesretained',caution='Frequency comparisonnot meal-interventionefficacy. Pvaluecomesfromreference row43describingcategorytest. Samecohort/crude-adjustednotindependentstudies.')
# VitaminD waist medians/IQRs,not confidence intervals.
rid='PM02717';tid='T3';c=table(rid,tid)[2]
for j,arm,n in [(1,'Placebo',63),(2,'14000IU/week',66),(3,'28000IU/week',69)]:
 add(rid,tid,3,outcome='Waistcircumferencechange',exposure='WeeklyvitaminDsupplementation',contrast=arm+' descriptivemedianchange',timepoint='4months',effect_measure='Reported medianchange(p25–p75),notCI',group1_summary=c[j],unit='cm',denominator_context=f'Perprotocolarmn{n};198completeanalyses after362initialrecruits,44preinterventionwithdrawals and120postrandomizationexclusions;not randomizedN198',model='KruskalWallis/Bonferroni;allwaistarmssharesuperscripta=no reportedsignificantdifference',caution='No pairwiseadjustedeffect/CI orpairedSEinselectedtable. PPanalysisselectsbaselinevitD<30ng/mLandcompleteoutcomes;120postrandomizationexclusions includevitDsufficiency/missingdata. CompleteanalysisNnotoriginalrandomizedN. WHtRinversescale andoutsideprintedIQRelsewhere notusedaswaisteffect.')
# Exercise trial includes nullcomponents; no manufactured treatment CI.
rid='PM04516';tid='ijerph-16-00483-t001'
for line,outcome,unit in [(6,'Waist circumference','cm'),(9,'Systolic blood pressure','mmHg'),(10,'Diastolic blood pressure','mmHg'),(11,'HDL cholesterol','mg/dL'),(12,'Triglycerides','mg/dL'),(13,'Blood glucose','mg/dL'),(14,'MetS z-score','Source zscore')]:
 c=table(rid,tid)[line-1]
 for j,arm,n in [(1,'MICT',15),(3,'REHIT',12)]:
  add(rid,tid,line,outcome=outcome,exposure='ReducedexertionHIIT versusmoderatecontinuoustraining',contrast=arm+' pre/postdescriptivemeans',timepoint='8weeks',effect_measure='Reported means(SD) withsource significance markers',group1_summary=c[j],group2_summary=c[j+1],unit=unit,denominator_context=f'{n}completersinarm;32randomized16perarm,27analyzed',model='Source*:withingroup p<.05;dagger:change differsfromMICT p<.05;exactp/CI notfabricated',caution='Small trial,attrition,allocation andendpointanalysisto verify. Notallcomponents showbetweenarmeffect. zscorepercentagechanges nearzero/negativebaselines misleading; no pairedvariancefrommarginalSD.')
assert len(out)==125 and len(roots)==9
for base in [R/'data',O]:
 with (base/'source_read_clinical_results_195.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
(D/'original_table_packets.json').write_text(json.dumps(list(packets.values()),indent=2,ensure_ascii=False),encoding='utf-8')
status=dict(new_specified_clinical_rows=len(out),new_reports_with_specified_rows=len(roots),original_source_hashes_verified=len(roots),new_rows_by_report=dict(collections.Counter(x['record_id'] for x in out)),explicit_quantitative_hold_rows=sum(bool(x['quantitative_hold']) for x in out),full_extraction_certified=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
