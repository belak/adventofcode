const INPUT_DATA: &str = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/data/day1.txt"));

fn main() {
    let data = parse_data(INPUT_DATA);
    println!("Part 1: {}", part1(&data));
    println!("Part 2: {}", part2(&data));
}

const DIGITS: [(&str, u32); 20] = [
    ("0", 0),
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("zero", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
];

fn parse_data(input: &str) -> Vec<&str> {
    input.trim().split('\n').collect()
}

fn part1(data: &[&str]) -> u32 {
    data.iter()
        .map(|line| line.chars().filter(|c| *c >= '0' && *c <= '9').collect())
        .map(|line: String| {
            let line = line.as_bytes();
            if line.len() > 1 {
                (line[0] - b'0') as u32 * 10 + (line[line.len() - 1] - b'0') as u32
            } else {
                (line[0] - b'0') as u32 * 10 + (line[0] - b'0') as u32
            }
        })
        .sum()
}

fn part2(data: &[&str]) -> u32 {
    let mut total = 0;

    for line in data.iter() {
        // Find each digit from the front and the back
        let mut first_digit = u32::MIN;
        let mut first_idx = usize::MAX;
        let mut last_digit = u32::MIN;
        let mut last_idx = usize::MIN;

        for digit in DIGITS.iter() {
            first_idx = match line.find(digit.0) {
                Some(idx) if idx < first_idx => {
                    first_digit = digit.1;
                    idx
                }
                _ => first_idx,
            };

            last_idx = match line.rfind(digit.0) {
                Some(idx) if idx >= last_idx => {
                    last_digit = digit.1;
                    idx
                }
                _ => last_idx,
            };
        }

        total += first_digit * 10 + last_digit;
    }

    total
}

#[cfg(test)]
mod test {
    use super::*;

    const PART1_SAMPLE_DATA: &str = r#"
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
    "#;

    #[test]
    fn sample_data_part1() {
        let data = parse_data(PART1_SAMPLE_DATA);
        assert_eq!(142, part1(&data));
    }

    const PART2_SAMPLE_DATA: &str = r#"
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
    "#;

    #[test]
    fn sample_data_part2() {
        let data = parse_data(PART2_SAMPLE_DATA);
        assert_eq!(282, part2(&data));
    }
}
