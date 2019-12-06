import fs from 'fs';

const lines: string[][] = fs
  .readFileSync('input/day3')
  .toString()
  .trim()
  .split('\n')
  .map((x: string) => x.split(','));

type direction = 'L' | 'R' | 'U' | 'D';

const line1 = lines[0];
const line2 = lines[1];

const DX = { L: -1, R: 1, U: 0, D: 0 };
const DY = { L: 0, R: 0, U: 1, D: -1 };

const range = (n: number): number[] => [...Array(n).keys()];

const getPoints = (ops: string[]) => {
  const points = new Map<string, number>();

  let pos = {
    x: 0,
    y: 0,
  };

  let dist = 0;

  ops.forEach((op) => {
    const dir = op[0] as direction;
    const amount = parseInt(op.slice(1));
    for (let n in range(amount)) {
      dist += 1;
      pos.x += DX[dir];
      pos.y += DY[dir];

      const key = `${pos.x},${pos.y}`;

      // Handle crossing itself.
      if (!points.has(key)) {
        points.set(key, dist);
      }
    }
  });

  return points;
};

const points1 = getPoints(line1);
const points2 = getPoints(line2);

const intersectingKeys = [...points1.keys()].filter((val) => points2.has(val));
const part1 = Math.min(
  ...intersectingKeys.map((val) => {
    return val
      .split(',')
      .map((x) => Math.abs(+x))
      .reduce((x, y) => x + y);
  })
);

const intersectingVals = intersectingKeys.map(
  (key) => points1.get(key)! + points2.get(key)!
);
const part2 = Math.min(...intersectingVals);

console.log('Part 1: %d', part1);
console.log('Part 2: %d', part2);
