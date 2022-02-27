const width = 800;
const height = 800;
const color1 = '#003365';
const canvas = document.getElementById("canvas");

paper.setup(canvas);

const ball = new paper.Path.Circle(new paper.Point(40, 205), 35);
ball.fillColor = color1;