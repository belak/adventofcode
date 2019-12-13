import { readItems, pairs, lcm, deepCopy } from './lib/utils';

const matcher = /^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$/;

type Point = {
  x: number;
  y: number;
  z: number;

  dx: number;
  dy: number;
  dz: number;
};

const items: Point[] = readItems('input/day12').map((x) => {
  const result = x.match(matcher);
  if (!result) {
    throw new Error('invalid input');
  }

  return {
    x: +result[1],
    y: +result[2],
    z: +result[3],

    dx: 0,
    dy: 0,
    dz: 0,
  };
});

const step = (points: Point[]) => {
  pairs(points.length).forEach(([aIdx, bIdx]) => {
    const a = points[aIdx];
    const b = points[bIdx];

    if (a.x > b.x) {
      a.dx--;
      b.dx++;
    } else if (a.x < b.x) {
      a.dx++;
      b.dx--;
    }

    if (a.y > b.y) {
      a.dy--;
      b.dy++;
    } else if (a.y < b.y) {
      a.dy++;
      b.dy--;
    }

    if (a.z > b.z) {
      a.dz--;
      b.dz++;
    } else if (a.z < b.z) {
      a.dz++;
      b.dz--;
    }
  });

  points.forEach((val) => {
    val.x += val.dx;
    val.y += val.dy;
    val.z += val.dz;
  });
};

let part1Items = deepCopy(items);
for (let i = 0; i < 1000; i++) {
  step(part1Items);
}

const part1 = part1Items
  .map((val) => {
    const pot = Math.abs(val.x) + Math.abs(val.y) + Math.abs(val.z);
    const kin = Math.abs(val.dx) + Math.abs(val.dy) + Math.abs(val.dz);
    return pot * kin;
  })
  .reduce((x, y) => x + y);

console.log('Part 1:', part1);

let xSolved = false;
let xCycles = 0;

let state = deepCopy(items);
while (!xSolved) {
  xCycles++;
  step(state);
  xSolved = state.every(
    (pt, idx) => pt.x === items[idx].x && pt.dx === items[idx].dx
  );
}

let ySolved = false;
let yCycles = 0;

state = deepCopy(items);
while (!ySolved) {
  yCycles++;
  step(state);
  ySolved = state.every(
    (pt, idx) => pt.y === items[idx].y && pt.dy === items[idx].dy
  );
}

let zSolved = false;
let zCycles = 0;

state = deepCopy(items);
while (!zSolved) {
  zCycles++;
  step(state);
  zSolved = state.every(
    (pt, idx) => pt.z === items[idx].z && pt.dz === items[idx].dz
  );
}

console.log('Part 2:', [xCycles, yCycles, zCycles].reduce(lcm));
