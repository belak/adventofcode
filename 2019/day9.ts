import fs from 'fs';

// Originally based on day7

const items: BigInt[] = fs
  .readFileSync('input/day9')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => BigInt(x));

type OpCallback = (state: State, params: BigInt[]) => void;
type ParamMapper = (state: State, mode: string, v: BigInt) => BigInt;

type State = {
  mem: Map<BigInt, BigInt>;
  ptr: BigInt;
  halted: boolean;
  input: BigInt[];
  out: BigInt;
  relativeBase: BigInt;
};

const newState = (data: BigInt[], input: BigInt[]): State => ({
  ptr: BigInt(0),
  out: BigInt(-1),
  halted: false,
  input: input.slice(),
  mem: data.reduce(
    (mem, val, idx) => mem.set(BigInt(idx), val),
    new Map<BigInt, BigInt>()
  ),
  relativeBase: BigInt(0),
});

const range = (start: BigInt, end: BigInt): BigInt[] =>
  [...Array(Number(end - start)).keys()].map((x) => BigInt(x) + start);

const processAdd = (state: State, params: BigInt[]) => {
  state.mem.set(params[2], params[0] + params[1]);
  state.ptr += BigInt(4);
};

const processMul = (state: State, params: BigInt[]) => {
  state.mem.set(params[2], params[0] * params[1]);
  state.ptr += BigInt(4);
};

const processInp = (state: State, params: BigInt[]) => {
  state.mem.set(params[0], state.input.shift()!);
  state.ptr += BigInt(2);
};

const processOut = (state: State, params: BigInt[]) => {
  console.log('Out:', params[0].toString());

  state.out = params[0];
  state.ptr += BigInt(2);
};

const processJT = (state: State, params: BigInt[]) => {
  state.ptr = params[0] !== BigInt(0) ? params[1] : state.ptr + BigInt(3);
};

const processJF = (state: State, params: BigInt[]) => {
  state.ptr = params[0] === BigInt(0) ? params[1] : state.ptr + BigInt(3);
};

const processLT = (state: State, params: BigInt[]) => {
  state.mem.set(params[2], params[0] < params[1] ? BigInt(1) : BigInt(0));
  state.ptr += BigInt(4);
};

const processEq = (state: State, params: BigInt[]) => {
  state.mem.set(params[2], params[0] === params[1] ? BigInt(1) : BigInt(0));
  state.ptr += BigInt(4);
};

const processRel = (state: State, params: BigInt[]) => {
  state.relativeBase += params[0];
  state.ptr += BigInt(2);
};

const processDone = (state: State, params: BigInt[]) => {
  state.mem = new Map();
  state.ptr = BigInt(-1);
  state.halted = true;
};

function inputParamMapper(state: State, mode: string, v: BigInt): BigInt {
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

function targetParamMapper(state: State, mode: string, v: BigInt): BigInt {
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

const processProgram = (data: BigInt[], input: BigInt[]) => {
  let state: State = newState(data, input);

  while (!state.halted) {
    processSingleOpCode(state);
  }
};

console.log('Part 1:');
processProgram(items, [BigInt(1)]);

console.log('Part 2:');
processProgram(items, [BigInt(2)]);
