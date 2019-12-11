import { newState, processState } from './lib/intcode';
import { readBigIntList } from './lib/utils';

const items = readBigIntList('input/day5');

const process = (data: bigint[], input: bigint) => {
  const state = newState(data, [input]);
  processState(state);
};

console.log('Part 1:');
process(items, 1n);

console.log('Part 2:');
process(items, 5n);
