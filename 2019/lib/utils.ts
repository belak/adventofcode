import * as fs from 'fs';

const readItems = (filename: string, split: string = '\n'): string[] =>
  fs
    .readFileSync(filename)
    .toString()
    .trim()
    .split(split);

const readNumberList = (filename: string, split: string = ','): number[] =>
  readItems(filename, split).map((x) => +x);

const readBigIntList = (filename: string, split: string = ','): bigint[] =>
  readItems(filename, split).map((x) => BigInt(x));

const range = (start: number, end: number = 0): number[] => {
  if (end == 0) {
    end = start;
    start = 0;
  }

  return [...Array(end - start).keys()].map((x) => x + start);
};

const bigIntRange = (start: bigint, end: bigint): bigint[] =>
  [...Array(Number(end - start)).keys()].map((x) => BigInt(x) + start);

const pairs = (max: number): Array<[number, number]> => {
  const ret: [number, number][] = [];

  for (var i = 0; i < max; i++) {
    for (var j = i + 1; j < max; j++) {
      ret.push([i, j]);
    }
  }

  return ret;
};

/* Found on: https://stackoverflow.com/questions/47047682/least-common-multiple-of-an-array-values-using-euclidean-algorithm */
const gcd = (a: number, b: number): number => (a ? gcd(b % a, a) : b);
const lcm = (a: number, b: number): number => (a * b) / gcd(a, b);

const deepCopy = <T>(val: T): T => JSON.parse(JSON.stringify(val));

const zip = <T, V>(one: T[], two: V[]): [T, V][] =>
  one.map((x, idx) => [x, two[idx]]);

export {
  readItems,
  readNumberList,
  readBigIntList,
  range,
  bigIntRange,
  pairs,
  gcd,
  lcm,
  zip,
  deepCopy,
};
