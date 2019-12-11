import fs from 'fs';

// Originally based on day9

const items: bigint[] = fs
  .readFileSync('input/day11')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => BigInt(x));

type OpCallback = (state: State, params: bigint[]) => void;
type ParamMapper = (state: State, mode: string, v: bigint) => bigint;

type Color = 'white' | 'black';

type State = {
  // Program related
  mem: Map<bigint, bigint>;
  ptr: bigint;
  halted: boolean;
  out: bigint;
  relativeBase: bigint;

  // Paint related
  outState: 'color' | 'dir';
  dir: number;
  pos: { x: number; y: number };
  panels: Map<string, Color>;
};

const newState = (data: bigint[], panels: Map<string, Color>): State => ({
  ptr: BigInt(0),
  out: BigInt(-1),
  halted: false,
  mem: data.reduce(
    (mem, val, idx) => mem.set(BigInt(idx), val),
    new Map<bigint, bigint>()
  ),
  relativeBase: BigInt(0),

  outState: 'color',
  dir: 0,
  pos: { x: 0, y: 0 },
  panels,
});

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

const range = (start: bigint, end: bigint): bigint[] =>
  [...Array(Number(end - start)).keys()].map((x) => BigInt(x) + start);

const processAdd = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] + params[1]);
  state.ptr += BigInt(4);
};

const processMul = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] * params[1]);
  state.ptr += BigInt(4);
};

const processInp = (state: State, params: bigint[]) => {
  const curColor = state.panels.get(`${state.pos.x},${state.pos.y}`) || 'black';
  const input = curColor === 'black' ? BigInt(0) : BigInt(1);
  state.mem.set(params[0], input);
  state.ptr += BigInt(2);
};

const processOut = (state: State, params: bigint[]) => {
  switch (state.outState) {
    case 'color':
      const color = params[0] === BigInt(0) ? 'black' : 'white';
      state.panels.set(`${state.pos.x},${state.pos.y}`, color);
      state.outState = 'dir';
      break;
    case 'dir':
      state.dir = nextDir(state.dir, Number(params[0]));
      state.outState = 'color';
      state.pos = {
        x: state.pos.x + change[state.dir].x,
        y: state.pos.y + change[state.dir].y,
      };
      break;
  }

  state.out = params[0];
  state.ptr += BigInt(2);
};

const processJT = (state: State, params: bigint[]) => {
  state.ptr = params[0] !== BigInt(0) ? params[1] : state.ptr + BigInt(3);
};

const processJF = (state: State, params: bigint[]) => {
  state.ptr = params[0] === BigInt(0) ? params[1] : state.ptr + BigInt(3);
};

const processLT = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] < params[1] ? BigInt(1) : BigInt(0));
  state.ptr += BigInt(4);
};

const processEq = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] === params[1] ? BigInt(1) : BigInt(0));
  state.ptr += BigInt(4);
};

const processRel = (state: State, params: bigint[]) => {
  state.relativeBase += params[0];
  state.ptr += BigInt(2);
};

const processDone = (state: State, params: bigint[]) => {
  state.mem = new Map();
  state.ptr = BigInt(-1);
  state.halted = true;
};

function inputParamMapper(state: State, mode: string, v: bigint): bigint {
  switch (mode) {
    case '0':
      return state.mem.get(v) || BigInt(0);
    case '1':
      return v;
    case '2':
      return state.mem.get(state.relativeBase + v) || BigInt(0);
  }

  throw new Error(`Unknown input param mode: ${mode}`);
}

function targetParamMapper(state: State, mode: string, v: bigint): bigint {
  switch (mode) {
    case '0':
      return v;
    case '2':
      return state.relativeBase + v;
  }

  throw new Error(`Unknown target param mode: ${mode}`);
}

const paramMap: {
  [key: string]: [OpCallback, ParamMapper[]];
} = {
  '01': [processAdd, [inputParamMapper, inputParamMapper, targetParamMapper]],
  '02': [processMul, [inputParamMapper, inputParamMapper, targetParamMapper]],
  '03': [processInp, [targetParamMapper]],
  '04': [processOut, [inputParamMapper]],
  '05': [processJT, [inputParamMapper, inputParamMapper]],
  '06': [processJF, [inputParamMapper, inputParamMapper]],
  '07': [processLT, [inputParamMapper, inputParamMapper, targetParamMapper]],
  '08': [processEq, [inputParamMapper, inputParamMapper, targetParamMapper]],
  '09': [processRel, [inputParamMapper]],
  '99': [processDone, []],
};

const processSingleOpCode = (state: State) => {
  const rawOpCode = state.mem.get(state.ptr)!.toString();
  const rawParamModes = rawOpCode
    .slice(0, -2)
    .split('')
    .reverse()
    .join('');
  const opCode = rawOpCode.slice(-2).padStart(2, '0');

  const fun = paramMap[opCode];
  if (!fun) {
    throw new Error(
      `Unexpected opcode: ${opCode} (${state.mem.get(state.ptr)!})`
    );
  }

  const [opCallback, paramMappers] = fun;
  const paramCount = paramMappers.length;
  const paramModes = rawParamModes.padEnd(paramCount, '0');
  const rawParams = range(
    state.ptr + BigInt(1),
    state.ptr + BigInt(1) + BigInt(paramCount)
  ).map((val) => state.mem.get(val) || BigInt(0));

  const params = paramMappers.map((cb, i) =>
    cb(state, paramModes[i], rawParams[i])
  );

  /*
  console.log('---');
  console.log('op:', rawOpCode);
  console.log('ptr:', state.ptr);
  console.log('rel:', state.relativeBase);
  console.log('rawMode:', rawParamModes);
  console.log('mode:', paramModes);
  console.log('raw:', rawParams);
  console.log('params:', params);
  console.log(
    'range:',
    range(state.ptr + BigInt(1), state.ptr + BigInt(1) + BigInt(paramCount))
  );
  console.log(
    state.ptr + BigInt(1),
    state.ptr + BigInt(1) + BigInt(paramCount)
  );
  console.log('---');
  //*/

  opCallback(state, params);
};

const processProgram = (data: bigint[], panels: Map<string, Color>) => {
  let state: State = newState(data, panels);

  while (!state.halted) {
    processSingleOpCode(state);
  }

  return state.panels;
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
