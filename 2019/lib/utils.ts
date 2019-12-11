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

export { readItems, readNumberList, readBigIntList, range, bigIntRange };
