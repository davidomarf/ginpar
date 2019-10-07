/* ##ginpar */
const paramsJSON = `[
  {
     "var":"WIDTH",
     "attrs":{
        "type":"number",
        "value":2048,
        "min":0,
        "max":4096
     }
  },
  {
     "var":"HEIGHT",
     "attrs":{
        "type":"number",
        "value":2560,
        "min":0,
        "max":5120
     }
  },
  {
     "var":"NUMBER_OF_COLUMNS",
     "attrs":{
        "type":"number",
        "value":30,
        "step":1
     }
  },
  {
     "var":"COLUMN_Y_SD",
     "name":"Columns offset sd",
     "attrs":{
        "type":"number",
        "value":300,
        "step":1
     }
  },
  {
     "var":"COLUMN_HF_MIN",
     "name":"Minimum column height factor",
     "attrs":{
        "type":"range",
        "value":0.1,
        "step":0.01,
        "min":0,
        "max":1
     }
  },
  {
     "var":"COLUMN_HF_MAX",
     "name":"Maximum column height factor",
     "attrs":{
        "type":"range",
        "value":0.6,
        "step":0.01,
        "min":0,
        "max":1
     }
  }
]`
/* ##ginpar */

function jsonToVars(json){
  return Object.assign(...json.map(e => {return {[e.var ]: e.attrs.value}}))
}

let {
  WIDTH, 
  HEIGHT,
  NUMBER_OF_COLUMNS,
  COLUMN_Y_SD,
  COLUMN_HF_MIN,
  COLUMN_HF_MAX} = jsonToVars(JSON.parse(paramsJSON))

/**
 * Standard function of p5js
 */
function setup() {
  createCanvas(WIDTH, HEIGHT).parent("artwork-container");
  background(225);

  // Call draw() only once
  noLoop();
}

/**
 * Standard function of p5js
 */
function draw() {
  // Don't draw the stroke of the shapes, and fill with gray
  noStroke();
  fill(30);

  let columns = generateColumns(NUMBER_OF_COLUMNS);

  // The index starts at 2 and ends at (30 - 2) to avoid drawing
  // the two leftmost and rightmost columns in the canvas.
  for (let i = 2; i < NUMBER_OF_COLUMNS-2; i++) {
    drawColumn(columns[i]);
    let squares = generateSquaresForColumn(columns[i]);
    drawSquares(squares, columns[i]);
  }
}

/**
 * Generates a custom number of columns across the width and height
 * of the canvas
 *
 * @param {number} n  Indicates the number of columns to generate
 */
function generateColumns(n) {
  let columns = [];

  for (let i = 0; i < n; i++) {
    // Create a column. Here, x represents the top left corner,
    // and y the y coordinate of the middle point.
    let column = {
      x: i * (WIDTH / n),
      y: HEIGHT / 2 + randomGaussian(0, COLUMN_Y_SD),
        "name": "Column Y standard deviation",
      width: WIDTH / (n * 1.3),
      height: random(HEIGHT * COLUMN_HF_MIN, HEIGHT * COLUMN_HF_MAX)
    };

    // Change the x value to be the x coordinate of the middle point.
    column.x = column.x + column.width / 2;

    // Set the borders of the column
    column.borders = {
      top: column.y - column.height / 2,
      bottom: column.y + column.height / 2,
      left: column.x - column.width / 2,
      right: column.x + column.width / 2
    };

    columns.push(column);
  }

  return columns;
}

/**
 * Calls the function to draw a rectangle by calling it with attributes
 * of the column object
 * @param {Object} column   Contains the information to build a column
 *                          At least {x, y, width, height}
 */
function drawColumn(column) {
  handDrawRectangleMiddle(
    { x: column.x, y: column.y },
    column.width,
    column.height
  );
}

/**
 * Generate the individual little squares that are aligned with a single
 * column
 * @param {Object} column   Contains the information to build a column
 *                          At least {wi}
 */
function generateSquaresForColumn(column) {
  let squares = [];

  // Don't need to count. Will break when the middle of the squares lies
  // outside the canvas dimensions
  for (let j = 0; ; j++) {
    squares.push({
      middle: {
        x: column.x,
        y: (column.width * j + column.width * 0.5 * j) / 2
      },
      size: 1
    });

    // Square is outside the canvas dimensions
    if (squares[j].middle.y >= HEIGHT) break;
  }
  return squares;
}

/**
 * Draws all the squares in a vertical line associated with a single column
 *
 * @param {Object[]} squares  Contains all the squares from a single column
 * @param {Object} column     Contains the information to build a column
 */
function drawSquares(squares, column) {
  // Push new p5js style configuration values
  push();

  // This makes p5js rect() take the center coordinates as the first two
  // parameters, instead of the top left corner
  rectMode(CENTER);

  // Don't draw the stroke of the shapes
  noStroke();

  for (let j = 0; j < squares.length; j++) {
    // Set a base color of (almost-)white that will be used in the default case
    colorMode(RGB);
    fill(225);

    // If the square is outside the column, the color is a black one, with a
    // variable opacity that gets lower the further away from the center
    if (isSquareOutsideColumn(squares[j], column)) {
      // Create a custom RGBA color just to change the opacity
      fill(
        `rgba(30, 30, 30, ${1 -
          abs(HEIGHT / 2 - squares[j].middle.y) / (HEIGHT / 2)})`
      );

      // The squares outside the column are subject to a probability of not
      // being drawn. This probability increases the further away from the center.
      if (random() * 0.9 < abs(HEIGHT / 2 - squares[j].middle.y) / (HEIGHT / 2))
        continue;
    }

    // With a proability of .1, change the color to one of the three using the
    // hues 40, 350, and 220.
    // This overrules the color of the squares outside columns, including opacity.
    if (random() > 0.9) {
      colorMode(HSL);
      fill(random([40, 350, 220]), 60, 40);
    }

    // Draw a single square that deviates from its middle point, and with a
    // height that deviates from the standard (0.25 of the width of the column)
    handDrawRectangleMiddle(
      {
        x: randomGaussian(squares[j].middle.x, 2),
        y: randomGaussian(squares[j].middle.y, 2)
      },
      column.width * 0.4,
      randomGaussian(column.width * squares[j].size - column.width * 0.75, 6)
    );
  }

  // Return to the previous p5js specifications set outside this function
  pop();
}

/* ---------------------------- Helping Functions --------------------------- */

/**
 * Determines if a square is outside the column
 *
 * @param {Object} square   Contains the information to build a square
 *                          At least {middle.y}
 * @param {Object} column   Contains the information to build a column
 *                          At least {top, bottom}
 */
function isSquareOutsideColumn(square, column) {
  return (
    square.middle.y < column.borders.top ||
    square.middle.y > column.borders.bottom
  );
}

/**
 * Calculates the four {x, y} points that represent the corners of a
 * rectangle with specified middle, and height and width values.
 *
 * @param {Object} middle   Coordinates of the middle of the rectangle
 * @param {number} width    Width of the rectangle
 * @param {number} height   Height of the rectangle
 * @returns {Object}        Contains the corners in the order
 *                          1---2
 *                          |   |
 *                          4---3
 */
function getCornersFromMiddle(middle, width, height) {
  let halfW = width / 2;
  let halfH = height / 2;
  return [
    { x: middle.x - halfW, y: middle.y - halfH },
    { x: middle.x + halfW, y: middle.y - halfH },
    { x: middle.x + halfW, y: middle.y + halfH },
    { x: middle.x - halfW, y: middle.y + halfH }
  ];
}

/**
 * Angle of the line that joins two different points
 *
 * @param {Object} p1   {x, y} coordinates of the first point
 * @param {Object} p2   {x, y} coordinates of the second point
 * @returns {number}    Angle in radians
 */
function angleBetweenPoints(p1, p2) {
  return atan2(p2.y - p1.y, p2.x - p1.x);
}

/**
 * Produce the array of points that emulates a shaky-straight line
 * joining two points a, b.
 * @param {Object} a {x, y} coordinates of the first point
 * @param {Object} b {x, y} coordinates of the  second point
 */
function getHandDrawnLine(a, b) {
  // Generating a different seed for every line avoids getting
  // the same curve-pattern in different lines.
  noiseSeed(random(1000000));

  // The number of points is calculated in function to the distance
  // between the points.
  let distance = dist(a.x, a.y, b.x, b.y);
  let internalPoints = distance;
  let angle = angleBetweenPoints(a, b);

  let pointsInLine = [];

  // Create a line with every point perfectly aligned
  for (let i = 0; i < internalPoints; i++) {
    pointsInLine.push({
      x: a.x + i * ((distance * cos(angle)) / internalPoints),
      y: a.y + i * ((distance * sin(angle)) / internalPoints)
    });
  }

  // Modify each point by displacing it in a perpendicular direction
  // to the one of the line
  for (let i = 0; i < pointsInLine.length; i++) {
    let displacement = 3 * noise(i * 0.2) - 0.5;
    let perpendicular = angle + PI / 2;
    pointsInLine[i].x += displacement * cos(perpendicular);
    pointsInLine[i].y += displacement * sin(perpendicular);
  }

  return pointsInLine;
}

/**
 * Draw a rectangle in a hand drawn style specifiying the coordinates of
 * the midpoint and the width and height values.
 *
 * @param {Object} middle   {x, y} coordinates of the midpoint.
 * @param {number} width    Width of the rectangle
 * @param {number} height   Height of the rectangle
 */
function handDrawRectangleMiddle(middle, width, height) {
  beginShape();

  // Get the coordinates of every corner of the rectangle
  let corners = getCornersFromMiddle(middle, width, height);

  // Draw a line joining every contiguous corner
  for (let i = 0; i < 4; i++) {
    let handLine = getHandDrawnLine(
      corners[i],
      corners[(i + 1) % corners.length]
    );

    // For every point in the hand drawn line, create a vertex
    handLine.map(e => vertex(e.x, e.y));
  }

  endShape(CLOSE);
}
