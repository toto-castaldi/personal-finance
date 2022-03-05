const width = 800;
const height = 800;
const color1 = '#307c1f';
const canvas = document.getElementById("canvas");

paper.setup(canvas);

const ball0 = new paper.Path.Circle(new paper.Point(40, 205), 35);
ball0.fillColor = color1;