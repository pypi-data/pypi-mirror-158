use crate::pklp::*;
use crate::simd::NameCacheSimd;

use memchr;

//region Parse

pub trait Parse: ParseHeader + ParsePreFlop + ParseStreets + ParseSummary + ParseSync {
    fn parse(p: &mut Parser);
    fn parse_hand(p: &mut Parser) -> Option<Hand>;
}

pub trait ParseSync {
    fn parse_sync(_p: &mut Parser) {}
}

pub trait ParseHeader {
    fn parse_header(p: &mut Parser) -> Option<Header>;
}

pub trait ParsePreFlop {
    fn parse_preflop(p: &mut Parser, currency: char) -> Option<Street>;
}

pub trait ParseStreets {
    fn parse_streets(p: &mut Parser, currency: char) -> Option<StreetArray>;
}

pub trait ParseSummary {
    fn parse_summary(p: &mut Parser, currency: char) -> Option<Summary>;
}

pub trait ParseAction: ParseActionHeader + ParseActionPreFlop + ParseActionStreet {}
impl<T> ParseAction for T where T: ParseActionHeader + ParseActionPreFlop + ParseActionStreet {}

pub trait ParseActionHeader {
    fn parse_action_header(p: &mut Parser, currency: char) -> Option<Action>;
}
pub trait ParseActionPreFlop {
    fn parse_action_preflop(p: &mut Parser, currency: char) -> Option<Action>;
}
pub trait ParseActionStreet {
    fn parse_action_street(p: &mut Parser, currency: char) -> Option<Action>;
}


pub trait ParseActionHeaderBlindOnly {}

pub trait ParseActionBlind {
    fn parse_action_blind(p: &mut Parser, currency: char) -> Option<Action>;
}

impl<T> ParseActionHeader for T where T: ParseActionHeaderBlindOnly + ParseActionBlind {
    fn parse_action_header(p: &mut Parser, currency: char) -> Option<Action> {
        Self::parse_action_blind(p, currency)
    }
}


pub trait ParsePreFlopDealtTo {
    const PREFLOP_HEADER_LINE_COUNT: usize = 1;
}

pub trait ParsePreFlopActionsOnly {
    const PREFLOP_HEADER_LINE_COUNT: usize = 1;
}


pub trait ParseStreet {
    fn is_summary_line(line: &str) -> bool;
    fn parse_street_header(p: &mut Parser) -> (StreetType, Cards);
}


pub trait ParseActionList: ParseAction {
    fn is_section_line(line: &str) -> bool;

    fn parse_action_list_header(p: &mut Parser, currency: char) -> Option<ActionSpan> {
        let actions = p.hands.begin_span(ActionSpan::default());
        while !Self::is_section_line(p.line) {
            let action = Self::parse_action_header(p, currency)?;
            p.advance();
            p.hands.actions.push(action);
        }
        Some(p.hands.end_span(actions))
    }

    fn parse_action_list_preflop(p: &mut Parser, currency: char) -> Option<ActionSpan> {
        let actions = p.hands.begin_span(ActionSpan::default());
        while !Self::is_section_line(p.line) {
            let action = Self::parse_action_preflop(p, currency)?;
            p.advance();
            p.hands.actions.push(action);
        }
        Some(p.hands.end_span(actions))
    }

    fn parse_action_list_street(p: &mut Parser, currency: char) -> Option<ActionSpan> {
        let actions = p.hands.begin_span(ActionSpan::default());
        while !Self::is_section_line(p.line) {
            let action = Self::parse_action_street(p, currency)?;
            p.advance();
            p.hands.actions.push(action);
        }
        Some(p.hands.end_span(actions))
    }
}


impl<T> Parse for T where T: ParseHeader + ParsePreFlop + ParseStreets + ParseSummary + ParseSync {
    fn parse(p: &mut Parser) {
        while !p.eof() {
            if p.line.is_empty() { p.advance(); continue; }
            if let Some(hand) = Self::parse_hand(p) {
                p.hands.hands.push(hand);
            } else {
                Self::parse_sync(p);
            }
        }
    }

    fn parse_hand(p: &mut Parser) -> Option<Hand> {
        p.players.clear();
        p.players_begin = p.hands.players.len();
        p.src_offset = p.hands.src.len();
        let mut header = Self::parse_header(p)?;
        let preflop = Self::parse_preflop(p, header.currency)?;
        let streets = Self::parse_streets(p, header.currency)?;
        let summary = Self::parse_summary(p, header.currency)?;
        header.players = PlayerSpan::new(p.players_begin, p.players.len());
        Some(Hand{header, preflop, streets, summary, src_offset: p.src_offset})
    }
}


impl<T> ParseStreets for T where T: ParseStreet + ParseActionList {
    fn parse_streets(p: &mut Parser, currency: char) -> Option<StreetArray> {
        let (flops_begin, turns_begin, riv_begin, sh_begin) = (p.hands.flops.len(), p.hands.turns.len(), p.hands.rivers.len(), p.hands.showdowns.len());
        let mut id = 0;
        while !Self::is_summary_line(p.line) {
            let (street_type, cards) = Self::parse_street_header(p);
            let actions = Self::parse_action_list_street(p, currency)?;
            p.hands[street_type].push(Street{cards, id, actions});
            id += 1;
        }
        Some((
            FlopSpan::range(flops_begin, p.hands.flops.len()), 
            TurnSpan::range(turns_begin, p.hands.turns.len()), 
            RiverSpan::range(riv_begin, p.hands.rivers.len()), 
            ShowdownSpan::range(sh_begin, p.hands.showdowns.len()),
        ))
    }
}


impl<T> ParsePreFlop for T where T: ParsePreFlopActionsOnly + ParseActionList {
    fn parse_preflop(p: &mut Parser, currency: char) -> Option<Street> { 
        for _ in 0..Self::PREFLOP_HEADER_LINE_COUNT {
            p.advance();
        }
        let actions = Self::parse_action_list_preflop(p, currency)?;
        Some(Street{cards: Cards::default(), id: 0, actions})
    }
}


pub trait ParseTrimPlayerName {
    fn trim_player_name(name: &str) -> &str {
        name
    }
}

pub trait ParseActionDealtTo: ParseTrimPlayerName {
    const DEALT_TO_PREFIX: &'static str = "Dealt to ";

    fn parse_action_dealt_to(p: &mut Parser, _: char) -> Option<Action> {
        let cards_begin = p.line.rfind('[').unwrap();
        let cards = parse_cards(&p.line[cards_begin + 1..p.line.len() - 1]);
        let name = &p.line[Self::DEALT_TO_PREFIX.len()..cards_begin - 1];
        Some(p.action_cards(ActionType::Dealt, Self::trim_player_name(name), cards))
    }
}

impl<T> ParseActionPreFlop for T where T: ParsePreFlopDealtTo + ParseActionDealtTo + ParseActionStreet {
    fn parse_action_preflop(p: &mut Parser, currency: char) -> Option<Action> {
        if p.line.starts_with(Self::DEALT_TO_PREFIX) {
            Self::parse_action_dealt_to(p, currency)
        } else {
            Self::parse_action_street(p, currency)
        }
    }
}

//endregion

//region Helper Traits

pub trait ParseNumberWithComma {}

pub trait ParseNumber {
    fn extract_integer(input: &str) -> Option<usize> {
        let mut offset = 0;
        for v in input.chars() {
            if !v.is_numeric() { break; }
            offset += v.len_utf8();
        }
        if offset > 0 { Some(offset) } else { None }
    }
    
    
    fn parse_integer(input: &str) -> Option<(u64, usize)> {
        if let Some(i) = Self::extract_integer(input) {
            if let Ok(v) = str::parse::<u64>(&input[..i]) {
                return Some((v, i))
            }
        }
        None
    }
    
    
    fn extract_float(input: &str) -> Option<usize> {
        if let Some(i) = Self::extract_integer(input) {
            Some(if input[i..].starts_with('.') {
                if let Some(x) = Self::extract_integer(&input[i+1..]) {
                    i + x + 1
                } else {
                    i
                }
            }
            else {
                i
            })
        } else {
            None
        }
    }
    
    
    fn parse_float(input: &str) -> Option<(Number, usize)> {
        if let Some(i) = Self::extract_float(input) {
            if let Ok(v) = str::parse::<Number>(&input[..i]) {
                return Some((v, i))
            }
        }
        None
    }
}


impl<T> ParseNumber for T where T: ParseNumberWithComma {    
    fn extract_integer(input: &str) -> Option<usize> {
        let mut offset = 0;
        for v in input.chars() {
            if !(v.is_numeric() || v == ',') { break; }
            offset += v.len_utf8();
        }
        if offset > 0 { Some(offset) } else { None }
    }

    fn extract_float(input: &str) -> Option<usize> {
        if let Some(i) = Self::extract_integer(input) {
            Some(if input[i..].starts_with('.') {
                if let Some(x) = Self::extract_integer(&input[i+1..]) {
                    i + x + 1
                } else {
                    i
                }
            }
            else {
                i
            })
        } else {
            if input.starts_with('.') {
                if let Some(x) = Self::extract_integer(&input[1..]) {
                    Some(x + 1)
                } else {
                    None
                }
            }
            else {
                None
            }
        }
    }

    fn parse_integer(input: &str) -> Option<(u64, usize)> {
        if let Some(i) = Self::extract_integer(input) {
            if let Ok(v) = str_to_integer(&input[..i]) {
                return Some((v, i))
            }
        }
        None
    }

    fn parse_float(input: &str) -> Option<(Number, usize)> {
        if let Some(i) = Self::extract_float(input) {
            if let Ok(v) = str_to_float(&input[..i]) {
                return Some((v, i))
            }
        }
        None
    }
}



impl<T> ParseCurrency for T where T: ParseNumber {}

pub trait ParseCurrency: ParseNumber {
    fn extract_currency(input: &str, currency: char, currency_begin: usize) -> Option<(Number, usize)> {
        let begin = currency_begin + currency.len_utf8();
        let (n, offset) = Self::parse_float(&input[begin..])?;
        Some((n, begin + offset))
    }

    fn find_currency(input: &str, currency: char) -> Option<(Number, (usize, usize))> {
        let r = if currency.len_utf8() == 1 {
            input.find_fast_char(currency)
        } else {
            let mut bytes = [0; 4];
            let s = currency.encode_utf8(&mut bytes);
            memchr::memmem::find(input.as_bytes(), s.as_bytes())
        };

        if let Some(currency_begin) = r {
            let (n, end) = Self::extract_currency(input, currency, currency_begin)?;
            Some((n, (currency_begin, end)))
        } else {
            None
        }
    }

    fn rfind_currency(input: &str, currency: char) -> Option<(Number, (usize, usize))> {
        let r = if currency.len_utf8() == 1 {
            input.rfind_fast_char(currency)
        } else {
            let mut bytes = [0; 4];
            let s = currency.encode_utf8(&mut bytes);
            memchr::memmem::rfind(input.as_bytes(), s.as_bytes())
        };

        if let Some(currency_begin) = r {
            if let Some((n, end)) = Self::extract_currency(input, currency, currency_begin) {
                return Some((n, (currency_begin, end)));
            }
        }
        None
    }
}

//endregion

//region Parser

pub struct Parser<'a> {
    pub lines: FastSplit<'a, 'static>,
    pub line: &'a str,
    pub data: &'a str,
    pub hands: &'a mut HandVec,
    pub players: NameCacheSimd,
    pub players_begin: usize,
    pub src_offset: usize,
}


impl<'a> Parser<'a> {
    pub fn new(s: &'a str, hands: &'a mut HandVec) -> Parser<'a> {
        let lines = split_lines(s);
        let mut p = Self{lines, line: "", data: s, hands, players: NameCacheSimd::new(), players_begin: 0, src_offset: 0};
        p.advance();
        p
    }

    pub fn eof(&self) -> bool { 
        self.line == "@@@" 
    }

    pub fn advance(&mut self) { 
        if let Some(r) = self.lines.next() {
            self.line = &self.data[r];
        } else {
            self.line = "@@@";
        }
    }
    
    pub fn push_str(&mut self, v: &str) -> Span {
        self.hands.push_str(v)
    }

    pub fn action_no_data(&self, kind: ActionType, name: &str) -> Action {
        Action::no_data(kind, self.players.find(name))
    }

    pub fn action_num(&mut self, kind: ActionType, name: &str, amount: Number) -> Action {
        let data = ActionData::new_num(amount);
        Action::new(kind, self.players.find(name), data)
    }
    
    pub fn action_cards(&mut self, kind: ActionType, name: &str, cards: Cards) -> Action {
        let id = self.hands.cards.len() as u32;
        self.hands.cards.push(cards);
        let data = ActionData::new_handle(id);
        Action::new(kind, self.players.find(name), data)
    }

    pub fn action_num_pair(&mut self, kind: ActionType, name: &str, v0: Number, v1: Number) -> Action {
        let id = self.hands.nums.len() as u32;
        self.hands.nums.push(v0);
        self.hands.nums.push(v1);
        let data = ActionData::new_handle(id);
        Action::new(kind, self.players.find(name), data)
    }

    pub fn add_player(&mut self, name: &str, seat: u8, chips: Number) -> u8 {
        let n = self.push_str(name);
        let id = self.players.len() as u8;
        self.players.add(name);
        self.hands.players.push(Player{name: n, seat, chips});
        id
    }

    pub fn player_id(&mut self, name: &str) -> u8 {
        let id = self.players.find(name);
        if id != 32 {
            id
        } else {
            self.add_player(name, SEAT_NONE, 0.0)
        }
    }

    pub fn player_mut(&mut self, id: u8) -> &mut Player {
        &mut self.hands.players[self.players_begin + id as usize]
    }
}

//endregion

//region String Ops

pub trait StrOps {
    fn find_after(&self, v: &str) -> Option<usize>;
    fn rfind_after(&self, v: &str) -> Option<usize>;
    fn starts_with_after(&self, v: &str) -> Option<usize>;
    fn ends_with_before(&self, v: &str) -> Option<usize>;
    fn split_after(&self, v: &str) -> Option<(&str, usize)>;
    fn rsplit_after(&self, v: &str) -> Option<(&str, usize)>;

    fn find_fast_char(&self, c: char) -> Option<usize>;
    fn rfind_fast_char(&self, c: char) -> Option<usize>;

    fn fast_split_char<'h>(&'h self, c: char) -> FastSplit<'h, 'static>;
    fn fast_split_str<'h, 'n>(&'h self, v: &'n str) -> FastSplit<'h, 'n>;
}

impl StrOps for str {
    fn find_after(&self, v: &str) -> Option<usize> {
        self.find(v).map(|x| x + v.len())
    }

    fn rfind_after(&self, v: &str) -> Option<usize> {
        self.rfind(v).map(|x| x + v.len())
    }

    fn starts_with_after(&self, v: &str) -> Option<usize> {
        if self.starts_with(v) { Some(v.len()) } else { None }
    }

    fn ends_with_before(&self, v: &str) -> Option<usize> {
        if self.ends_with(v) { Some(self.len() - v.len()) } else { None }
    }
    
    fn split_after(&self, v: &str) -> Option<(&str, usize)> {
        let end = self.find(v)?;
        Some((&self[..end], end + v.len()))
    }

    fn rsplit_after(&self, v: &str) -> Option<(&str, usize)> {
        let end = self.rfind(v)?;
        Some((&self[..end], end + v.len()))
    }

    fn find_fast_char(&self, c: char) -> Option<usize>
    {
        assert!(c.len_utf8() == 1);
        memchr::memchr(c as u8, self.as_bytes())
    }

    fn rfind_fast_char(&self, c: char) -> Option<usize>
    {
        assert!(c.len_utf8() == 1);
        memchr::memrchr(c as u8, self.as_bytes())
    }

    fn fast_split_char<'h>(&'h self, c: char) -> FastSplit<'h, 'static>
    {
        FastSplit::from_char(c, self)
    }

    fn fast_split_str<'h, 'n>(&'h self, v: &'n str) -> FastSplit<'h, 'n>
    {
        FastSplit::from_str(v, self)
    }
}

pub enum FastSplit<'h, 'n> {
    Char(FastSplitChar<'h>),
    Str(FastSplitStr<'h, 'n>),
}

impl<'h, 'n> FastSplit<'h, 'n> {
    pub fn from_char(needle: char, haystack: &'h str) -> Self { Self::Char(FastSplitChar::new(needle, haystack)) }
    pub fn from_str(needle: &'n str, haystack: &'h str) -> Self { Self::Str(FastSplitStr::new(needle, haystack)) }
}

impl<'h, 'n> Iterator for FastSplit<'h, 'n> {
    type Item = std::ops::Range<usize>;
    fn next(&mut self) -> Option<Self::Item> {
        match self {
            Self::Char(v) => v.next(),
            Self::Str(v) => v.next(),
        }
    }
}


pub struct FastSplitChar<'h> {
    haystack_len: usize,
    prev: usize,
    iter: memchr::Memchr<'h>
}

impl<'h> FastSplitChar<'h> {
    fn new(needle: char, haystack: &'h str) -> Self {
        assert!(needle.len_utf8() == 1);
        Self{
            haystack_len: haystack.len(),
            prev: 0, 
            iter: memchr::memchr_iter(needle as u8, haystack.as_bytes())
        }
    }
}

impl<'h> Iterator for FastSplitChar<'h> {
    type Item = std::ops::Range<usize>;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.prev >= self.haystack_len { return None; }
        let pos = self.iter.next().unwrap_or(self.haystack_len);
        let s = self.prev..pos;
        self.prev = pos + 1;
        Some(s)
    }
}


pub struct FastSplitStr<'h, 'n> {
    haystack_len: usize,
    needle_len: usize,
    prev: usize,
    iter: memchr::memmem::FindIter<'h, 'n>
}

impl<'h, 'n> FastSplitStr<'h, 'n> {
    fn new(needle: &'n str, haystack: &'h str) -> Self {
        Self{
            haystack_len: haystack.len(),
            needle_len: needle.len(), 
            prev: 0, 
            iter: memchr::memmem::find_iter(haystack.as_bytes(), needle.as_bytes())
        }
    }
}

impl<'h, 'n> Iterator for FastSplitStr<'h, 'n> {
    type Item = std::ops::Range<usize>;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.prev >= self.haystack_len { return None; }
        let pos = self.iter.next().unwrap_or(self.haystack_len);
        let s = self.prev..pos;
        self.prev = pos + self.needle_len;
        Some(s)
    }
}


//endregion

//region Parse Helpers

//region General

fn split_lines<'h>(haystack: &'h str) -> FastSplit<'h, 'static> {
    if let Some(end) = haystack.find('\n') {
        if haystack[..end].ends_with('\r') {
            return FastSplit::from_str("\r\n", haystack);
        }
    }
    FastSplit::from_char('\n', haystack)
}

pub fn str_to_integer(input: &str) -> Result<u64, std::num::ParseFloatError> {
    let mut chars = input.chars();
    let mut value = 0u64;
    while let Some(c) = chars.next() {
        match c {
            ',' => continue,
            '.' => break,
            _ => { value = value * 10 + ((c as u8) - b'0') as u64 }
        }
    }
    Ok(value)
}


pub fn str_to_float(input: &str) -> Result<Number, std::num::ParseFloatError> {
    let mut chars = input.chars();
    let mut value = 0usize;
    while let Some(c) = chars.next() {
        match c {
            ',' => continue,
            '.' => break,
            _ => { value = value * 10 + ((c as u8) - b'0') as usize }
        }
    }
    
    let decimal_tenth = (chars.next().unwrap_or('0') as u8) - b'0';
    let decimal_hundredth = (chars.next().unwrap_or('0') as u8) - b'0';
    let decimal = ((10 * decimal_tenth + decimal_hundredth) as Number) / 100.0;
    
    Ok(value as Number + decimal)
}


pub fn parse_seat_name(input: &str) -> Option<(Span, &str, usize)> {
    //     |
    //     v 
    // Seat 2: name ($1) 
    const BEFORE_SEAT: usize = "Seat ".len();
    //      -|
    //       v
    // Seat 2: name ($1) 
    let seat_has_two_digits = input[BEFORE_SEAT + 1..].chars().next().unwrap().is_numeric();
    let seat_sep = BEFORE_SEAT + 1 + seat_has_two_digits as usize;
    //              |---
    //              v
    // Seat 2: name ($1) 
    let end = input.rfind('(')?;
    //      _       
    // Seat 2: name ($1) 
    let seat = Span::range(BEFORE_SEAT, seat_sep);
    //         ____
    // Seat 2: name ($1) 
    let name = &input[seat_sep+2..end-1];
    //               ___
    // Seat 2: name ($1) 
    Some((seat, name, end + 1))
}

//endregion

//region Currency

const EURO: char = '\u{20ac}';
const INDIAN_RUPEE: char = '\u{20b9}';

pub fn parse_currency_char(input: &str) -> Option<(char, usize)> {
    for c in &['$', '£', '¥', EURO, INDIAN_RUPEE] {
        if input.starts_with(*c) {
            return Some((*c, c.len_utf8()));
        }
    }
    None
}

pub fn get_currency_iso(currency: char) -> &'static str {
    match currency {
        '$' => "USD", 
        '£' => "GBP", 
        '¥' => "JPY", 
        EURO => "EUR", 
        INDIAN_RUPEE => "INR",
        c => unreachable!("Invalid currency character: '{}'", c)
    }
}


impl Header {
    pub fn currency_iso(&self) -> &'static str { get_currency_iso(self.currency) }
}

//endregion

//region Cards

pub fn parse_cards(part: &str) -> Cards {
    let mut cards = Cards::default();
    for p in part.split(' ') {
        cards.push(Card::from(p));
    }
    cards
}


pub fn find_cards(part: &str) -> (Cards, (usize, usize)) {
    if let Some(begin) = part.find('[') {
        if let Some(end) = part[begin..].find(']') {
            return (parse_cards(&part[begin+1..begin+1+end]), (begin+1, begin+1+end));
        }
    }
    (Cards::default(), (0, 0))
}

//endregion

//region Action helpers

macro_rules! parse_action_lines {
    ($p:expr, $currency:expr, $f:expr, $($fn:expr),*) => {{
        if let Some(r) = $f($p, $currency) {
            Some(r)
        }
        $(
            else if let Some(r) = $fn($p, $currency) {
                Some(r)
            }
        )*
        else {
            None
        }
    }};

    ($p:expr, $currency:expr, $f:expr, $($fn:expr,)*) => {{
        parse_action_lines!($p, $currency, $f, $($fn),*)
    }};
}

macro_rules! parse_action_suffix_only {
    ($kind:expr, $ends_with:literal, $suffix:literal) => {
        parse_action_suffix_only!($kind, $ends_with, $suffix, ActionData::invalid())
    };

    ($kind:expr, $ends_with:literal, $suffix:literal, $data:expr) => {|p: &mut Parser, _: char| -> Option<Action> {
        if p.line.ends_with($ends_with) {
            Some(Action::new($kind, p.player_id(Self::trim_player_name(&p.line[..p.line.len()-$suffix.len()])), $data))
        } else {
            None
        }
    }};
}

//endregion

//endregion


/*
    pub trait ParseGenericAction: ParseCurrency {
        const ACTION_PREFIX: &'static str;

        fn is_all_in(line: &str) -> bool;

        fn parse_action_blind(p: &mut Parser, currency: char) -> Option<Action> {
            let (bet, (bet_begin, _)) = Self::rfind_currency(p.line, currency)?;
            let (blind, suffix) = if &p.line[bet_begin - 4..bet_begin - 2] == "ds" { 
                (Blind::Both, "posts small & big blinds ")
            } else { 
                let blind_end = &p.line[..bet_begin - 4].rfind(' ').unwrap() - 1;
                let c = p.line[blind_end..].chars().next().unwrap();
                match c {
                    'g' => (Blind::Big, "posts big blind"),
                    'l' => (Blind::Small, "posts small blind"),
                    // 'n' => (Blind::Small, "posts button blind"),
                    _ => unreachable!(),
                }
            };
            let name_end = bet_begin - suffix.len() - Self::ACTION_PREFIX.len();
            Some(p.action_extra(ActionType::Blind, &p.line[..name_end], bet, blind as u8))
        }

        fn parse_action_bet_call_raise(p: &mut Parser, currency: char) -> Option<Action> {
            let all_in = Self::is_all_in(p.line);
            let (amount, (amount_begin, amount_end)) = Self::find_currency(p.line, currency)?;
            let (t, suffix) = match p.line[amount_begin - 3..].chars().next().unwrap() {
                't' => (ActionType::Bet, "bets "),
                'l' => (ActionType::Call, "calls "),
                'e' => (ActionType::Raise, "raises "),
                _ => return None,
            };
            
            let name_end = amount_begin - suffix.len() - Self::ACTION_PREFIX.len();
            Some(p.action_all_in(t, &p.line[..name_end], amount, all_in))
        }    
    }

    impl ParseGenericAction for PokerStars {
        const ACTION_PREFIX: &'static str = ": ";
        fn is_all_in(line: &str) -> bool { line.ends_with("in") }
    }

    impl ParseGenericAction for OnGame {
        const ACTION_PREFIX: &'static str = " ";
        fn is_all_in(line: &str) -> bool { line.ends_with(']') }
    }
*/

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_parse_cards() {
        assert_eq!(cards!(As), parse_cards("As"));
        assert_eq!(cards!(As As), parse_cards("As As"));
        assert_eq!(cards!(As As), parse_cards("As, As"));
        assert_eq!(cards!(As Ad Ah Ac), parse_cards("As Ad Ah Ac"));
        assert_eq!(cards!(2s), parse_cards("2s"));
        assert_eq!(cards!(3s), parse_cards("3s"));
        assert_eq!(cards!(4s), parse_cards("4s"));
        assert_eq!(cards!(5s), parse_cards("5s"));
        assert_eq!(cards!(6s), parse_cards("6s"));
        assert_eq!(cards!(7s), parse_cards("7s"));
        assert_eq!(cards!(8s), parse_cards("8s"));
        assert_eq!(cards!(9s), parse_cards("9s"));
        assert_eq!(cards!(Ts), parse_cards("Ts"));
        assert_eq!(cards!(Js), parse_cards("Js"));
        assert_eq!(cards!(Qs), parse_cards("Qs"));
        assert_eq!(cards!(Ks), parse_cards("Ks"));
    }

    #[test]
    fn test_str_to_float() {
        assert_eq!(Ok(1.0), str_to_float("1"));
        assert_eq!(Ok(1.2), str_to_float("1.2"));
        assert_eq!(Ok(1.23), str_to_float("1.23"));
        assert_eq!(Ok(10.23), str_to_float("10.23"));
        assert_eq!(Ok(100.23), str_to_float("100.23"));
        assert_eq!(Ok(1000.23), str_to_float("1000.23"));
        assert_eq!(Ok(1000.23), str_to_float("1,000.23"));
    }

    
    // #[test]
    // fn test_parse_currency() {
    //     assert_eq!(Some((1.23, 5)), find_currency("$1.23", '$'));
    //     assert_eq!(Some((1000.23, 9)), find_currency_commas("$1,000.23", '$'));
    // }

    // #[test]
    // fn test_parse_action_generic1() {
        /*
        // Blind
        abcd posts small blind ($1)
        abcd: posts small blind ($1)
        
        // Call
        abcd calls $1
        abcd: calls $1

        // Bet
        abcd bets $1
        abcd: bets $1
        
        // Bet (All in)
        abcd: bets $1 and is all-in
        abcd bets $1 [all in]
        
        // Raise
        abcd raises to $1
        abcd raises $1 to $2
        abcd: raises $1 to $2

        // Raise (All in)
        abcd: raises $1 to $2 and is all in
        abcd raises to $1, and is all in
        */
        
    //     println!("{:?}", PokerStars::parse_action_bet_call_raise(&mut Parser::new("abcd: raises $1 to $2"), '$'));
    //     println!("{:?}", PokerStars::parse_action_bet_call_raise(&mut Parser::new("abcd: raises to $2 and is all in"), '$'));
    //     assert!(1==0);
    // }
}
