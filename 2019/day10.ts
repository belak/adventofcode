import fs from 'fs';

const lines: string[] = fs
  .readFileSync('input/day10')
  .toString()
  .trim()
  .split('\n');

const width = lines[0].length;
const height = lines.length;

type Slope = number;
type Point = { x: number; y: number; dist: number };

const range = (n: number): number[] => [...Array(n).keys()];

const calc = (
  rawMap: string[],
  targetX: number,
  targetY: number
): Map<Slope, Point[]> => {
  const out = new Map<Slope, Point[]>();

  if (rawMap[targetY][targetX] !== '#') return out;

  range(width).forEach((x) => {
    range(height).forEach((y) => {
      // If there's no asteroid here, skip it
      if (rawMap[y][x] !== '#') {
        return;
      }

      // If we're at the target, don't count that either
      if (x === targetX && y === targetY) {
        return;
      }

      const dx = x - targetX;
      const dy = y - targetY;
      const dist = Math.sqrt(dx * dx + dy * dy);

      // Much easier to reason about in degrees
      const angle = (Math.atan2(dy, dx) * 180.0) / Math.PI;
      //console.log(angle);

      const prev = out.get(angle) || [];

      // Add the point and ensure they're sorted by distance
      const points = [{ x, y, dist }, ...prev];
      points.sort((a, b) => a.dist - b.dist);

      out.set(angle, points);
    });
  });

  /*
  console.log('x:', targetX);
  console.log('y:', targetY);
  console.log(out);
  console.log(out.size);
  */

  return out;
};

let part1Point: Point = { x: -1, y: -1, dist: -1 };
let part1Count = -1;
let finalMap = new Map<Slope, Point[]>();

range(height).forEach((y) => {
  return range(height).forEach((x) => {
    const map = calc(lines, x, y);
    if (map.size > part1Count) {
      part1Point = { x, y, dist: 0 };
      part1Count = map.size;
      finalMap = map;
    }
  });
});

console.log('Part 1: %d (%d, %d)', part1Count, part1Point.x, part1Point.y);

// Grab the keys, sort them, and re-order the array starting at the top point.
let keys = [...finalMap.keys()];
keys.sort((a, b) => a - b);

const topIdx = keys.findIndex((val) => val >= -90);
keys = [...keys.slice(topIdx), ...keys.slice(0, topIdx)];

const destroyedPoints: Point[] = [];

while (finalMap.size > 0) {
  keys.forEach((key) => {
    const data = finalMap.get(key);
    if (data === undefined) {
      return;
    }

    destroyedPoints.push(data.shift());
    if (data.length === 0) {
      finalMap.delete(key);
    } else {
      finalMap.set(key, data);
    }
  });
}

const part2 = destroyedPoints[199];
console.log('Part2:', part2);
