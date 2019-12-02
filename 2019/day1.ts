import fs from 'fs';

import chalk from 'chalk';

const lines = fs
  .readFileSync('input/day1')
  .toString()
  .trim()
  .split('\n');

// Calculate the gas cost for a single item
const calculate = (x: number) => Math.max(0, Math.floor(x / 3) - 2);

// Given an initial gas cost, calculate the cost of the gas for this gas. Note
// that this assumes the gas will be passed in and not the module weight.
const recursiveCalculate = (x: number) => {
  let ret = x;
  let tmp = calculate(x);

  while (tmp > 0) {
    ret += tmp;
    tmp = calculate(tmp);
  }

  return ret;
}

const moduleCosts = lines.map((line) => calculate(parseInt(line)));
const modulesTotal = moduleCosts.reduce((total, current) => total + current, 0);

const recursiveCosts = moduleCosts.map(recursiveCalculate);
const recursiveTotal = recursiveCosts.reduce((total, current) => total + current, 0)

console.log(chalk.green('Total: ') + '%d', modulesTotal);
console.log(chalk.green('Recursive Total: ') + '%d', recursiveTotal);
