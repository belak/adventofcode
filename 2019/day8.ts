import { readNumberList } from './lib/utils';

const items: number[] = readNumberList('input/day8', '');

const chunk = <T>(array: T[], size: number) => {
  const chunked_arr = [];
  for (let i = 0; i < array.length; i++) {
    const last = chunked_arr[chunked_arr.length - 1];
    if (!last || last.length === size) {
      chunked_arr.push([array[i]]);
    } else {
      last.push(array[i]);
    }
  }
  return chunked_arr;
};

const layers = chunk(items, 25 * 6);

let minZeros = 25 * 6 + 1;
let minVal = 0;

layers.forEach((layer) => {
  const zeros = layer.filter((x) => x === 0).length;
  if (zeros < minZeros) {
    minZeros = zeros;
    minVal =
      layer.filter((x) => x === 1).length * layer.filter((x) => x === 2).length;
  }
});

console.log('Part 1:', minVal);

let output = layers.reduce((x, y) =>
  x.map((z, idx) => (x[idx] === 2 ? y[idx] : x[idx]))
);

console.log('Part 2:');
const img = chunk(output, 25);
img.forEach((x) => {
  console.log(x.map((y) => (y ? '1' : ' ')).join(''));
});
