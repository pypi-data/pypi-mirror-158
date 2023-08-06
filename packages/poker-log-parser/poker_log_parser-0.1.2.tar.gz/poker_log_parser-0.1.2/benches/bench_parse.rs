extern crate poker_log_parser;
use poker_log_parser::api;

use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn parse_benchmark(c: &mut Criterion) {
    let data_pokerstars = std::fs::read_to_string("tests/data/bench/pokerstars.txt").unwrap();
    let data_pluribus = std::fs::read_to_string("tests/data/bench/pluribus.txt").unwrap();
    let data_ongame = std::fs::read_to_string("tests/data/bench/ongame_obf.txt").unwrap();
    c.bench_function("parse (50) - pokerstars", |b| b.iter(|| api::parse_string(black_box(&data_pokerstars))));
    c.bench_function("parse (50) - pluribus", |b| b.iter(|| api::parse_string(black_box(&data_pluribus))));
    c.bench_function("parse (50) - ongame", |b| b.iter(|| api::parse_string(black_box(&data_ongame))));
}

criterion_group!(benches, parse_benchmark);
criterion_main!(benches);
