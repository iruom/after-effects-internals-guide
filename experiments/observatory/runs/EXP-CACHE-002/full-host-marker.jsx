var out = new File("D:/Developer/After Effects Internals Guide/experiments/observatory/runs/EXP-CACHE-002/full-host-script-ran.txt");
out.open("w");
out.writeln("version=" + app.version);
out.writeln("build=" + app.buildName);
out.writeln("pid_marker=full-host");
out.close();
app.exitAfterLaunchAndEval = true;
