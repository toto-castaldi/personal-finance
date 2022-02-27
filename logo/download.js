document.getElementById("download-to-svg").onclick = () => {
    var fileName = "logo.svg"
    var url = "data:image/svg+xml;utf8," + encodeURIComponent(paper.project.exportSVG({ asString: true }));
    var link = document.createElement("a");
    link.download = fileName;
    link.href = url;
    link.click();
}