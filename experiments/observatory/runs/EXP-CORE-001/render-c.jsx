(function () {
    var label = "C";
    var c = null;
    for (var i=1; i<=app.project.numItems; ++i) {
        var it = app.project.item(i);
        if (it && it.name === "AEIG_CORE_COMP") { c = it; break; }
    }
    var dir = new Folder("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CORE-001/png-" + label);
    if (!dir.exists) dir.create();
    var log = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CORE-001/pass-" + label + ".txt");
    log.open("w"); log.writeln("begin=" + (new Date()).getTime());
    try {
        if (!c) throw new Error("temp comp not found");
        for (var f=0; f<120; ++f) {
            var out = new File(dir.fsName + "/f" + ("000"+f).slice(-3) + ".png");
            c.saveFrameToPng(f/24.0, out);
        }
        log.writeln("ok=true");
    } catch (e) { log.writeln("ok=false"); log.writeln("error=" + e.toString()); }
    log.writeln("end=" + (new Date()).getTime()); log.close();
})();

