import { readItems } from './lib/utils';

const items: number[] = readItems('input/day16', '').map((x) => +x);

const expand = (base: number[], len: number) =>
  Array(len)
    .fill(base)
    .flat();

const modifiers = [0, 1, 0, -1];

const modifierIdx = (digitIdx: number, dataIdx: number): number => {
  return modifiers[
    Math.floor((dataIdx + 1) / (digitIdx + 1)) % modifiers.length
  ];
};

const part1 = (data: number[]): number => {
  for (let i = 0; i < 100; i++) {
    for (let j = 0; j < data.length; j++) {
      data[j] =
        Math.abs(
          data
            .map((x, dataIdx) => x * modifierIdx(j, dataIdx))
            .reduce((x, y) => x + y)
        ) % 10;
    }
  }

  return parseInt(data.slice(0, 8).join(''));
};

// This is very frustrating. Lots of dynamic programming problems it seems like
// you have to notice the "gotcha" or it will seem unsolvable.
//
// Almost every instance of a solution in the subreddit seems to involve someone
// saying "I noticed X" without a very clear explanation of how that lets them
// make the optimizations they did.
const part2 = (data: number[]): number => {
  const baseOffset = parseInt(data.slice(0, 7).join(''));

  // Create a new array that's been expanded 10000 times.
  const digits = expand(data, 10000);

  for (let i = 0; i < 100; i++) {
    // We loop through from the end to the start because the current value is
    // equal to the previous value for this column plus the current value for
    // the next column.
    //
    // Defined more simply:
    //
    // value(digit, phase) = value(digit + 1, phase) + value(digit, phase - 1)
    //
    // Please don't ask me why because I really don't know.

    for (let j = digits.length - 2; j >= 0; j--) {
      digits[j] = Math.abs(digits[j] + digits[j + 1]) % 10;
    }
  }

  return parseInt(digits.slice(baseOffset, baseOffset + 8).join(''));
};

console.time('Part 1');
let data = items.slice();
console.log('Part 1:', part1(data));
console.timeEnd('Part 1');

console.time('Part 2');
data = items.slice();
console.log('Part 2:', part2(data));
console.timeEnd('Part 2');
