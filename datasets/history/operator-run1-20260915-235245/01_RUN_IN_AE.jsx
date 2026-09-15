var CACHE = "D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CACHE-002/";
var RG = "D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-RG-001/";
var SCRIPT = "D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-SCRIPT-001/";
var LOGPATH = CACHE + "fixture-script.log";
var RECEIPT = CACHE + "receipt-matrix.tsv";
var PASSFILE = RG + "current-pass.txt";
var REFLECT = SCRIPT + "runtime-reflection.tsv";
var ENV = CACHE + "environment.txt";
function log(s){ var f=new File(LOGPATH); f.open("a"); f.writeln((new Date()).getTime()+"\t"+s); f.close(); }
function writeText(path,s){ var f=new File(path); f.open("w"); f.write(s); f.close(); }
function clean(s){ return String(s).replace(/[\t\r\n]+/g," "); }
function emitReflect(label,kind,info){
  var f=new File(REFLECT); f.open("a");
  var name="", type="", data="", ro="";
  try{name=info.name;}catch(e){}
  try{type=info.type;}catch(e){}
  try{data=info.dataType;}catch(e){}
  try{ro=info.isReadOnly;}catch(e){}
  f.writeln([clean(label),clean(kind),clean(name),clean(type),clean(data),clean(ro)].join("\t")); f.close();
}
function dumpReflect(obj,label){
  try{
    var r=obj.reflect, i;
    for(i=0;i<r.properties.length;i++) emitReflect(label,"property",r.properties[i]);
    for(i=0;i<r.methods.length;i++) emitReflect(label,"method",r.methods[i]);
  }catch(e){ log("REFLECT_ERR="+label+" "+e); }
}
function renderPass(comp,label,path){
  writeText(PASSFILE,label);
  log("PASS_BEGIN="+label);
  var rq=app.project.renderQueue.items.add(comp);
  if(label=="A"){
    dumpReflect(app.project.renderQueue,"RenderQueue");
    dumpReflect(rq,"RenderQueueItem");
    try{dumpReflect(rq.outputModule(1),"OutputModule");}catch(e){}
  }
  rq.timeSpanStart=0; rq.timeSpanDuration=comp.frameDuration;
  var om=rq.outputModule(1); om.applyTemplate("Lossless"); om.file=new File(path);
  app.project.renderQueue.render();
  log("PASS_END="+label+" status="+rq.status);
  try{rq.remove();}catch(e){log("RQ_REMOVE_ERR="+e);}
}
var comp=null;
var env=[];
try{env.push("app.version="+app.version);}catch(e){}
try{env.push("app.buildNumber="+app.buildNumber);}catch(e){}
try{env.push("app.buildName="+app.buildName);}catch(e){}
try{env.push("os="+$.os);}catch(e){}
try{env.push("locale="+app.isoLanguage);}catch(e){}
try{env.push("gpuAccelType="+app.project.gpuAccelType);}catch(e){}
writeText(ENV,env.join("\n")+"\n");
writeText(REFLECT,"label\tkind\tname\ttype\tdataType\tisReadOnly\n");
log("SCRIPT_ENTER AE="+app.version+" items_before="+app.project.numItems);
dumpReflect(app,"Application");
dumpReflect(app.project,"Project");
try {
  comp=app.project.items.addComp("AEIG_L5_FIXTURE",64,64,1,1,24);
  dumpReflect(comp,"CompItem");
  log("renderers="+comp.renderers.join(" | "));
  comp.renderer="AEIG Receipt Probe"; log("renderer="+comp.renderer);
  var layer=comp.layers.addSolid([0.2,0.4,0.6],"AEIG_SOLID",64,64,1,1);
  dumpReflect(layer,"AVLayer");
  var fx=layer.property("ADBE Effect Parade"); dumpReflect(fx,"EffectParade");
  var e1=fx.addProperty("ADBE Gaussian Blur 2"); e1.property(1).setValue(10); dumpReflect(e1,"GaussianBlur"); log("fx1="+e1.matchName+" blur=10");
  var e2=fx.addProperty("ADBE Fill"); dumpReflect(e2,"Fill"); log("fx2="+e2.matchName);
  var e3=fx.addProperty("ADBE Tint"); dumpReflect(e3,"Tint"); log("fx3="+e3.matchName);
  log("numEffects="+fx.numProperties);
  renderPass(comp,"A",CACHE+"fixture-output-A.avi");
  e1.property(1).setValue(75);
  log("MUTATION blur=75");
  renderPass(comp,"B",CACHE+"fixture-output-B.avi");
} catch(e) {
  log("ERR="+e.toString()+" line="+e.line);
}
try { if(comp) comp.remove(); } catch(e2) { log("COMP_REMOVE_ERR="+e2); }
writeText(PASSFILE,"DONE");
log("receipt_exists="+(new File(RECEIPT)).exists);
log("reflection_exists="+(new File(REFLECT)).exists);
log("items_after="+app.project.numItems);
log("SCRIPT_EXIT");
