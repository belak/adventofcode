import fs from 'fs';

// Originally based on day2

const items = fs
  .readFileSync('input/day5')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => +x);

const processAdd = (state: State, params: number[]): State => ({
  ...state,
  mem: state.mem.map((item, index) =>
    index === params[2] ? params[0] + params[1] : item
  ),
  ptr: state.ptr + 4,
});

const processMul = (state: State, params: number[]): State => ({
  ...state,
  mem: state.mem.map((item, index) =>
    index === params[2] ? params[0] * params[1] : item
  ),
  ptr: state.ptr + 4,
});

const processInp = (state: State, params: number[]): State => ({
  ...state,
  mem: state.mem.map((item, index) =>
    index === params[0] ? state.input : item
  ),
  ptr: state.ptr + 2,
});

const processOut = (state: State, params: number[]): State => {
  console.log('Out:', params[0]);

  return {
    ...state,
    ptr: state.ptr + 2,
  };
};

const processJT = (state: State, params: number[]): State => ({
  ...state,
  ptr: params[0] !== 0 ? params[1] : state.ptr + 3,
});

const processJF = (state: State, params: number[]): State => ({
  ...state,
  ptr: params[0] === 0 ? params[1] : state.ptr + 3,
});

const processLT = (state: State, params: number[]): State => ({
  ...state,
  mem: state.mem.map((item, index) =>
    index === params[2] ? (params[0] < params[1] ? 1 : 0) : item
  ),
  ptr: state.ptr + 4,
});

const processEq = (state: State, params: number[]): State => ({
  ...state,
  mem: state.mem.map((item, index) =>
    index === params[2] ? (params[0] === params[1] ? 1 : 0) : item
  ),
  ptr: state.ptr + 4,
});

const processDone = (state: State, params: number[]): State => ({
  ...state,
  mem: [],
  ptr: -1,
  done: true,
});

function genericParamMapper(mode: string, data: number[], v: number) {
  switch (mode) {
    case '0':
      return data[v];
    case '1':
      return v;
  }

  throw new Error(`Unknown param mode: ${mode}`);
}

const immediateParamMapper: ParamMapper = (mode, data, v) => v;

type OpCallback = (state: State, params: number[]) => State;
type ParamMapper = (mode: string, data: number[], v: number) => number;

type State = {
  mem: number[];
  ptr: number;
  done: boolean;
  input: number;
};

const paramMap: {
  [key: string]: [OpCallback, ParamMapper[]];
} = {
  '01': [
    processAdd,
    [genericParamMapper, genericParamMapper, immediateParamMapper],
  ],
  '02': [
    processMul,
    [genericParamMapper, genericParamMapper, immediateParamMapper],
  ],
  '03': [processInp, [immediateParamMapper]],
  '04': [processOut, [genericParamMapper]],
  '05': [processJT, [genericParamMapper, genericParamMapper]],
  '06': [processJF, [genericParamMapper, genericParamMapper]],
  '07': [
    processLT,
    [genericParamMapper, genericParamMapper, immediateParamMapper],
  ],
  '08': [
    processEq,
    [genericParamMapper, genericParamMapper, immediateParamMapper],
  ],
  '99': [processDone, []],
};

const processOpCode = (data: number[], input: number) => {
  let state: State = {
    ptr: 0,
    mem: data.slice(),
    done: false,
    input,
  };

  while (!state.done) {
    const rawParamModes = state.mem[state.ptr]
      .toString()
      .slice(0, -2)
      .split('')
      .reverse()
      .join('');
    const opCode = state.mem[state.ptr]
      .toString()
      .slice(-2)
      .padStart(2, '0');

    const fun = paramMap[opCode];
    if (!fun) {
      throw new Error(`Unexpected opcode: ${opCode} (${state.mem[state.ptr]})`);
    }

    const [cb, paramMappers] = fun;
    const paramCount = paramMappers.length;
    const paramModes = rawParamModes.padEnd(paramCount, '0');
    const rawParams = state.mem.slice(
      state.ptr + 1,
      state.ptr + 1 + paramCount
    );
    const params = paramMappers.map((cb, i) =>
      cb(paramModes[i], state.mem, rawParams[i])
    );

    // console.log(opCode, params);
    state = cb(state, params);
    // console.log('Ptr:', ptr)
  }

  return -1;
};

console.log('Part 1:');
processOpCode(items, 1);

console.log('Part 2:');
processOpCode(items, 5);
