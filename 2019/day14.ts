import { readItems } from './lib/utils';

type Target = {
  amount: number;
  name: string;

  requirements: Map<string, number>;
};

const data: Map<string, Target> = readItems('input/day14')
  .map(
    (x): Target => {
      const [reqs, produces] = x.split(' => ', 2);
      const requirements = reqs
        .split(', ')
        .map((y) => y.split(' '))
        .reduce((prev, [reqAmount, key]) => {
          prev.set(key, +reqAmount);
          return prev;
        }, new Map<string, number>());
      const [amount, name] = produces.split(' ');
      return { amount: +amount, name, requirements };
    }
  )
  .reduce((prev, current) => {
    prev.set(current.name, current);
    return prev;
  }, new Map<string, Target>());

const calc = (
  name: string,
  amount: number,
  surplus: Map<string, number> = new Map<string, number>()
): number => {
  if (name === 'ORE') return 1 * amount;

  let surplusAmount = surplus.get(name) || 0;

  // If the amount needed is less than what's leftover, we can return 0 and
  // update the surplus count.
  if (amount <= surplusAmount) {
    surplus.set(name, surplusAmount - amount);
    return 0;
  }

  // Use up the surplus first
  amount -= surplusAmount;
  surplus.set(name, 0);

  const target = data.get(name)!;

  // We need the requested amount divided by how many this recipe produces.
  const needed = Math.ceil(amount / target.amount);

  const reqs = target.requirements;

  // Calculate how much ore each of the requirements would need (multiplied by
  // how many we need), taking into account any surplus.
  const ore = [...reqs.keys()]
    .map((x) => calc(x, reqs.get(x)! * needed, surplus))
    .reduce((a, b) => a + b);

  // Update the surplus. Note that we need to update surplusAmount because we
  // can't just use += on a Map.
  surplusAmount = surplus.get(name) || 0;
  surplus.set(name, target.amount * needed - amount);

  return ore;
};

const part1 = calc('FUEL', 1);
console.log('Part 1:', part1);

const maxOre = 1000000000000;

// Wow, it has been a long time since I've written a binary search.
let low = 0;
let high = maxOre;
while (low < high) {
  const mid = Math.ceil((low + high) / 2);
  const ore = calc('FUEL', mid);
  if (ore > maxOre) {
    high = mid - 1;
  } else if (ore < maxOre) {
    low = mid;
  }
}

console.log('Part 2:', low);
