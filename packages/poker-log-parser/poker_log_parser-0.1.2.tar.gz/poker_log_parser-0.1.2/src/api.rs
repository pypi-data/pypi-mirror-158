use crate::pklp::HandVec;
use crate::parsers::*;
use rayon::prelude::*;


pub fn parse_string_into(src: &str, hands: &mut HandVec) -> Result<(), String> {
    let site = detect_site(&src)?;
    parse_str(site, src, hands);
    Ok(())
}


pub fn parse_string(src: &str) -> Result<HandVec, String> {
    let mut hands = HandVec::default();
    parse_string_into(src, &mut hands)?;
    Ok(hands)
}


pub fn parse_path_into(path: &str, hands: &mut HandVec) -> Result<(), String> {
    match std::fs::read_to_string(path) {
        Ok(src) => parse_string_into(&src, hands),
        Err(e) => Err(format!("Failed to open file at path '{}' with error {}", path, e)),
    }
}


pub fn parse_path(path: &str) -> Result<HandVec, String> {
    match std::fs::read_to_string(path) {
        Ok(src) => parse_string(&src),
        Err(e) => Err(format!("Failed to open file at path '{}' with error {}", path, e)),
    }
}


pub fn parse_strings(srcs: Vec<String>) -> Vec<HandVec> {
    srcs.par_iter()
        .filter_map(|x| parse_string(x).ok())
        .collect()
}


pub fn parse_paths(paths: &[String]) -> Vec<HandVec> {
    paths.par_iter()
        .filter_map(|x| parse_path(x).ok())
        .collect()
}

// TODO: How should lists of errors be handled?

pub fn combine(v: Vec<HandVec>) -> HandVec {
    HandVec::combine(v)
}

// TODO: To/from bytes

// TODO: Save/load binary

pub fn to_json(v: &HandVec) -> Result<String, String> {
    match crate::json::to_json(v, v) {
        Ok(v) => Ok(v),
        Err(e) => Err(format!("Failed to write json: {}", e))
    }
}


pub fn to_json_ohh(v: &HandVec) -> Result<String, String> {
    match crate::json::to_json_ohh(v, v) {
        Ok(v) => Ok(v),
        Err(e) => Err(format!("Failed to write json: {}", e))
    }
}
