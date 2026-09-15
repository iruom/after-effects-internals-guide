var out = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CACHE-002/full-host25-script-ran.txt");
out.open("w");
out.writeln("version=" + app.version);
out.writeln("build=" + app.buildName);
out.close();
app.exitAfterLaunchAndEval = true;
