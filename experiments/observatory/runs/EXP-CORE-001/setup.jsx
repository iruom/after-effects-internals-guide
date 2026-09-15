(function () {
    var PREFIX = "AEIG_CORE_";
    for (var i = app.project.numItems; i >= 1; --i) {
        var old = app.project.item(i);
        if (old && old.name.indexOf(PREFIX) === 0) { try { old.remove(); } catch (_) {} }
    }
    var c = app.project.items.addComp(PREFIX + "COMP", 512, 512, 1, 5, 24);
    c.layers.addSolid([0.04,0.04,0.04], PREFIX + "BG", 512, 512, 1, 5);
    var colors = [[0.9,0.2,0.1],[0.1,0.7,0.9],[0.7,0.2,0.9]];
    for (var n=0; n<3; ++n) {
        var fg = c.layers.addSolid(colors[n], PREFIX + "FG" + n, 180, 180, 1, 5);
        var p = fg.property("ADBE Transform Group").property("ADBE Position");
        p.setValueAtTime(0, [100 + n*40, 120 + n*90]);
        p.setValueAtTime(2.5, [410 - n*50, 390 - n*70]);
        p.setValueAtTime(5, [100 + n*40, 120 + n*90]);
        var r = fg.property("ADBE Transform Group").property("ADBE Rotate Z");
        r.setValueAtTime(0, n*15); r.setValueAtTime(5, 360 + n*15);
        var fx = fg.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
        fx.property(1).setValueAtTime(0, 5); fx.property(1).setValueAtTime(2.5, 60); fx.property(1).setValueAtTime(5, 5);
    }
    var log = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CORE-001/setup.txt");
    log.open("w"); log.writeln("ok=true"); log.writeln("frames=120"); log.writeln("layers=" + c.numLayers); log.close();
})();