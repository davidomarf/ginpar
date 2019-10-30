/* You don't need to initialize your variables in here. However, if you decide
 * to do it, you **must** use `var` instead of `let` or `const`.
 */

var DIMENSIONS = [2048, 2048]

/**
 * Standard function of p5js
 */
function setup() {
  createCanvas(DIMENSIONS[0], DIMENSIONS[1]).parent("artwork-container");

  // Call draw() only once
  noLoop();
}

/**
 * Standard function of p5js
 */
function draw() {
  // Set a background color
  background(225);
}
