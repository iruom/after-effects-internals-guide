(function () {
    var log = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CORE-001/mutate.txt");
    log.open("w");
    try {
        var c = null;
        for (var i=1; i<=app.project.numItems; ++i) {
            var it = app.project.item(i);
            if (it && it.name === "AEIG_CORE_COMP") { c = it; break; }
        }
        if (!c) throw new Error("temp comp not found");
        for (var n=0; n<3; ++n) {
            var fg = c.layer("AEIG_CORE_FG" + n);
            var fx = fg.property("ADBE Effect Parade").property(1);
            fx.property(1).setValueAtTime(2.5, 110);
        }
        log.writeln("ok=true"); log.writeln("blur_mid=110");
    } catch (e) { log.writeln("ok=false"); log.writeln("error=" + e.toString()); }
    log.close();
})();