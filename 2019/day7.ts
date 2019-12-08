import fs from 'fs';

// Originally based on day5

const items = fs
  .readFileSync('input/day7')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => +x);

const processAdd = (state: State, params: number[]): Partial<State> => ({
  mem: state.mem.map((item, index) =>
    index === params[2] ? params[0] + params[1] : item
  ),
  ptr: state.ptr + 4,
});

const processMul = (state: State, params: number[]): Partial<State> => ({
  mem: state.mem.map((item, index) =>
    index === params[2] ? params[0] * params[1] : item
  ),
  ptr: state.ptr + 4,
});

const processInp = (state: State, params: number[]): Partial<State> => ({
  mem: state.mem.map((item, index) =>
    index === params[0] ? state.input[0] : item
  ),
  input: state.input.slice(1),
  ptr: state.ptr + 2,
});

const processOut = (state: State, params: number[]): Partial<State> => {
  //console.log('Out:', params[0]);

  return {
    ptr: state.ptr + 2,
    out: params[0],
    done: true,
  };
};

const processJT = (state: State, params: number[]): Partial<State> => ({
  ptr: params[0] !== 0 ? params[1] : state.ptr + 3,
});

const processJF = (state: State, params: number[]): Partial<State> => ({
  ptr: params[0] === 0 ? params[1] : state.ptr + 3,
});

const processLT = (state: State, params: number[]): Partial<State> => ({
  mem: state.mem.map((item, index) =>
    index === params[2] ? (params[0] < params[1] ? 1 : 0) : item
  ),
  ptr: state.ptr + 4,
});

const processEq = (state: State, params: number[]): Partial<State> => ({
  mem: state.mem.map((item, index) =>
    index === params[2] ? (params[0] === params[1] ? 1 : 0) : item
  ),
  ptr: state.ptr + 4,
});

const processDone = (state: State, params: number[]): Partial<State> => ({
  mem: [],
  ptr: -1,
  done: true,
  halted: true,
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

type OpCallback = (state: State, params: number[]) => Partial<State>;
type ParamMapper = (mode: string, data: number[], v: number) => number;

type State = {
  mem: number[];
  ptr: number;
  done: boolean;
  halted: boolean;
  input: number[];
  out: number;
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

const processSingleOpCode = (state: State): State => {
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
  const rawParams = state.mem.slice(state.ptr + 1, state.ptr + 1 + paramCount);
  const params = paramMappers.map((cb, i) =>
    cb(paramModes[i], state.mem, rawParams[i])
  );

  return {
    ...state,
    ...cb(state, params),
  };
};

const newState = (data: number[], input: number[]): State => ({
  ptr: 0,
  out: -1,
  done: false,
  halted: false,
  input: input.slice(),
  mem: data.slice(),
});

const processPipeline = (data: number[], input: number[]): number => {
  let prev = 0;

  input.forEach((x) => {
    let state: State = newState(data, [x, prev]);
    while (!state.halted) {
      state = processSingleOpCode(state);
    }
    prev = state.out;
  });

  return prev;
};

const processFeedback = (data: number[], input: number[]): number => {
  const states = input.map((x) => newState(data, [x]));

  let prev = 0;

  // Keep doing this as long as the first engine hasn't halted.
  while (!states[0].halted) {
    states.forEach((state, idx) => {
      // Reset the done flag, so we can continue processing instructions.
      state.done = false;

      // Push the output of the previous to the input stack of the next program.
      state.input.push(prev);

      while (!state.done) {
        state = processSingleOpCode(state);
      }

      // Update the prev value to the output of the latest state.
      prev = state.out;

      // Update the states array to include this final state.
      states[idx] = state;
    });
  }

  return prev;
};

const permutations = <T>(inputArr: T[]) => {
  let result: T[][] = [];

  const permute = (arr: T[], m: T[] = []) => {
    if (arr.length === 0) {
      result.push(m);
    } else {
      for (let i = 0; i < arr.length; i++) {
        let curr = arr.slice();
        let next = curr.splice(i, 1);
        permute(curr.slice(), m.concat(next));
      }
    }
  };

  permute(inputArr);

  return result;
};

const part1Input = [0, 1, 2, 3, 4];
const part1InputOptions = permutations(part1Input);

const part1 = Math.max(
  ...part1InputOptions.map((x) => processPipeline(items, x))
);

console.log('Part 1:', part1);

const part2Input = [5, 6, 7, 8, 9];
const part2InputOptions = permutations(part2Input);
const part2 = Math.max(
  ...part2InputOptions.map((x) => processFeedback(items, x))
);
console.log('Part 2:', part2);
