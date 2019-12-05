import fs from 'fs';

// Originally based on day2

const items = fs
  .readFileSync('input/day5')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => +x);

const processAdd = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  param2: number,
  target: number
): [number[], number, boolean] => [
  data.map((item, index) => (index === target ? param1 + param2 : item)),
  ptr + 4,
  false,
];

const processMul = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  param2: number,
  target: number
): [number[], number, boolean] => [
  data.map((item, index) => (index === target ? param1 * param2 : item)),
  ptr + 4,
  false,
];

const processInp = (
  ptr: number,
  data: number[],
  input: number,
  target: number
): [number[], number, boolean] => [
  data.map((item, index) => (index === target ? input : item)),
  ptr + 2,
  false,
];

const processOut = (
  ptr: number,
  data: number[],
  input: number,
  target: number
): [number[], number, boolean] => {
  console.log('Out:', target);
  return [data, ptr + 2, false];
};

const processJT = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  target: number
): [number[], number, boolean] => {
  return [data, param1 !== 0 ? target : ptr + 3, false];
};

const processJF = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  target: number
): [number[], number, boolean] => {
  return [data, param1 === 0 ? target: ptr + 3, false];
};

const processLT = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  param2: number,
  target: number
): [number[], number, boolean] => [
  data.map((item, index) => (index === target ? (param1 < param2 ? 1 : 0) : item)),
  ptr + 4,
  false,
];

const processEq = (
  ptr: number,
  data: number[],
  input: number,
  param1: number,
  param2: number,
  target: number
): [number[], number, boolean] => [
  data.map((item, index) => (index === target ? (param1 === param2 ? 1 : 0) : item)),
  ptr + 4,
  false,
];

const processDone = (
  ptr: number,
  data: number[],
  input: number,
  target: number
): [number[], number, boolean] => {
  return [[], -1, true];
};

function genericParamMapper(mode: string, data: number[], v: number) {
  switch (mode) {
    case '0':
      return data[v];
    case '1':
      return v;
  }

  throw new Error(`Unknown param mode: ${mode}`);
}

const immediateParamMapper = (mode: string, data: number[], v: number) => v;

type OpCallback = (
  ptr: number,
  data: number[],
  input: number,
  ...params: number[]
) => [number[], number, boolean];
type ParamMapper = (mode: string, data: number[], v: number) => number;

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
  '07': [processLT, [genericParamMapper, genericParamMapper, immediateParamMapper]],
  '08': [processEq, [genericParamMapper, genericParamMapper, immediateParamMapper]],
  '99': [processDone, []],
};

const processOpCode = (data: number[], input: number) => {
  let ptr = 0;
  let ret = data.slice();
  let done = false;

  while (!done) {
    const rawParamModes = ret[ptr]
      .toString()
      .slice(0, -2)
      .split('')
      .reverse()
      .join('');
    const opCode = ret[ptr]
      .toString()
      .slice(-2)
      .padStart(2, '0');

    const fun = paramMap[opCode];
    if (!fun) {
      throw new Error(`Unexpected opcode: ${opCode} (${ret[ptr]})`);
    }

    const [cb, paramMappers] = fun;
    const paramCount = paramMappers.length;
    const paramModes = rawParamModes.padEnd(paramCount, '0');
    const rawParams = ret.slice(ptr + 1, ptr + 1 + paramCount);
    const params = paramMappers.map((cb, i) =>
      cb(paramModes[i], ret, rawParams[i])
    );

    // console.log(opCode, params);
    [ret, ptr, done] = cb(ptr, ret, input, ...params);
    // console.log('Ptr:', ptr)
  }

  return -1;
};

console.log('Part 1:');
processOpCode(items, 1);

console.log('Part 2:');
processOpCode(items, 5);
