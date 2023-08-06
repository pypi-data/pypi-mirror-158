#![feature(portable_simd)]

mod simd;
#[macro_use]
mod pklp;
mod parsers;
mod api;
mod json;
mod combine;

use parsers::parser::Parse;
use pklp::PrintHandVec;
use parsers::*;

use std::time::{Duration, Instant};
use rayon::prelude::*;


fn main_json() {
    // let cards = cards!(Qh Ad);
    // let r = json::to_json(&cards, ()).unwrap();
    // println!("{}", &r);
}


fn main_basic() {
    // let src = std::fs::read_to_string("tests/data/example/pokerstars_obf.txt").unwrap();
    let src = std::fs::read_to_string("tests/data/PokerStars/_ante.txt").unwrap();
    let mut hands = pklp::HandVec::new();
    let mut p = parser::Parser::new(&src, &mut hands);
    PokerStars::parse(&mut p);
}


enum MainType {
    MultiThreaded,
    SingleThreaded,
    Debug
}
fn main_bench(t: MainType, print_info: bool) {
    let mut info = pklp::HandVecExpectedSize::default();

    // for d in ["PokerStarsObf"] {
    for d in ["Pluribus", "PokerStars", "OnGame", "PokerStarsObf"] {
            let paths = std::fs::read_dir(&format!("tests/data/{}", d)).unwrap()
                .map(|x| x.unwrap().path())
                .collect::<Vec<std::path::PathBuf>>();
    
            let files = paths[..std::cmp::min(1000, paths.len())].par_iter()
                .map(|p| std::fs::read_to_string(&p).unwrap())
                .collect::<Vec<String>>();
    
            let size_bytes = files.iter().map(|x| x.len()).sum::<usize>();
            let start = Instant::now();
            let hands = match t {
                MainType::MultiThreaded => api::parse_strings(files),
                MainType::SingleThreaded => files.iter().map(|x| api::parse_string(x).unwrap()).collect::<Vec<pklp::HandVec>>(),
                MainType::Debug => files.iter().enumerate().map(|(i,x)| { println!("{}", paths[i].display()); api::parse_string(x).unwrap() }).collect::<Vec<pklp::HandVec>>(),
            };
            let duration = start.elapsed();
            info.update(&hands);
    
            let total = hands.iter().map(|x| x.hands.len()).sum::<usize>();
            println!("{:15} ({:6.1} MB in RAM)     hands: {:9},     time: {:.2},     hands/sec: {:8},     MB/sec: {:5}", 
                d, 
                hands.iter().map(|x| x.size_bytes()).sum::<usize>() as f64 / 1000000.0,
                total,
                duration.as_micros() as f64 / 1000000.0,
                (total as f64 / duration.as_micros() as f64 * 1000000.0) as u64,
                (size_bytes as f64 / duration.as_micros() as f64) as u64);
        }
        
        if print_info {
            println!("MAX {:?}", info.max_rounded_up());
            println!("AVG {:?}", info.avg_rounded_up());
        }
}


fn main_detect() {
    let mut paths = std::fs::read_dir("tests/data/example").unwrap()
        .map(|x| x.unwrap().path())
        .collect::<Vec<std::path::PathBuf>>();
    paths.sort();

    for p in &paths {
        match std::fs::read_to_string(p) {
            Ok(s) => {
                if let Ok(s) = detect_site(&s) {
                    println!("{:60} - {:?}", p.display(), s);
                } else {
                    println!("{:60} - Invalid - '{}'", p.display(), s.trim_start().lines().next().unwrap());
                }
            }
            Err(e) => {
                println!("{:60} - Error ({:?})", p.display(), e);
            }
        }
    }
}

fn main() {
    // TODO: CLI

    // main_json();
    
    // main_basic();

    // main_detect();

    let print_info = false;
    // let print_info = true;
    main_bench(MainType::MultiThreaded, print_info);
    // main_bench(MainType::SingleThreaded, print_info);
    // main_bench(MainType::Debug, print_info);
}
