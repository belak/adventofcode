import { processProgram } from './lib/intcode';
import { readBigIntList } from './lib/utils';

const items: bigint[] = readBigIntList('input/day2');

const processNounVerb = (
  rawData: bigint[],
  noun: bigint,
  verb: bigint
): bigint => {
  const data = rawData.slice();
  data[1] = noun;
  data[2] = verb;

  const state = processProgram(data);
  return state.mem.get(0n) || -1n;
};

console.log('Calc: %s', processNounVerb(items, 12n, 2n));

for (let i = 0n; i <= 99n; i++) {
  for (let j = 0n; j <= 99n; j++) {
    if (processNounVerb(items, i, j) == 19690720n) {
      console.log('Answer: %s', 100n * i + j);
    }
  }
}
