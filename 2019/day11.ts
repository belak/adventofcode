import { newState, processState } from './lib/intcode';
import { bigIntRange as range, readBigIntList } from './lib/utils';

const items: bigint[] = readBigIntList('input/day11');

type Color = 'white' | 'black';

const change = [
  { x: 0, y: -1 },
  { x: 1, y: 0 },
  { x: 0, y: 1 },
  { x: -1, y: 0 },
];

const nextDir = (cur: number, dir: number): number => {
  const dirChange = dir === 1 ? 1 : -1;

  // Special case wrapping
  if (cur === 0 && dirChange === -1) return 3;
  if (cur === 3 && dirChange === 1) return 0;

  return cur + dirChange;
};

const processProgram = (data: bigint[], panels: Map<string, Color>) => {
  let outState: 'color' | 'dir' = 'color';
  let dir: number = 0;
  let pos: { x: number; y: number } = { x: 0, y: 0 };

  let state = newState(data);

  state.inputCallback = (state) => {
    const curColor = panels.get(`${pos.x},${pos.y}`) || 'black';
    return curColor === 'black' ? 0n : 1n;
  };

  state.outputCallback = (state, out) => {
    switch (outState) {
      case 'color':
        const color = out === 0n ? 'black' : 'white';
        panels.set(`${pos.x},${pos.y}`, color);
        outState = 'dir';
        break;
      case 'dir':
        dir = nextDir(dir, Number(out));

        pos.x += change[dir].x;
        pos.y += change[dir].y;

        outState = 'color';
        break;
      default:
        throw new Error('unknown outState');
    }
  };

  processState(state);

  return panels;
};

console.log('Part 1:');
console.log(processProgram(items, new Map<string, Color>()).size);

console.log('Part 2:');
const part2Panels = processProgram(
  items,
  new Map<string, Color>().set('0,0', 'white')
);

const part2Keys = [...part2Panels.keys()].map((x) =>
  x.split(',').map((y) => +y)
);

const maxX = Math.max(...part2Keys.map((x) => x[0]));
const maxY = Math.max(...part2Keys.map((x) => x[1]));
const minX = Math.min(...part2Keys.map((x) => x[0]));
const minY = Math.min(...part2Keys.map((x) => x[1]));

console.log(maxX, maxY, minX, minY);

range(BigInt(minY), BigInt(maxY + 1)).forEach((y) => {
  range(BigInt(minX), BigInt(maxX + 1)).forEach((x) => {
    const char = part2Panels.get(`${x},${y}`) === 'white' ? '#' : ' ';
    process.stdout.write(char);
  });
  process.stdout.write('\n');
});
