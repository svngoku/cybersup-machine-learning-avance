"""Preserve native charts while making scatter rendering explicit across viewers.

LibreOffice connects marker-only series when they retain a visible line, and
assumes smoothing when c:smooth is absent. No data are changed here.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import sys
import xml.etree.ElementTree as ET

NS = {"c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

source, target = map(Path, sys.argv[1:3])
assert source.resolve() != target.resolve()
with ZipFile(source) as src, ZipFile(target, "w", ZIP_DEFLATED) as out:
    for info in src.infolist():
        data = src.read(info.filename)
        if info.filename.endswith(".xml") and ("/charts/" in info.filename or "/theme/" in info.filename):
            root = ET.fromstring(data)
            for scatter in root.findall(".//c:scatterChart", NS):
                only_markers = scatter.find("c:scatterStyle", NS).get("val") == "marker"
                for series in scatter.findall("c:ser", NS):
                    smooth = series.find("c:smooth", NS)
                    if smooth is None:
                        smooth = ET.SubElement(series, "{" + NS["c"] + "}smooth")
                    smooth.set("val", "0")
                    if only_markers:
                        line = series.find("c:spPr/a:ln", NS)
                        if line is not None:
                            for child in list(line):
                                line.remove(child)
                            ET.SubElement(line, "{" + NS["a"] + "}noFill")
            # The only hyperlinks in this deck sit on the orange template pages.
            for scheme in root.findall(".//a:clrScheme", NS):
                for kind in ("hlink", "folHlink"):
                    color = scheme.find("a:" + kind, NS)
                    if color is not None:
                        for child in list(color):
                            color.remove(child)
                        ET.SubElement(color, "{" + NS["a"] + "}srgbClr", val="FFFFFF")
            data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        out.writestr(info, data)
print("Native chart and hyperlink rendering normalized")
