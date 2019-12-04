import fs from 'fs';

import chalk from 'chalk';

const lines = fs
  .readFileSync('input/day4')
  .toString()
  .trim()
  .split('-');

const range = (n: number): number[] => [...Array(n).keys()];

const rangeLow = +lines[0];
const rangeHigh = +lines[1];

// "thanks i hate it - jsvana"

// Match ascending numbers
const rule1Matcher = /^0*1*2*3*4*5*6*7*8*9*$/;
const rule1 = rule1Matcher.test.bind(rule1Matcher);

// Match doubles
const rule2Matcher = /(\d)\1/;
const rule2 = rule2Matcher.test.bind(rule2Matcher);

// Split into groups of 1 or more matching numbers and ensure we have a group
// that's at exactly size 2.
const rule3 = (x: string) => x.split(/((\d)\2*)/g).some((y) => y.length == 2);

const data = range(rangeHigh - rangeLow + 1).map((x) => x + rangeLow).map((x) => x.toString());

const part1Data = data.filter(rule1).filter(rule2);
const part2Data = part1Data.filter(rule3);

console.log(`${chalk.green('Part 1:')} %d`, part1Data.length);
console.log(`${chalk.green('Part 2:')} %d`, part2Data.length);
