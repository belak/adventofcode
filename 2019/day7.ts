import { newState, processState } from './lib/intcode';
import { readBigIntList } from './lib/utils';

const items = readBigIntList('input/day7');

const processPipeline = (data: bigint[], input: bigint[]): bigint => {
  let prev = 0n;

  input.forEach((x) => {
    let state = newState(data, [x, prev]);
    state.outputCallback = (state, out) => {
      prev = out;
    };
    processState(state);
  });

  return prev;
};

const processFeedback = (data: bigint[], input: bigint[]): bigint => {
  const states = input.map((x, idx) => newState(data, [x]));

  let prev = 0n;

  // Keep doing this as long as the last engine hasn't halted.
  while (!states[states.length - 1].halted) {
    states.forEach((state, idx) => {
      // Push the output of the previous to the input stack of the next program.
      state.input.push(prev);

      // Ensure the output updates the prev value
      state.outputCallback = (state, out) => {
        prev = out;
      };

      try {
        processState(state);
      } catch (e) {
        const err: Error = e;
        if (err.message !== 'no input') {
          throw err;
        }
      }
    });
  }

  return prev;
};

const permutations = <T>(inputArr: T[]) => {
  let result: T[][] = [];

  const permute = (arr: T[], m: T[] = []) => {
    if (arr.length === 0) {
      result.push(m);
    } else {
      for (let i = 0; i < arr.length; i++) {
        let curr = arr.slice();
        let next = curr.splice(i, 1);
        permute(curr.slice(), m.concat(next));
      }
    }
  };

  permute(inputArr);

  return result;
};

const part1Input = [0n, 1n, 2n, 3n, 4n];
const part1InputOptions = permutations(part1Input);

const part1 = Math.max(
  ...part1InputOptions
    .map((x) => processPipeline(items, x))
    .map((x) => Number(x))
);

console.log('Part 1:', part1);

const part2Input = [5n, 6n, 7n, 8n, 9n];
const part2InputOptions = permutations(part2Input);
const part2 = Math.max(
  ...part2InputOptions
    .map((x) => processFeedback(items, x))
    .map((x) => Number(x))
);
console.log('Part 2:', part2);
