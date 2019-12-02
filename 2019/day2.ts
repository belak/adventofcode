import fs from 'fs';

import chalk from 'chalk';

const items = fs
  .readFileSync('input/day2')
  .toString()
  .trim()
  .split(',')
  .map((x: string) => +x);

const processAdd = (
  data: number[],
  param1: number,
  param2: number,
  target: number
) =>
  data.map((item, index) =>
    index === target ? data[param1] + data[param2] : item
  );

const processMul = (
  data: number[],
  param1: number,
  param2: number,
  target: number
  ) =>
  data.map((item, index) =>
    index === target ? data[param1] * data[param2] : item
  );

const processOpCode = (data: number[], noun: number, verb: number) => {
  let ret = data.slice();
  ret[1] = noun;
  ret[2] = verb;

  for (let i = 0; i < ret.length; i++) {
    switch (data[i]) {
      case 1:
        ret = processAdd(ret, ret[i + 1], ret[i + 2], ret[i + 3]);
        i += 3;
        break;
      case 2:
        ret = processMul(ret, ret[i + 1], ret[i + 2], ret[i + 3]);
        i += 3;
        break;
      case 99:
        return ret[0];
        break;
    }
  }

  return -1;
};

console.log(`${chalk.green('Calc:')} %d`, processOpCode(items, 12, 2));

for (let i = 0; i <= 99; i++) {
  for (let j = 0; j <= 99; j++) {
    if (processOpCode(items, i, j) == 19690720) {
      console.log(`${chalk.green('Answer:')} %d`, 100 * i + j);
    }
  }
}
