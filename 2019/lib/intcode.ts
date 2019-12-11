import { bigIntRange as range } from './utils';

type State = {
  mem: Map<bigint, bigint>;
  ptr: bigint;
  relativeBase: bigint;
  input: bigint[];

  halted: boolean;

  inputCallback: InputCallback;
  outputCallback: OutputCallback;
};

type InputCallback = (state: State) => bigint;
type OutputCallback = (state: State, out: bigint) => void;

type OpCallback = (state: State, params: bigint[]) => void;
type ParamMapper = (state: State, mode: string, v: bigint) => bigint;

const newState = (data: bigint[], input: bigint[] = []): State => ({
  ptr: 0n,
  halted: false,
  mem: data.reduce(
    (mem, val, idx) => mem.set(BigInt(idx), val),
    new Map<bigint, bigint>()
  ),
  relativeBase: 0n,

  input,

  inputCallback: (state: State): bigint => {
    const input = state.input.shift();
    if (input === undefined) {
      throw new Error('no input');
    }
    return input;
  },

  outputCallback: (state: State, out: bigint) => {
    console.log('Out:', out.toString());
  },
});

const processAdd = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] + params[1]);
  state.ptr += 4n;
};

const processMul = (state: State, params: bigint[]) => {
  state.mem.set(params[2], params[0] * params[1]);
  state.ptr += 4n;
};

const processInp = (state: State, params: bigint[]) => {
  const input = state.inputCallback(state);

  state.mem.set(params[0], input);
  state.ptr += 2n;
};

const processOut = (state: State, params: bigint[]) => {
  state.outputCallback(state, params[0]);
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

const processNextOpCode = (state: State) => {
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

const processState = (state: State): State => {
  while (!state.halted) {
    processNextOpCode(state);
  }

  return state;
};

const processProgram = (data: bigint[], input: bigint[] = []): State =>
  processState(newState(data, input));

export {
  processProgram,
  processState,
  processNextOpCode,
  InputCallback,
  OutputCallback,
  State,
  newState,
};
