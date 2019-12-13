import { newState, processState } from './lib/intcode';
import { bigIntRange as range, readBigIntList } from './lib/utils';

const items: bigint[] = readBigIntList('input/day13');

type Tile = 'wall' | 'block' | 'hpaddle' | 'ball';

const tileType = (val: number): Tile | null => {
  switch (val) {
    case 0:
      return null;
    case 1:
      return 'wall';
    case 2:
      return 'block';
    case 3:
      return 'hpaddle';
    case 4:
      return 'ball';
  }

  throw new Error('unknown tyle type');
};

type Point = { x: number; y: number };

const processProgram = (data: bigint[]) => {
  const tiles = new Map<string, Tile>();
  let outState: 'x' | 'y' | 'tile' = 'x';
  let pos: Point = { x: 0, y: 0 };
  let ballCoords: Point = { ...pos };
  let paddleCoords: Point = { ...pos };
  let score = 0;

  let state = newState(data);

  state.inputCallback = (state) => {
    if (ballCoords.x < paddleCoords.x) {
      return -1n;
    } else if (ballCoords.x > paddleCoords.x) {
      return 1n;
    } else {
      return 0n;
    }
  };

  state.outputCallback = (state, out) => {
    switch (outState) {
      case 'x':
        pos.x = Number(out);
        outState = 'y';
        break;
      case 'y':
        pos.y = Number(out);
        outState = 'tile';
        break;
      case 'tile':
        outState = 'x';
        if (pos.x === -1 && pos.y === 0) {
          score = Number(out);
          return;
        }
        const key = `${pos.x},${pos.y}`;
        const t = tileType(Number(out));
        if (t) {
          if (t === 'ball') {
            ballCoords = { ...pos };
          } else if (t === 'hpaddle') {
            paddleCoords = { ...pos };
          } else {
            tiles.set(key, t);
          }
        } else {
          tiles.delete(key);
        }
        break;
      default:
        throw new Error('unknown outState');
    }
  };

  processState(state);

  console.log('Score:', score);

  return tiles;
};

console.log('Part 1:');
console.log(
  [...processProgram(items).values()].filter((x) => x === 'block').length
);

const part2Data = items.slice().map((val, idx) => (idx === 0 ? 2n : val));
processProgram(part2Data);
