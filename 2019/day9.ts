import fs from 'fs';

// Originally based on day7

const items: bigint[] = fs
  .readFileSync('input/day9')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => BigInt(x));

type OpCallback = (state: State, params: bigint[]) => void;
type ParamMapper = (state: State, mode: string, v: bigint) => bigint;

type State = {
  mem: Map<bigint, bigint>;
  ptr: bigint;
  halted: boolean;
  input: bigint[];
  out: bigint;
  relativeBase: bigint;
};

const newState = (data: bigint[], input: bigint[]): State => ({
  ptr: 0n,
  out: -1n,
  halted: false,
  input: input.slice(),
  mem: data.reduce(
    (mem, val, idx) => mem.set(BigInt(idx), val),
    new Map<bigint, bigint>()
  ),
  relativeBase: 0n,
});

const range = (start: bigint, end: bigint): bigint[] =>
  [...Array(Number(end - start)).keys()].map((x) => BigInt(x) + start);

const processAdd = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] + params[1]);
  state.ptr += 4n;
};

const processMul = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] * params[1]);
  state.ptr += 4n;
};

const processInp = (state: State, params: bigint[]) => {
  state.mem.set(params[0], state.input.shift()!);
  state.ptr += 2n;
};

const processOut = (state: State, params: bigint[]) => {
  console.log('Out:', params[0].toString());

  state.out = params[0];
  state.ptr += 2n;
};

const processJT = (state: State, params: bigint[]) => {
  state.ptr = params[0] !== 0n ? params[1] : state.ptr + 3n;
};

const processJF = (state: State, params: bigint[]) => {
  state.ptr = params[0] === 0n ? params[1] : state.ptr + 3n;
};

const processLT = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] < params[1] ? 1n : 0n);
  state.ptr += 4n;
};

const processEq = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] === params[1] ? 1n : 0n);
  state.ptr += 4n;
};

const processRel = (state: State, params: bigint[]) => {
  state.relativeBase += params[0];
  state.ptr += 2n;
};

const processDone = (state: State, params: bigint[]) => {
  state.mem = new Map();
  state.ptr = -1n;
  state.halted = true;
};

function inputParamMapper(state: State, mode: string, v: bigint): bigint {
  switch (mode) {
    case '0':
      return state.mem.get(v) || 0n;
    case '1':
      return v;
    case '2':
      return state.mem.get(state.relativeBase + v) || 0n;
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
    state.ptr + 1n,
    state.ptr + 1n + BigInt(paramCount)
  ).map((val) => state.mem.get(val) || 0n);

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
    range(state.ptr + 1n, state.ptr + 1n + BigInt(paramCount))
  );
  console.log(
    state.ptr + 1n,
    state.ptr + 1n + BigInt(paramCount)
  );
  console.log('---');
  //*/

  opCallback(state, params);
};

const processProgram = (data: bigint[], input: bigint[]) => {
  let state: State = newState(data, input);

  while (!state.halted) {
    processSingleOpCode(state);
  }
};

console.log('Part 1:');
processProgram(items, [1n]);

console.log('Part 2:');
processProgram(items, [2n]);
