/**
 * Standard function of p5js
 */
function setup() {
  createCanvas(DIMENSIONS[0], DIMENSIONS[1]).parent("artwork-container");

  // Use the same seed for every time setup is called.
  // (These are generated and initialized by Ginpar)
  randomSeed(RANDOM_SEED);
  noiseSeed(NOISE_SEED);
}

/**
 * Standard function of p5js
 */
function draw() {
  // Set a background color
  background(225);
}
