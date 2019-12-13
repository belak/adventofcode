import { readItems, pairs, lcm, deepCopy } from './lib/utils';

const matcher = /^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$/;

type Coord = {
  val: number;
  change: number;
};

type Point = {
  x: Coord;
  y: Coord;
  z: Coord;
};

const updateVelocity = (a: Coord, b: Coord) => {
  if (a.val > b.val) {
    a.change--;
    b.change++;
  } else if (a.val < b.val) {
    a.change++;
    b.change--;
  }
};

const items: Point[] = readItems('input/day12').map((x) => {
  const result = x.match(matcher);
  if (!result) {
    throw new Error('invalid input');
  }

  return {
    x: { val: +result[1], change: 0 },
    y: { val: +result[2], change: 0 },
    z: { val: +result[3], change: 0 },
  };
});

const step = (points: Point[]) => {
  pairs(points.length).forEach(([aIdx, bIdx]) => {
    const a = points[aIdx];
    const b = points[bIdx];

    updateVelocity(a.x, b.x);
    updateVelocity(a.y, b.y);
    updateVelocity(a.z, b.z);
  });

  points.forEach((val) => {
    val.x.val += val.x.change;
    val.y.val += val.y.change;
    val.z.val += val.z.change;
  });
};

let part1Items = deepCopy(items);
for (let i = 0; i < 1000; i++) {
  step(part1Items);
}

const part1 = part1Items
  .map((val) => {
    const pot = Math.abs(val.x.val) + Math.abs(val.y.val) + Math.abs(val.z.val);
    const kin =
      Math.abs(val.x.change) + Math.abs(val.y.change) + Math.abs(val.z.change);
    return pot * kin;
  })
  .reduce((x, y) => x + y);

console.log('Part 1:', part1);

let xSolved = false;
let xCycles = 0;
let ySolved = false;
let yCycles = 0;
let zSolved = false;
let zCycles = 0;

let state = deepCopy(items);
while (!(xSolved && ySolved && zSolved)) {
  if (!xSolved) xCycles++;
  if (!ySolved) yCycles++;
  if (!zSolved) zCycles++;

  step(state);

  const cmp = (a: Coord, b: Coord): boolean =>
    a.val === b.val && a.change === b.change;

  xSolved = xSolved || state.every((pt, idx) => cmp(pt.x, items[idx].x));
  ySolved = ySolved || state.every((pt, idx) => cmp(pt.y, items[idx].y));
  zSolved = zSolved || state.every((pt, idx) => cmp(pt.z, items[idx].z));
}

console.log('Part 2:', [xCycles, yCycles, zCycles].reduce(lcm));
