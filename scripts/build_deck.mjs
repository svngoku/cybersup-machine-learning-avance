import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';

const root=path.resolve(process.env.COURSE_ROOT ?? '.');
const pkg=process.env.RUNTIME_NODE_MODULES ?? '/Users/svngoku/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {FileBlob,PresentationFile}=await import(pathToFileURL(path.join(pkg,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const skill=process.env.PRESENTATION_SKILL_DIR ?? '/Users/svngoku/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const template=process.env.COURSE_TEMPLATE ?? path.join(root,'CYBERSUP - TEMPLATE DATA_IA.pptx');
const source=await fs.readFile(template);
const p=await PresentationFile.importPptx(await FileBlob.load(template));
const templates=[...p.slides.items];
const sources=JSON.parse(await fs.readFile(path.join(root,'resources/sources.json'),'utf8'));
const charts=JSON.parse(await fs.readFile(path.join(root,'assets/chart-data.json'),'utf8'));
const tables=JSON.parse(await fs.readFile(path.join(root,'course/tables.json'),'utf8'));
const meta={name:'Chrys Fé-Marty NIONGOLO',repo:'https://github.com/svngoku/cybersup-machine-learning-avance',linkedin:'https://www.linkedin.com/in/chrys-f%C3%A9-marty-niongolo-410770153/'};
const C={ink:'#12194C',orange:'#FF7900',blue:'#303C8B',muted:'#555B70',white:'#FFFFFF'};
let all=[];
for(const filename of (await fs.readdir(path.join(root,'course'))).filter(n=>/^\d.*\.md$/.test(n)).sort()){
 const input=await fs.readFile(path.join(root,'course',filename),'utf8');
 for(const block of input.split(/^## /m).slice(1)){
  const lines=block.trim().split('\n'); const title=lines.shift().trim();
  const d={title,bullets:[],notes:'',refs:[],day:Number(filename[0]),kind:'content'};
  for(const line of lines){
   if(line.startsWith('- '))d.bullets.push(line.slice(2));
   else if(line.startsWith('> '))d.takeaway=(d.takeaway?d.takeaway+' ':'')+line.slice(2);
   else if(line.startsWith('Notes: '))d.notes+=line.slice(7)+'\n';
   else if(line.startsWith('Sources: '))d.refs=line.slice(9).split(',').map(x=>x.trim());
   else if(line.startsWith('Kind: '))d.kind=line.slice(6).trim();
   else if(line.startsWith('Chart: '))d.chart=line.slice(7).trim();
   else if(line.startsWith('Table: '))d.table=line.slice(7).trim();
   else if(line.startsWith('Equation: '))d.equation=line.slice(10).trim();
  }
  all.push(d);
 }
}
function textbox(slide,text,box,size=28,color=C.ink,font='DM Sans',bold=false){
 const s=slide.shapes.add({name:'course-'+text.slice(0,35),geometry:'textbox',position:box,fill:'none',line:{fill:'none',width:0}});
 s.text=text;s.text.style={typeface:font,fontSize:size,color,bold,autoFit:'none',wrap:'square',insets:{top:0,bottom:0,left:0,right:0},verticalAlignment:'top'};return s;
}
function edit(s,text,pos,size,font='DM Sans',color=C.white){
 s.text=text;if(pos)s.position=pos;
 s.text.style={typeface:font,fontSize:size,color,autoFit:'none',wrap:'square',insets:{top:0,bottom:0,left:0,right:0}};
}
function byText(slide,text){return slide.shapes.items.find(s=>String(s.text).includes(text));}
function brand(slide,d,i,dark=false){
 for(const s of slide.shapes.items){
  const text=String(s.text);
  if(text.includes('{{NOM_DU_COURS}}'))edit(s,'Machine Learning Avancé · M2 Data / IA',{...s.position,width:720},16,'DM Sans',dark?C.white:C.ink);
  else if(text.includes('{{AN1-AN2}}'))edit(s,'2026 / '+String(i+1).padStart(3,'0'),{left:1090,top:654,width:145,height:28},14,'Roboto Mono',dark?C.white:C.ink);
  else if(text.includes('{{NOM_DU_CHAPITRE}}'))edit(s,d.day?'JOUR '+d.day:'CYBERSUP',{left:995,top:48,width:220,height:24},14,'Roboto Mono',dark?C.white:C.ink);
 }
}
function dropBody(slide){
 for(const s of [...slide.shapes.items])if(s.position.top<620 && !(String(s.text).includes('SPE')||s.position.left<0))s.delete();
 for(const im of [...slide.images.items])if(im.frame.top<620)im.delete();
}
const tableOwners=[],chartOwners=[];
for(let i=0;i<all.length;i++){
 const d=all[i];let slide;
 if(d.kind==='cover'){
  slide=templates[0].duplicate();
  edit(byText(slide,'{{NOM_DU_COURS}}'),'MACHINE LEARNING\nAVANCÉ',{left:96,top:118,width:1090,height:220},78,'Archivo Black');
  edit(byText(slide,'{{SOUS-TITRE}}'),'21–25 SEPTEMBRE 2026\n35 heures · M2 Data / IA',{left:96,top:363,width:920,height:100},32);
  textbox(slide,meta.name,{left:96,top:497,width:910,height:45},27,C.white);
  byText(slide,'{{LOGO}}')?.delete();
  slide.images.add({blob:new Uint8Array(await fs.readFile(path.join(root,'assets/qr-repository.png'))),contentType:'image/png',position:{left:1106,top:499,width:106,height:106},alt:'QR vers le dépôt privé du cours'});
  edit(byText(slide,'SYLLABUS'),'RESSOURCES',null,11,'DM Sans',C.ink);
  edit(byText(slide,'SCAN ME'),'ACCÈS PRIVÉ',{left:1106,top:604,width:108,height:14},10,'DM Sans',C.ink);
  brand(slide,d,i,true);
 }else if(d.kind==='trainer'){
  slide=templates[1].duplicate();dropBody(slide);
  textbox(slide,'VOTRE FORMATEUR',{left:60,top:67,width:1100,height:55},36,C.white,'Archivo Black');
  textbox(slide,'Chrys\nFé-Marty\nNIONGOLO',{left:65,top:174,width:360,height:240},46,C.white,'Archivo Black');
  textbox(slide,'Machine Learning Avancé\nCybersup · Septembre 2026',{left:65,top:440,width:350,height:110},24,C.white);
  textbox(slide,'UNE SEMAINE POUR PRATIQUER',{left:465,top:174,width:710,height:65},28,C.white,'Archivo Black');
  textbox(slide,d.bullets.join('\n\n'),{left:465,top:262,width:690,height:265},26,C.white);
  const l=textbox(slide,'Profil LinkedIn de Chrys Fé-Marty NIONGOLO',{left:465,top:544,width:700,height:48},22,C.white);l.text.get(String(l.text)).link={uri:meta.linkedin,isExternal:true};l.text.get(String(l.text)).fill=C.white;
  brand(slide,d,i,true);
 }else if(d.kind==='agenda'){
  slide=templates[2].duplicate();
  const labels=['Évaluer et régulariser','Ensembles et optimisation','Déséquilibre et features','Clustering et anomalies','Interpréter et restituer'];
  const old=['LOGO ','UTILISATION INCORRECTE DU LOGO','TYPOGRAPHIE','COULEURS ','IDENTITE VISUELLE'];
  for(let j=0;j<5;j++)edit(byText(slide,old[j]),labels[j],{left:172,top:103+j*58,width:645,height:46},28,'DM Sans');
  edit(byText(slide,'Cette présentation'), 'Évaluer, optimiser et interpréter des modèles.\n\nCours, TP Python et projet en binôme.',{left:870,top:151,width:345,height:175},22,'DM Sans');
  edit(byText(slide,'5 jours de'),'35 h en présentiel',{left:915,top:329,width:285,height:30},20);
  edit(byText(slide,'5 Chapitres'),'5 journées',{left:915,top:386,width:285,height:30},20);
  for(const t of ['{{LOGO}}','SYLLABUS','SCAN ME'])byText(slide,t)?.delete();
  for(const s of [...slide.shapes.items])if(s.position.left>1080&&s.position.top>450&&s.position.top<620)s.delete();
  brand(slide,d,i,true);
 }else if(d.kind==='section'){
  slide=templates[4].duplicate();
  edit(byText(slide,'{{NOM_DU_CHAPITRE}}'),d.title,{left:275,top:232,width:905,height:172},54,'Archivo Black');
  edit(byText(slide,'01'),String(d.day).padStart(2,'0'),null,80,'Roboto Mono');
  textbox(slide,d.takeaway??'',{left:100,top:470,width:1080,height:70},28,C.white);
  brand(slide,d,i,true);
 }else if(d.kind==='closing'){
  slide=templates[16].duplicate();
  edit(byText(slide,'MERCI'),'À VOUS DE JOUER',{left:100,top:250,width:1110,height:125},72,'Archivo Black');
  textbox(slide,meta.name,{left:100,top:418,width:1080,height:54},30,C.white);
  const l=textbox(slide,'Ressources et notebooks sur GitHub',{left:100,top:490,width:1000,height:60},29,C.white);l.text.get(String(l.text)).link={uri:meta.repo,isExternal:true};l.text.get(String(l.text)).fill=C.white;
  brand(slide,d,i,true);
 }else{
  slide=templates[5].duplicate();brand(slide,d,i);
  if(d.kind==='summary')slide.background.fill='#F7EEE5';
  textbox(slide,d.title,{left:80,top:90,width:1110,height:95},36,C.ink,'Archivo Black');
  if(d.chart){
   const spec=charts[d.chart];if(!spec)throw Error('Unknown chart '+d.chart);
   const colors=[C.blue,C.orange,'#16A5AA','#9A3070','#8490A4'];
   const scatter=spec.type==='scatter';const chart=slide.charts.add(spec.type,{
    position:{left:76,top:195,width:745,height:370},categories:spec.categories,
    series:spec.series.map((s,j)=>({...s,fill:colors[j%colors.length],line:{fill:colors[j%colors.length],width:2.5},marker:{symbol:scatter?'circle':'none',size:d.chart==='kmeans'||d.chart==='dbscan'?4:3}})),
    hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:'DM Sans',fontSize:16}},
    xAxis:{...(['roc','pr','calibration'].includes(d.chart)?{min:0,max:1}:{}),title:spec.xlabel,textStyle:{typeface:'DM Sans',fontSize:15},majorGridlines:null},
    yAxis:{...(['roc','pr','calibration'].includes(d.chart)?{min:0,max:1}:{}),title:spec.ylabel,textStyle:{typeface:'DM Sans',fontSize:15},majorGridlines:{fill:'#E5E7EE',width:1}},
    chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',
    scatterOptions:{style:['kmeans','dbscan'].includes(d.chart)?'marker':'lineWithMarkers'},
    barOptions:{direction:'column',grouping:'clustered'},lineOptions:{smooth:false},
   });applyPresentationChartFont(chart,{fontFamily:'DM Sans'});chartOwners.push(i+1);
   textbox(slide,d.bullets.join('\n\n'),{left:855,top:210,width:348,height:345},25,C.ink);
   textbox(slide,spec.disclosure,{left:80,top:571,width:1115,height:41},15,C.muted);
  }else if(d.table){
   const values=tables[d.table];if(!values)throw Error('Unknown table '+d.table);
   const table=slide.tables.add({rows:values.length,columns:values[0].length,left:80,top:192,width:1120,height:320,values});
   for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
    const cell=table.getCell(r,c);cell.fill=r===0?C.blue:(r%2?'#F4F5F8':'#FFFFFF');
    cell.text.style={typeface:'DM Sans',fontSize:values.length>=7?20:(values[0].length>3?21:23),color:r===0?C.white:C.ink,bold:r===0,insets:{left:12,right:12,top:10,bottom:10}};
   }
   tableOwners.push(i+1);textbox(slide,d.takeaway??d.bullets.join(' '),{left:80,top:540,width:1110,height:60},25,C.ink);
  }else{
   const top=d.equation?274:208;const step=d.bullets.length>3?77:98;
   if(d.equation)textbox(slide,d.equation,{left:80,top:184,width:1110,height:73},32,C.blue,'DM Sans',true);
   d.bullets.forEach((line,j)=>textbox(slide,line,{left:86,top:top+j*step,width:1100,height:step-10},d.bullets.length>3?27:30,C.ink));
   if(d.takeaway)textbox(slide,d.takeaway,{left:80,top:548,width:1115,height:68},25,C.blue,'DM Sans',true);
  }
  const refText=d.refs.length?'Sources : '+d.refs.join(', ')+' · liens et détails dans les notes':'Exemple ou activité originale du cours';
  textbox(slide,refText,{left:80,top:620,width:1090,height:22},13,C.muted,'Roboto Mono');
 }
 slide.moveTo(p.slides.items.length-1);
 const bibliography=d.refs.map(id=>{if(!sources[id])throw Error('Unknown reference '+id);const r=sources[id];return `[${id}] ${r.title}. ${r.author}. ${r.date}. ${r.url} (consulté le 19 septembre 2026).`;}).join('\n');
 slide.speakerNotes.textFrame.setText(`${d.title}\n\n${d.notes}\n${d.takeaway??''}\n\n${d.chart?charts[d.chart].disclosure:''}\n\n${bibliography}\n\nFormateur : ${meta.name}`);
 if((i+1)%20===0)console.log('Slides préparées',i+1);
}
for(const s of templates)s.delete();
const build=path.join(root,'.build');await fs.mkdir(build,{recursive:true});await fs.mkdir(path.join(root,'output'),{recursive:true});
const rawCandidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(rawCandidate);
const candidate=path.join(build,'candidate-normalized.pptx');
execFileSync(process.env.RUNTIME_PYTHON??'/Users/svngoku/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',[path.join(root,'scripts/normalize_pptx.py'),rawCandidate,candidate],{stdio:'inherit'});
await fs.writeFile(path.join(build,'slide-manifest.json'),JSON.stringify(all,null,2));
const finalPath=path.join(root,'output',process.env.OUTPUT_NAME??'CYBERSUP-Machine-Learning-Avance-2026.pptx');
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,
 pythonExecutable:process.env.RUNTIME_PYTHON??'/Users/svngoku/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],
 explicitTotalSlideCount:all.length,requiredNativeTableOwnerSlides:tableOwners,requiredNativeChartOwnerSlides:chartOwners,
 materializeLiteralChartWorkbooks:true,verifyArtifactToolImport:true,
 fontPolicy:{basis:'reference',families:['Archivo Black','DM Sans','Roboto Mono'],referencePath:template,referenceSha256:createHash('sha256').update(source).digest('hex')},
 receiptPath:path.join(build,path.basename(finalPath,'.pptx')+'-validation.json')});
console.log(JSON.stringify({finalPath,slides:all.length,charts:chartOwners.length,tables:tableOwners.length}));
