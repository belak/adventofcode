import { processProgram } from './lib/intcode';
import { readBigIntList } from './lib/utils';

const items: bigint[] = readBigIntList('input/day9');

console.log('Part 1:');
processProgram(items, [1n]);

console.log('Part 2:');
processProgram(items, [2n]);
