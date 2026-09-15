app.beginSuppressDialogs();
var root = new Folder("D:/Developer/After Effects Internals Guide/experiments/persistence/fixtures");
if (!root.exists) root.create();

function newComp() {
    app.newProject();
    return app.project.items.addComp("AEIG_Fixture", 320, 240, 1.0, 1.0, 24.0);
}

function saveTo(name) {
    app.project.save(new File(root.fsName + "/" + name));
}

var comp = newComp();
var textLayer = comp.layers.addText("A");
textLayer.name = "Text";
saveTo("text_A.aep");
var td = textLayer.property("ADBE Text Properties").property("ADBE Text Document").value;
td.text = "B";
textLayer.property("ADBE Text Properties").property("ADBE Text Document").setValue(td);
saveTo("text_B.aep");
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
comp = newComp();
var shapeLayer = comp.layers.addShape();
shapeLayer.name = "Shape";
var rootVectors = shapeLayer.property("ADBE Root Vectors Group");
var group = rootVectors.addProperty("ADBE Vector Group");
group.name = "Rect Group";
var vectors = group.property("ADBE Vectors Group");
var rect = vectors.addProperty("ADBE Vector Shape - Rect");
rect.property("ADBE Vector Rect Size").setValue([100, 100]);
var fill = vectors.addProperty("ADBE Vector Graphic - Fill");
fill.property("ADBE Vector Fill Color").setValue([1, 0, 0, 1]);
saveTo("shape_rect_100.aep");
rect.property("ADBE Vector Rect Size").setValue([200, 100]);
saveTo("shape_rect_200.aep");
app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.endSuppressDialogs(false);
app.quit();
