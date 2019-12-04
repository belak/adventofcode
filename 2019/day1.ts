import fs from 'fs';

const lines = fs
  .readFileSync('input/day1')
  .toString()
  .trim()
  .split('\n')
  .map((x) => +x);

// Calculate the gas cost for a single item
const calculate = (x: number) => Math.max(0, Math.floor(x / 3) - 2);

// Given an initial gas cost, calculate the cost of the gas for this gas. Note
// that this assumes the gas will be passed in and not the module weight.
const recursiveCalculate = (x: number) =>
  x === 0 ? x : x + recursiveCalculate(calculate(x));

const moduleCosts = lines.map(calculate);
const modulesTotal = moduleCosts.reduce((total, current) => total + current);

const recursiveCosts = moduleCosts.map(recursiveCalculate);
const recursiveTotal = recursiveCosts.reduce(
  (total, current) => total + current
);

console.log('Total: %d', modulesTotal);
console.log('Recursive Total: %d', recursiveTotal);
