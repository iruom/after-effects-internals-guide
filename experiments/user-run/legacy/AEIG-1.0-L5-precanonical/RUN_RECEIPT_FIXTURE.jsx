var LOGPATH = "D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CACHE-002/fixture-script.log";
function log(s){ var f=new File(LOGPATH); f.open("a"); f.writeln(s); f.close(); }
var oldActive = app.project.activeItem;
var comp = null, rq = null;
log("SCRIPT_ENTER AE=" + app.version + " items_before=" + app.project.numItems);
try {
  comp = app.project.items.addComp("AEIG_RECEIPT_FIXTURE",64,64,1,1,24);
  log("comp_created");
  comp.renderer = "AEIG Receipt Probe";
  log("renderer=" + comp.renderer);
  var layer = comp.layers.addSolid([0.2,0.4,0.6],"AEIG_SOLID",64,64,1,1);
  var fx = layer.property("ADBE Effect Parade");
  var e1 = fx.addProperty("ADBE Gaussian Blur 2"); log("fx1=" + (e1 ? e1.matchName : "null"));
  var e2 = fx.addProperty("ADBE Fill"); log("fx2=" + (e2 ? e2.matchName : "null"));
  var e3 = fx.addProperty("ADBE Tint"); log("fx3=" + (e3 ? e3.matchName : "null"));
  log("numEffects=" + fx.numProperties);
  rq = app.project.renderQueue.items.add(comp);
  rq.timeSpanStart = 0; rq.timeSpanDuration = comp.frameDuration;
  var om = rq.outputModule(1); om.applyTemplate("Lossless");
  om.file = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CACHE-002/fixture-output.avi");
  log("render_start"); app.project.renderQueue.render(); log("render_done status=" + rq.status);
} catch(e) { log("ERR=" + e.toString() + " line=" + e.line); }
try { if (rq) rq.remove(); } catch(e2) { log("RQ_REMOVE_ERR="+e2); }
try { if (comp) comp.remove(); } catch(e3) { log("COMP_REMOVE_ERR="+e3); }
try { if (oldActive) oldActive.openInViewer(); } catch(e4) {}
log("items_after=" + app.project.numItems);
