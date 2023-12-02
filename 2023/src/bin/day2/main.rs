const INPUT_DATA: &str = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/data/day2.txt"));

fn main() {
    let data = parse_data(INPUT_DATA);
    println!("Part 1: {}", part1(&data));
    println!("Part 2: {}", part2(&data));
}

type InputData = Vec<(u32, Vec<Turn>)>;

struct Turn {
    r: i32,
    g: i32,
    b: i32,
}

fn parse_data(input: &str) -> InputData {
    input
        .trim()
        .split('\n')
        .map(|line| {
            let mut parts = line.split(": ");
            let header = parts.next().unwrap();
            let data = parts.next().unwrap();

            let mut header_parts = header.split(' ');
            let _ = header_parts.next().unwrap();
            let idx = header_parts.next().unwrap();

            let mut turns = Vec::new();

            for turn_data in data.split("; ") {
                let mut turn = Turn { r: 0, g: 0, b: 0 };
                for play in turn_data.split(", ") {
                    let mut play_parts = play.split(' ');

                    let count = play_parts.next().unwrap().parse().unwrap();
                    let name = play_parts.next().unwrap();

                    match name {
                        "red" => turn.r = count,
                        "green" => turn.g = count,
                        "blue" => turn.b = count,
                        _ => unimplemented!("unknown play color"),
                    }
                }

                turns.push(turn);
            }

            (idx.parse().unwrap(), turns)
        })
        .collect()
}

fn part1(data: &InputData) -> u32 {
    data.iter()
        .map(|(idx, turns)| {
            let mut final_turn = Turn { r: 0, g: 0, b: 0 };
            for turn in turns.iter() {
                if turn.r > final_turn.r {
                    final_turn.r = turn.r;
                }
                if turn.g > final_turn.g {
                    final_turn.g = turn.g;
                }
                if turn.b > final_turn.b {
                    final_turn.b = turn.b;
                }
            }
            (idx, final_turn)
        })
        .filter(|(_idx, turn)| turn.r <= 12 && turn.g <= 13 && turn.b <= 14)
        .map(|(idx, _)| idx)
        .sum()
}

fn part2(data: &InputData) -> i32 {
    data.iter()
        .map(|(_, turns)| {
            let mut final_turn = Turn { r: 0, g: 0, b: 0 };
            for turn in turns.iter() {
                if turn.r > final_turn.r {
                    final_turn.r = turn.r;
                }
                if turn.g > final_turn.g {
                    final_turn.g = turn.g;
                }
                if turn.b > final_turn.b {
                    final_turn.b = turn.b;
                }
            }
            final_turn.r * final_turn.g * final_turn.b
        })
        .sum()
}

#[cfg(test)]
mod test {
    use super::*;

    const PART1_SAMPLE_DATA: &str = r#"}
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    "#;

    #[test]
    fn sample_data_part1() {
        let data = parse_data(PART1_SAMPLE_DATA);
        assert_eq!(8, part1(&data));
    }

    const PART2_SAMPLE_DATA: &str = PART1_SAMPLE_DATA;

    #[test]
    fn sample_data_part2() {
        let data = parse_data(PART2_SAMPLE_DATA);
        assert_eq!(2286, part2(&data));
    }
}
