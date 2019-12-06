import fs from 'fs';

type BodyMap = {
  [key: string]: BodyInfo;
};

type BodyInfo = {
  parent: string;
  path: string[];
};

const items = fs
  .readFileSync('input/day6')
  .toString()
  .trim()
  .split('\n')
  .map((x: string) => x.split(')'));

const calculatePath = (body: string, map: BodyMap): string[] => {
  let path = [];
  let curNode = map[body];

  while (map[curNode.parent]) {
    if (map[curNode.parent].path.length) {
      path.push(curNode.parent, ...map[curNode.parent].path);
      break;
    } else {
      path.push(curNode.parent);
      curNode = map[curNode.parent];
    }
  }

  return path;
};

const generateMap = (input: string[][]): BodyMap => {
  const parentMap: BodyMap = input.reduce((out, data) => {
    const parent = data[0];
    const node = data[1];

    out[node] = {
      parent,
      path: [],
    };

    return out;
  }, {} as BodyMap);

  return Object.keys(parentMap).reduce((total, val) => {
    return {
      ...total,
      [val]: {
        ...total[val],
        path: calculatePath(val, total),
      },
    };
  }, parentMap);
};

const bodyMap = generateMap(items);

const part1 = Object.keys(bodyMap).reduce(
  (total, val) => total + bodyMap[val].path.length + 1,
  0
);

console.log('Part 1:', part1);

// Take the path from you to the start and santa to the start, remove the common
// beginning and add the lengths together.
const youPath = bodyMap['YOU'].path.reverse();
const sanPath = bodyMap['SAN'].path.reverse();

while (youPath[0] === sanPath[0]) {
  youPath.shift();
  sanPath.shift();
}

const part2 = youPath.length + sanPath.length;

console.log('Part 2:', part2);
