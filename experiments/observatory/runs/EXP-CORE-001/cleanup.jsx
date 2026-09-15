(function () {
    var log = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CORE-001/cleanup.txt");
    log.open("w");
    var removed = 0;
    for (var i=app.project.numItems; i>=1; --i) {
        var it = app.project.item(i);
        if (it && it.name.indexOf("AEIG_CORE_") === 0) {
            try { it.remove(); removed++; } catch (_) {}
        }
    }
    log.writeln("removed=" + removed);
    log.writeln("remaining_items=" + app.project.numItems);
    log.close();
})();