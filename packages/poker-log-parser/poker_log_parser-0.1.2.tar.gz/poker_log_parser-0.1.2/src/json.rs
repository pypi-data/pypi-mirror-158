use crate::pklp::*;

//region Json

use std::fmt::Write;
type JsonResult = std::fmt::Result;

pub fn to_json<'a, T: Json<JsonCompact<'a>>>(v: &T, r: &'a HandVec) -> Result<String, std::fmt::Error> {
    Ok({
        let mut f = JsonFormatter{out: String::with_capacity(100000)};
        v.serialize(&mut f, &mut JsonCompact{r, hand: 0})?;
        f.out
    })
}


pub fn to_json_ohh<'a, T: Json<JsonOHH<'a>>>(v: &T, r: &'a HandVec) -> Result<String, std::fmt::Error> {
    let mut f = JsonFormatter{out: String::with_capacity(100000)};
    v.serialize(&mut f, &mut JsonOHH{r})?;
    Ok(f.out)
}

pub trait Json<E> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult;
}

pub struct JsonFormatter {
    out: String,
}

pub struct JsonArrayFormatter<'a> {
    f: &'a mut JsonFormatter,
    is_first: bool,
}

pub struct JsonObjectFormatter<'a> {
    f: &'a mut JsonFormatter,
    is_first: bool,
}

impl JsonFormatter {
    fn array<'a>(&'a mut self) -> JsonArrayFormatter<'a> {
        self.write_char('[').unwrap();
        JsonArrayFormatter { f: self, is_first: true }
    }

    fn object<'a>(&'a mut self) -> JsonObjectFormatter<'a> {
        self.write_char('{').unwrap();
        JsonObjectFormatter { f: self, is_first: true }
    }
}

impl<'a> JsonArrayFormatter<'a> {
    fn entry<E, T: Json<E>>(&mut self, value: T, extra: &mut E) -> &mut Self {
        if !self.is_first { write!(self.f, ",").unwrap(); }
        self.is_first = false;
        value.serialize(self.f, extra).unwrap();
        self
    }

    
    fn entries<E, T: Json<E>>(&mut self, values: &[T], extra: &mut E) -> &mut Self {
        for v in values { self.entry(v, extra); }
        self
    }

    fn finish(&mut self) -> JsonResult {
        write!(self.f, "]")
    }
}

impl<'a> JsonObjectFormatter<'a> {
    fn entry<E, T: Json<E>>(&mut self, name: &str, value: T, extra: &mut E) -> &mut Self {
        if !self.is_first { self.f.write_char(',').unwrap() ;}
        self.is_first = false;
        write!(self.f, "\"{}\"", name).unwrap();
        self.f.write_char(':').unwrap();
        value.serialize(self.f, extra).unwrap();
        self
    }
    
    fn entry_if<E, T: Json<E>>(&mut self, cond: bool, name: &str, value: T, extra: &mut E) -> &mut Self {
        if cond { self.entry(name, value, extra); }
        self
    }

    fn entry_opt<E, T: Json<E>>(&mut self, name: &str, values: &[T], extra: &mut E) -> &mut Self {
        self.entry_if(!values.is_empty(), name, values, extra)
    }

    fn finish(&mut self) -> JsonResult {
        self.f.write_char('}')
    }
}

impl std::fmt::Write for JsonFormatter {
    fn write_char(&mut self, c: char) -> std::fmt::Result {
        self.out.push(c);
        Ok(())
    }

    fn write_str(&mut self, s: &str) -> std::fmt::Result {
        self.out.push_str(s);
        Ok(())
    }
}

impl<E> Json<E> for bool {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.write_str(if *self { "true" } else { "false" })
    }
}

impl<E> Json<E> for char {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.write_char('"')?;
        f.write_char(*self)?;
        f.write_char('"')
    }
}

impl<E> Json<E> for u8 {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "{}", self)
    }
}

impl<E> Json<E> for u64 {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "{}", self)
    }
}

impl<E> Json<E> for Number {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "{}", self)
    }
}

impl<E> Json<E> for str {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "\"{}\"", self)
    }
}

impl<E> Json<E> for &str {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "\"{}\"", self)
    }
}

impl<E, T: Json<E>> Json<E> for &T {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        (*self).serialize(f, extra)
    }
}

impl<E, T: Json<E>> Json<E> for Option<T> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        match self {
            Some(v) => v.serialize(f, extra),
            None => write!(f, "null"),
        }
    }
}

impl<E, T: Json<E>> Json<E> for [T] {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.array().entries(self, extra).finish()
    }
}

impl<E, T: Json<E>> Json<E> for &[T] {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.array().entries(*self, extra).finish()
    }
}

impl<E, T: Json<E>, const N: usize> Json<E> for [T; N] {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        self.as_slice().serialize(f, extra)
    }
}

impl<E, T: Json<E>> Json<E> for Vec<T> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        self.as_slice().serialize(f, extra)
    }
}

//endregion

//region JSON Extra

pub struct JsonCompact<'a> {
    r: &'a HandVec,
    hand: usize,
}

pub struct JsonOHH<'a> {
    r: &'a HandVec,
}

impl JsonOHH<'_> {
    const SPEC_VERSION: &'static str = "1.4.1";
}


impl<E> Json<E> for Cards {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.array()
            .entries(&self.values[0..self.size as usize], extra)
            .finish()
    }
}


impl<E> Json<E> for Card {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        f.write_char('"')?;
        f.write_char(Card::num_to_char(self.n()))?;
        f.write_char(self.suit().char())?;
        f.write_char('"')
    }
}


impl<E> Json<E> for DateTime {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        write!(f, "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}Z",
            self.year(), self.month(), self.day(), self.hour(), self.min(), self.sec())
    }
}


impl<E> Json<E> for PokerSite {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        use PokerSite::*;
        f.write_str(match self {
            PokerStars          => "PokerStars",
            PokerStarsPluribus  => "PokerStarsPluribus",
            OnGame              => "OnGame",
            Absolute            => "Absolute",
            EverLeaf            => "EverLeaf",
            BetOnline           => "BetOnline",
            FullTiltPoker       => "FullTiltPoker",
            PacificPoker        => "PacificPoker",
            PokerTracker        => "PokerTracker",
            PartyPoker          => "PartyPoker",
            GGPoker             => "GGPoker",
            Winamax             => "Winamax",
            KingsClub           => "KingsClub",
            Bovada              => "Bovada",
            Enet                => "Enet",
            Cake                => "Cake",
            Pkr                 => "Pkr",
            Winning             => "Winning",
        })
    }
}


impl<E> Json<E> for GameType {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut E) -> JsonResult {
        use GameType::*;
        f.write_str(match self {
            HoldEm              => "HoldEm",
            Omaha               => "Omaha",
            OmahaHiLo           => "OmahaHiLo",
        })
    }
}

//endregion

//region JsonCompact

impl Json<JsonCompact<'_>> for HandSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.write_char('[')?;
        let mut comma = false;
        for h in &extra.r[*self] {
            if comma { f.write_char(',')?; }
            comma = true;
            h.serialize(f, extra);
            extra.hand += 1;
        }
        f.write_char(']')
    }
}

impl Json<JsonCompact<'_>> for HandVec {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        HandSpan::new(0, self.hands.len()).serialize(f, extra)
    }
}


impl Json<JsonCompact<'_>> for Hand {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("header", &self.header, extra)
            .entry("preflop", &self.preflop, extra)
            .entry("flops", &self.flops(), extra)
            .entry("turns", &self.turns(), extra)
            .entry("rivers", &self.rivers(), extra)
            .entry("showdowns", &self.showdowns(), extra)
            .entry("summary", &self.summary, extra)
            .finish()
    }
}


impl Json<JsonCompact<'_>> for Header {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("site", &self.site, extra)
            .entry("game_type", &self.game_type, extra)
            .entry("bet_type", &self.bet_type, extra)
            .entry("id", &self.id, extra)
            .entry("table_name", &self.table_name, extra)
            .entry("start_date", &self.start_date, extra)
            .entry("currency", self.currency, extra)
            .entry("is_tournament", &self.is_tournament, extra)
            .entry("max_players", &self.max_players, extra)
            .entry("dealer_id", &self.dealer, extra)
            .entry("hero_id", &self.hero, extra)
            .entry("bet_cap", &self.bet_cap, extra)
            .entry("ante", &self.ante, extra)
            .entry("small_blind", &self.small_blind, extra)
            .entry("big_blind", &self.big_blind, extra)
            .entry("players", &self.players, extra)
            .entry("actions", &self.actions, extra)
            .finish()
    }
}


impl Json<JsonCompact<'_>> for FlopSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for TurnSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for RiverSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for ShowdownSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for Street {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("id", &self.id, extra)
            .entry_opt("cards", self.cards.values(), extra)
            .entry("actions", &self.actions, extra)
            .finish()
    }
}


impl Json<JsonCompact<'_>> for Summary {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("total_pot", &self.pot.total, extra)
            .entry("main_pot", &self.pot.main, extra)
            .entry("side_pots", &self.pot.side, extra)
            .entry("rake", &self.pot.rake, extra)
            .entry("winners", &self.winners, extra)
            .entry("actions", &self.actions, extra)
            .finish()
    }
}


impl Json<JsonCompact<'_>> for WinnerSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for Winner {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("player_id", &self.player_id, extra)
            .entry("game_id", &self.game_id, extra)
            .entry("amount", &self.amount, extra)
            .finish()
    }
}


struct JsonPlayer<'a> {
    player: &'a Player,
    id: u8,
}
impl Json<JsonCompact<'_>> for PlayerSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        let players = &extra.r[*self];
        let mut l = f.array();
        for (i, p) in players.iter().enumerate() {
            l.entry(&JsonPlayer{player: p, id: i as u8}, extra);
        }
        l.finish()
    }
}
impl Json<JsonCompact<'_>> for JsonPlayer<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.object()
            .entry("name", &self.player.name, extra)
            .entry("id", &self.id, extra)
            .entry("seat", &self.player.seat, extra)
            .entry("chips", &self.player.chips, extra)
            .finish()
    }
}


impl Json<JsonCompact<'_>> for ActionSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}
impl Json<JsonCompact<'_>> for Action {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        let cards = if self.kind.can_have_cards() { self.data.cards(extra.r) } else { Cards::default() };
        let msg = if self.kind == ActionType::Say { self.data.message(extra.hand, extra.r) } else { "" };
        let (cashout_amount, cashout_fee) = if self.kind == ActionType::CashOut { self.data.pair(extra.r) } else { (0.0, 0.0) };

        let mut o = f.object();
        o.entry("player_id", &self.player_id, extra);
        o.entry("type", &self.kind, extra);
        o.entry_opt("cards", cards.values(), extra);
        if self.kind.can_have_num() {
            o.entry("amount", self.data.num(), extra);
        }
        if self.kind.can_have_all_in() {
            o.entry("all_in", self.kind.is_all_in(), extra);
        }
        if self.kind.can_have_blind() {
            o.entry("blind", Blind::from(self.kind), extra);
        }
        if self.kind.can_have_pot() {
            o.entry("pot", Pot::from(self.kind), extra);
        }
        if !msg.is_empty() {
            o.entry("msg", msg, extra);
        }
        if self.kind == ActionType::Join {
            o.entry("seat", self.data.handle() as u8, extra);
        }
        if self.kind == ActionType::CashOut {
            o.entry("amount", cashout_amount, extra);
            o.entry("fee", cashout_fee, extra);
        }
        o.finish()
    }
}
impl Json<JsonCompact<'_>> for ActionType {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.write_str(match self {
            Self::Bet |
            Self::BetAllIn              => "bet",
            Self::Call |
            Self::CallAllIn             => "call",
            Self::Raise |
            Self::RaiseAllIn            => "raise",
            Self::Check                 => "check",
            Self::Fold                  => "fold",
            Self::Muck                  => "muck",
            Self::Show                  => "show",
            Self::Dealt                 => "dealt",
            Self::Ante |
            Self::BigBlind |
            Self::SmallBlind |
            Self::BigSmallBlind |
            Self::DeadBlind |
            Self::ExtraBlind            => "blind",
            Self::CashOut               => "cashout",
            Self::CollectMainPot |
            Self::CollectSidePot1 |
            Self::CollectSidePot2 |
            Self::CollectSidePot3       => "collect_pot",
            Self::UncalledBetReturned   => "uncalled_bet",
            Self::Join                  => "join",
            Self::Leave                 => "leave",
            Self::Sitout                => "sitout",
            Self::Say                   => "say",
        })
    }
}
impl Json<JsonCompact<'_>> for Blind {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.write_str(match self {
            Self::Ante  => "ante",
            Self::Big   => "big",
            Self::Small => "small",
            Self::Both  => "big_small",
            Self::Dead  => "dead",
            Self::Extra => "extra",
        })
    }
}
impl Json<JsonCompact<'_>> for Pot {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        f.write_str(match self {
            Self::Main  => "main",
            Self::Side1 => "side_1",
            Self::Side2 => "side_2",
            Self::Side3 => "side_3",
        })
    }
}


impl Json<JsonCompact<'_>> for BetType {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        use BetType::*;
        f.write_str(match self {
            NoLimit             => "NoLimit",
            Limit               => "Limit",
            PotLimit            => "PotLimit",
        })
    }
}


impl Json<JsonCompact<'_>> for Span {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonCompact<'_>) -> JsonResult {
        extra.r.src[*self].serialize(f, extra)
    }
}

//endregion

//region JsonOHH

impl Json<JsonOHH<'_>> for HandVec {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        self.hands.serialize(f, extra)
    }
}

impl Json<JsonOHH<'_>> for HandSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        extra.r[*self].serialize(f, extra)
    }
}

impl Json<JsonOHH<'_>> for Hand {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let dealer_seat = self.header.dealer(extra.r).seat;
        f.object()
            // "internal_version"
            // "table_handle"
            // "table_skin"
            // "tournament_info"
            // "tournament_rebuys"
            // "tournament_bounties"
            .entry("spec_version", JsonOHH::SPEC_VERSION, extra)
            .entry("site_name", &self.header.site, extra)
            .entry("network_name", &self.header.site, extra)
            .entry("game_type", &self.header.game_type, extra)
            .entry("table_name", &self.header.table_name, extra)
            .entry("game_number", &self.header.id, extra)
            .entry("start_date_utc", &self.header.start_date, extra)
            .entry("tournament", &self.header.is_tournament, extra)
            .entry("table_size", &self.header.max_players, extra)
            .entry("currency", &self.header.currency_iso(), extra)
            .entry("dealer_seat", &dealer_seat, extra)
            .entry("hero_player_id", None as Option<u8>, extra)
            .entry("small_blind", &self.header.small_blind, extra)
            .entry("big_blind", &self.header.big_blind, extra)
            .entry("ante_amount", &self.header.ante, extra)
            .entry("bet_limit", &JsonOHHBetLimit{cap: self.header.bet_cap, bet_type: self.header.bet_type}, extra)
            .entry("players", &self.header.players, extra)
            .entry("flags", &JsonOHHFlags{hand: self}, extra)
            .entry("rounds", &JsonOHHRounds{header_actions: self.header.actions, preflop: &self.preflop, streets: self.streets}, extra)
            .entry("pots", &JsonOHHPots{pots: self.summary.pot, winners: self.summary.winners}, extra)
            .finish()
    }
}


struct JsonOHHFlags<'a> {
    hand: &'a Hand
}

impl Json<JsonOHH<'_>> for JsonOHHFlags<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let mut l = f.array();
        
        if self.hand.flops().size() > 1 
            || self.hand.turns().size() > 1 
            || self.hand.rivers().size() > 1 
            || self.hand.showdowns().size() > 1 
        {
            l.entry("Run_It_Twice", extra);
        }

        if false { // obfuscated
            l.entry("Anonymous", extra);
        }

        if self.hand.header.hero == SEAT_NONE {
            l.entry("Observed", extra);
        }

        if false { // fast game
            l.entry("Fast", extra);
        }

        if self.hand.header.bet_cap > 0.0 {
            l.entry("Cap", extra);
        }

        l.finish()
    }
}


struct JsonOHHBetLimit {
    cap: Number,
    bet_type: BetType,
}

impl Json<JsonOHH<'_>> for JsonOHHBetLimit {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.object()
            .entry("bet_type", &self.bet_type, extra)
            .entry("cap", &self.cap, extra)
            .finish()
    }
}


impl Json<JsonOHH<'_>> for PlayerSpan {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let players = &extra.r[*self];
        let mut l = f.array();
        for (i, p) in players.iter().enumerate() {
            l.entry(&JsonPlayer{player: p, id: i as u8}, extra);
        }
        l.finish()
    }
}
impl Json<JsonOHH<'_>> for JsonPlayer<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.object()
            .entry("id", &self.id, extra)
            .entry("seat", &self.player.seat, extra)
            .entry("name", &self.player.name, extra)
            .entry("starting_stack", &self.player.chips, extra)
            .entry("player_bounty", &0.0, extra)
            .finish()
    }
}


struct JsonOHHRounds<'a> {
    header_actions: ActionSpan,
    preflop: &'a Street,
    streets: StreetArray,
}

impl Json<JsonOHH<'_>> for JsonOHHRounds<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let flops = &extra.r[self.streets.0];
        let turns = &extra.r[self.streets.1];
        let rivers = &extra.r[self.streets.2];
        let showdowns = &extra.r[self.streets.3];
        let mut l = f.array();
        l.entry(&JsonOHHPreflop{header_actions: self.header_actions, preflop: self.preflop}, extra);
        for s in flops { l.entry(&JsonOHHStreet{kind: StreetType::Flop, street: s}, extra); }
        for s in turns { l.entry(&JsonOHHStreet{kind: StreetType::River, street: s}, extra); }
        for s in rivers { l.entry(&JsonOHHStreet{kind: StreetType::Turn, street: s}, extra); }
        for s in showdowns { l.entry(&JsonOHHStreet{kind: StreetType::Showdown, street: s}, extra); }
        l.finish()
    }
}

struct JsonOHHPreflop<'a> {
    header_actions: ActionSpan,
    preflop: &'a Street,
}

struct JsonOHHStreet<'a> {
    kind: StreetType,
    street: &'a Street,
}

// TODO: JsonOHH - update previous actions with new data from summary
// TODO: JsonOHH - get cashout action for specific player win

impl Json<JsonOHH<'_>> for JsonOHHPreflop<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let actions = ActionSpan::new(self.header_actions.begin(), self.header_actions.size() + self.preflop.actions.size());
        f.object()
            .entry("street", "Preflop", extra)
            .entry("id", &0u8, extra)
            .entry("actions", &actions, extra)
            .finish()
    }
}

impl Json<JsonOHH<'_>> for JsonOHHStreet<'_> {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.object()
            .entry("street", &self.kind, extra)
            .entry("id", &(self.street.id + 1), extra)
            .entry_opt("cards", self.street.cards.values(), extra)
            .entry("actions", &self.street.actions, extra)
            .finish()
    }
}

impl Json<JsonOHH<'_>> for StreetType {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.write_str(match self {
            Self::Flop                  => "Flop",
            Self::Turn                  => "Turn",
            Self::River                 => "River",
            Self::Showdown              => "Showdown",
        })
    }
}

struct JsonOHHPots {
    pots: PotInfo,
    winners: WinnerSpan,
}

struct JsonOHHPot {
    pots: PotInfo,
    winners: WinnerSpan,
    pot_index: u8,
}

struct JsonOHHPlayerWins {
    pots: PotInfo,
    winners: WinnerSpan,
    pot_index: u8,
}

struct JsonOHHPlayerWin {
    pots: PotInfo,
    winner: Winner,
    pot_index: u8,
}

impl Json<JsonOHH<'_>> for JsonOHHPots {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let mut l = f.array();
        l.finish()
    }
}

impl Json<JsonOHH<'_>> for JsonOHHPot {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let amount = match self.pot_index {
            0 => self.pots.main,
            i => self.pots.side[i as usize - 1],
        };
        let rake = match self.pot_index {
            0 => self.pots.rake,
            _ => 0.0,
        };
        f.object()
            .entry("number", &self.pot_index, extra)
            .entry("amount", amount, extra)
            .entry("rake", &rake, extra)
            .entry("jackpot", &0.0, extra)
            .finish()
    }
}

impl Json<JsonOHH<'_>> for JsonOHHPlayerWins {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let mut l = f.array();
        unimplemented!("JsonOHH - player wins");
        l.finish()
    }
}

impl Json<JsonOHH<'_>> for JsonOHHPlayerWin {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.object()
            .entry("player_id", &self.winner.player_id, extra)
            .entry("win_amount", &self.winner.amount, extra)
            .entry("cashout_amount", &0.0, extra)
            .entry("cashout_fee", &0.0, extra)
            .entry("bonus_amount", &0.0, extra)
            .entry("contributed_rake", &0.0, extra)
            .finish()
    }
}


impl Json<JsonOHH<'_>> for ActionSpan {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        let actions = &extra.r[*self];
        let mut l = f.array();
        for a in actions {
            match a.kind {
                _ => l.entry(a, extra),
            };
        }
        l.finish()
    }
}

impl Json<JsonOHH<'_>> for Action {    
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        unimplemented!("JsonOHH - action")
    }
}


impl Json<JsonOHH<'_>> for BetType {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        f.write_str(match self {
            Self::NoLimit               => "NL",
            Self::Limit                 => "FL",
            Self::PotLimit              => "PL",
        })
    }
}


impl Json<JsonOHH<'_>> for Span {
    fn serialize(&self, f: &mut JsonFormatter, extra: &mut JsonOHH<'_>) -> JsonResult {
        extra.r.src[*self].serialize(f, extra)
    }
}

//endregion

//region OpenHandHistory Format

/* 
<hand> {"ohh":
  {
		"spec_version": version_string,
		"site_name": string,
		"network_name": string,
		"internal_version": version_string,
		"tournament": boolean
		"tournament_info": <tournament_info_obj>,
		"game_number": string,
		"start_date_utc": string,
		"table_name": string,
		"table_handle": string,
		"table_skin": string,
		"game_type": string,
		"bet_limit": <bet_limit_obj>,
		"table_size": integer,
		"currency": string,
		"dealer_seat": integer,
		"small_blind": decimal,
		"big_blind": decimal,
		"ante_amount": decimal,
		"hero_player_id": integer,
		"flags": [
			string,
			string
		],
		"players": [
			<player_obj>,
			<player_obj>
		],
		"rounds": [
			<round_obj>,
			<round_obj>
		],
		"pots": [
			<pot_obj>,
			<pot_obj>
		],
		"tournament_rebuys": [	
			<tournament_rebuy_obj>,
			<tournament_rebuy_obj>
		],
		"tournament_bounties": [
			<tournament_bounty_obj>,
			<tournament_bounty_obj>
		]
	}
}

<bet_limit_obj> {
    "bet_type": string,
    "bet_cap": decimal
}

<player_obj> {
	"id": integer,
	"seat": integer,
	"name": string,
	"display": string,
	"starting_stack": decimal,
	"player_bounty": decimal
}

<round_obj> {
	"id": integer,
	"street": street_string
	"cards": [
		string,
		string,
		string
	],
	"actions": [
		<action_obj>,
		<action_obj>
	]
}

<action_obj> {
	"action_number": integer,
	"player_id": integer,
	"action": string,
	"amount": decimal,
	"is_allin": boolean,
	"cards": [
		card string,
		card string
	]
}

<pot_obj> {
	"number": integer,
	"amount": decimal,
	"rake": decimal,
	"jackpot": decimal,
	"player_wins": [
		<player_win_obj>,
		<player_win_obj>
	]
}

<player_win_obj> {
	"player_id": int,
	"win_amount": decimal,
	"cashout_amount": decimal,
	"cashout_fee": decimal,
	"bonus_amount": decimal,
	"contributed_rake": decimal
}

<tournament_info_obj> {
  "tournament_number": string,
  "name": string,  
  "start_date_utc": string,
  "currency": string,
  "buyin_amount": decimal,
  "fee_amount": decimal,
  "bounty_fee_amount": decimal,
  "initial_stack": integer,
  "type": string,
  "flags": array,
  "speed": object
}

<tournament_rebuy_obj> {
	"player_id": int,
	"rebuy_action": string,
	"amount": decimal,
	"chips": int
}

<tournament_bounty_obj> {
	"player_id": int,
	"bounty_won": decimal,
	"defeated_player_id": int
}

<speed_obj> {
	"type": string,		
	"round_time": integer
}

*/

//endregion

//region Tests

mod tests {
    use super::*;

    #[test]
    fn json_cards() {
        assert_eq!(Ok("[\"Qc\"]".into()), 
            to_json(&cards!(Qc), &HandVec::default()));

        assert_eq!(Ok("[\"As\",\"Ad\",\"Ac\",\"Ah\"]".into()), 
            to_json(&cards!(As Ad Ac Ah), &HandVec::default()));
    }

    #[test]
    fn json_players() {
        let mut h = HandVec::default();
        h.src = "abcd".into();
        h.players.push(Player{name: Span::new(0, 4), seat: 1, chips: 1.23});

        assert_eq!(Ok("[{\"name\":\"abcd\",\"id\":0,\"seat\":1,\"chips\":1.23}]".into()), 
            to_json(&PlayerSpan::new(0, 1), &h));
    }
}

//endregion
