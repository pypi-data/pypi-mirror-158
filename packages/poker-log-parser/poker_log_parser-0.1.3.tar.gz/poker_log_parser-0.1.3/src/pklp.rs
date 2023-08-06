//region Structs

pub const SEAT_NONE: u8 = u8::MAX;
pub const SEAT_AFTER_DEALER: u8 = u8::MAX - 1;
pub const SEAT_INITIAL: u8 = u8::MAX - 2;

pub type Number         = f32;
pub type StreetArray    = (FlopSpan, TurnSpan, RiverSpan, ShowdownSpan);


#[derive(Debug, Clone, Copy)]
pub enum Pot { Main, Side1, Side2, Side3 }


#[derive(Debug, Clone, Copy)]
pub enum Blind { Ante, Small, Big, Both, Dead, Extra }


#[derive(Debug, Clone, Copy)]
pub enum Suit { Spade, Club, Heart, Diamond }


#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum StreetType { Flop, Turn, River, Showdown }


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BetType { NoLimit, Limit, PotLimit }


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ActionType {
    Bet,
    Call,
    Raise,
    BetAllIn,
    CallAllIn,
    RaiseAllIn,

    Check,
    Fold,
    Muck,
    Show,
    Dealt,

    Ante,
    BigBlind,
    SmallBlind,
    BigSmallBlind,
    DeadBlind,
    ExtraBlind,

    CashOut,
    CollectMainPot,
    CollectSidePot1,
    CollectSidePot2,
    CollectSidePot3,
    UncalledBetReturned,
    
    Join,
    Leave,
    Sitout,
    Say,
}


#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum GameType {
    HoldEm,
    Omaha,
    OmahaHiLo,
}


#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum PokerSite {
    PokerStars,
    PokerStarsPluribus, // Subset of PokerStars format generated from Pluribus AI match logs
    OnGame,
    
    Absolute,
    EverLeaf,
    BetOnline,
    FullTiltPoker,
    PacificPoker, // Now 888Poker
    PokerTracker,
    PartyPoker,
    GGPoker,
    Winamax,
    KingsClub,
    Bovada,
    Enet,
    Cake,
    Pkr,
    Winning,
    
    // TODO: XML formats?
    // Boss
    // IPoker
    // Merge
    // Microgaming
}


#[derive(Debug, Clone, PartialEq)]
pub struct HandVec {
    pub src: String,
    pub hands: Vec<Hand>,
    pub players: Vec<Player>,
    pub flops: Vec<Street>,
    pub turns: Vec<Street>,
    pub rivers: Vec<Street>,
    pub showdowns: Vec<Street>,
    pub actions: Vec<Action>,
    pub nums: Vec<Number>,
    pub cards: Vec<Cards>,
    pub winners: Vec<Winner>,
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct Hand {
    pub header: Header,
    pub preflop: Street,
    pub summary: Summary,
    pub streets: StreetArray,
    pub src_offset: usize,
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct Header {
    pub players: PlayerSpan,
    pub max_players: u8, 
    pub site: PokerSite,
    pub game_type: GameType,
    pub dealer: u8,
    pub hero: u8,
    pub currency: char,
    pub ante: Number,
    pub small_blind: Number,
    pub big_blind: Number,
    pub bet_type: BetType,
    pub bet_cap: Number,
    pub id: Span,
    pub table_name: Span, 
    pub actions: ActionSpan,
    pub start_date: DateTime,
    pub is_tournament: bool,
    // "tournament_info": <tournament_info_obj>,
}


#[derive(Default, Debug, Clone, Copy, PartialEq, Eq)]
pub struct Street {
    pub cards: Cards,
    pub id: u8,
    pub actions: ActionSpan,
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct PotInfo {
    pub total: Number,
    pub rake: Number,
    pub main: Number,
    pub side: [Number; 3],
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct Summary {
    pub pot: PotInfo,
    pub winners: WinnerSpan,
    pub actions: ActionSpan,
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct Player {
    pub name: Span,
    pub chips: Number,
    pub seat: u8,
}


#[derive(Default, Debug, Clone, Copy, PartialEq)]
pub struct Winner {
    pub amount: Number,
    pub player_id: u8,
    pub game_id: u8,
}


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ActionData(u32);


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Action {
    pub data: ActionData,
    pub player_id: u8,
    pub kind: ActionType,
}


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Card(pub u8);


#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub struct Cards {
    pub values: [Card; 5],
    pub size: u8,
}


//endregion

//region Hand

impl std::default::Default for PokerSite {
    fn default() -> Self { Self::PokerStars }
}

impl std::default::Default for GameType {
    fn default() -> Self { Self::HoldEm }
}

impl std::default::Default for BetType {
    fn default() -> Self { Self::NoLimit }
}

impl HandVec {
    pub fn new() -> Self {
        Self { 
            src: String::with_capacity(131072),
            hands: Vec::with_capacity(1024), 
            players: Vec::with_capacity(4096), 
            flops: Vec::with_capacity(512), 
            turns: Vec::with_capacity(256), 
            rivers: Vec::with_capacity(256), 
            showdowns: Vec::with_capacity(16), 
            actions: Vec::with_capacity(8192), 
            nums: Vec::with_capacity(256), 
            cards: Vec::with_capacity(512),
            winners: Vec::with_capacity(1024),
        }
    }

    pub fn size_bytes(&self) -> usize {
        self.src.len()
        + (self.hands.len() * std::mem::size_of::<Hand>())
        + (self.players.len() * std::mem::size_of::<Player>())
        + (self.flops.len() * std::mem::size_of::<Street>())
        + (self.turns.len() * std::mem::size_of::<Street>())
        + (self.rivers.len() * std::mem::size_of::<Street>())
        + (self.showdowns.len() * std::mem::size_of::<Street>())
        + (self.actions.len() * std::mem::size_of::<Action>())
        + (self.nums.len() * std::mem::size_of::<Number>())
        + (self.cards.len() * std::mem::size_of::<Cards>())
        + (self.winners.len() * std::mem::size_of::<Winner>())
    }

        
    pub fn push_str(&mut self, v: &str) -> Span {
        let begin = self.src.len();
        self.src.push_str(v);
        Span::range(begin, self.src.len())
    }
}

impl Hand {
    pub fn flops(&self) -> FlopSpan { self.streets.0 }
    pub fn turns(&self) -> TurnSpan { self.streets.1 }
    pub fn rivers(&self) -> RiverSpan { self.streets.2 }
    pub fn showdowns(&self) -> ShowdownSpan { self.streets.3 }

    pub fn street<'a>(&self, index: StreetType, h: &'a HandVec) -> &'a [Street] {
        match index {
            StreetType::Flop => &h[self.streets.0],
            StreetType::Turn => &h[self.streets.1],
            StreetType::River => &h[self.streets.2],
            StreetType::Showdown => &h[self.streets.3],
        }
    }
}

impl Header {
    pub fn dealer<'a>(&self, h: &'a HandVec) -> &'a Player {
        &h[self.players][self.dealer as usize]
    }

    pub fn player<'a>(&self, id: u8, h: &'a HandVec) -> &'a Player {
        &h[self.players][id as usize]
    }
}

impl std::default::Default for HandVec {
    fn default() -> Self { 
        Self::new()
        // Self{src: String::new(), hands: Vec::new(), players: Vec::new(), flops: Vec::new(), turns: Vec::new(), rivers: Vec::new(), showdowns: Vec::new(), actions: Vec::new(), nums: Vec::new(), cards: Vec::new(), winners: Vec::new()}
    }
}

impl std::ops::Index<StreetType> for HandVec {
    type Output = Vec<Street>;
    fn index(&self, index: StreetType) -> &Self::Output {
        match index {
            StreetType::Flop => &self.flops,
            StreetType::Turn => &self.turns,
            StreetType::River => &self.rivers,
            StreetType::Showdown => &self.showdowns,
        }
    }
}

impl std::ops::IndexMut<StreetType> for HandVec {
    fn index_mut(&mut self, index: StreetType) -> &mut Self::Output {
        match index {
            StreetType::Flop => &mut self.flops,
            StreetType::Turn => &mut self.turns,
            StreetType::River => &mut self.rivers,
            StreetType::Showdown => &mut self.showdowns,
        }
    }
}

// make cards object from identifiers
macro_rules! cards {
    ($($card:tt) *) => {{
        let mut c = crate::pklp::Cards::default();
        $(
            c.push(crate::pklp::Card::from(stringify!($card)));
        )*
        c   
    }};
}

//endregion

//region Summary

impl std::convert::From<u8> for Pot {
    fn from(v: u8) -> Self {
        match v {
            0 => Self::Main,
            1 => Self::Side1,
            2 => Self::Side2,
            3 => Self::Side3,
            _ => unreachable!(),
        }
    }
}

impl std::convert::From<u8> for Blind {
    fn from(v: u8) -> Self {
        match v {
            0 => Self::Small,
            1 => Self::Big,
            2 => Self::Both,
            3 => Self::Dead,
            4 => Self::Extra,
            _ => unreachable!(),
        }
    }
}

impl std::convert::From<ActionType> for Blind {
    fn from(v: ActionType) -> Self {
        match v {
            ActionType::Ante => Blind::Ante,
            ActionType::SmallBlind => Blind::Small,
            ActionType::BigBlind => Blind::Big,
            ActionType::BigSmallBlind => Blind::Both,
            ActionType::DeadBlind => Blind::Dead,
            ActionType::ExtraBlind => Blind::Extra,
            _ => unreachable!(),
        } 
    }
}

impl std::convert::From<ActionType> for Pot {
    fn from(v: ActionType) -> Self {
        match v {
            ActionType::CollectMainPot => Pot::Main,
            ActionType::CollectSidePot1 => Pot::Side1,
            ActionType::CollectSidePot2 => Pot::Side2,
            ActionType::CollectSidePot3 => Pot::Side3,
            _ => unreachable!(),
        }
    }
}

//endregion

//region Card

impl Card {
    pub fn new(n: u8, suit: Suit)   -> Self { Self(n | (suit as u8) << 6) }
    pub fn n(self)                  -> u8   { self.0 & 0b00111111 }
    pub fn suit(self)               -> Suit { Suit::from(self.0 >> 6) }
    pub fn num_to_char(n: u8)       -> char {
        match n {
            1 => 'A',
            10 => 'T',
            11 => 'J',
            12 => 'Q',
            13 => 'K',
            _ => (b'0' + n) as char
        }
    }
}

impl Cards {
    pub fn push(&mut self, card: Card) {
        self.values[self.size as usize] = card;
        self.size += 1;
    }

    pub fn values(&self) -> &[Card] {  
        &self.values[..self.size as usize]
    }
}

impl std::default::Default for Cards {
    fn default() -> Self { Self{values: [Card::new(1, Suit::Spade); 5], size: 0} }
}

impl std::ops::Index<usize> for Cards {
    type Output = Card;
    fn index(&self, index: usize) -> &Self::Output {
        &self.values[index]
    }
}

impl std::convert::From<u8> for Suit {
    fn from(v: u8) -> Self {
        match v {
            0 => Suit::Spade,
            1 => Suit::Club,
            2 => Suit::Heart,
            3 => Suit::Diamond,
            _ => unreachable!(),
        }
    }
}

impl std::convert::From<&str> for Card {
    fn from(p: &str) -> Self {
        let mut chars = p.chars();
        let (nc, mut sc) = (chars.next().unwrap(), chars.next().unwrap());
        let n = match nc {
            'A' => 1,
            'T' => 10,
            'J' => 11,
            'Q' => 12,
            'K' => 13,
            // 10c
            '1' => { sc = chars.next().unwrap(); 10 }
            x => x as u8 - b'0'
        };
        let suit = match sc.to_lowercase().next().unwrap() {
            's' => Suit::Spade,
            'h' => Suit::Heart,
            'd' => Suit::Diamond,
            'c' => Suit::Club,
            s => unreachable!("Invalid suit: {} in '{}'", s, p),
        };
        Card::new(n, suit)
    }
}

impl Suit {
    pub fn char(self) -> char {
        match self {
            Suit::Spade => 's',
            Suit::Club => 'c',
            Suit::Heart => 'h',
            Suit::Diamond => 'd',
        }
    }
    

    pub fn from_char(c: char) -> Self {
        match c {
            's' => Suit::Spade,
            'c' => Suit::Club,
            'h' => Suit::Heart,
            'd' => Suit::Diamond,
            _ => unreachable!(),
        }
    }


    pub fn unicode(self) -> char {
        match self {
            Suit::Spade => '♠',
            Suit::Heart => '♥',
            Suit::Club => '♣',
            Suit::Diamond => '♦',
        }
    }
}

impl std::fmt::Display for Card {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}{}", Card::num_to_char(self.n()), self.suit().unicode())
    }
}

//endregion

//region Action

impl Action {
    pub fn new(kind: ActionType, player_id: u8, data: ActionData) -> Self { Self{kind, player_id, data} }
    pub fn no_data(kind: ActionType, player_id: u8) -> Self { Self{kind, player_id, data: ActionData::invalid()} }
}

impl ActionData {
    pub fn invalid()                            -> Self     { Self(u32::MAX) }
    pub fn new_handle(h: u32)                   -> Self     { Self(h) }
    pub fn new_num(n: Number)                   -> Self     { Self(n.to_bits()) }
    pub fn new_message(s: Span)                 -> Self     { assert!(s.size() <= 255, "Message is too long {} - max: 255", s.size()); Self(s.begin() as u32 | (s.size() << Self::DATA_MSG_SIZE_SHIFT) as u32) }
    
    pub fn handle(self)                         -> u32      { self.0 }
    pub fn num(self)                            -> Number   { Number::from_bits(self.0) }
    pub fn cards(self, v: &HandVec)             -> Cards    { if self == Self::invalid() { Cards::default() } else { v.cards[self.handle() as usize] } }

    pub fn message_span(&self, offset: usize)   -> Span     { Span::new((self.0 & Self::DATA_MSG_OFF) as usize + offset, (self.0 >> Self::DATA_MSG_SIZE_SHIFT) as usize) }
    pub fn message<'a>(&self, h: usize, v: &'a HandVec) -> &'a str { &v.src[self.message_span(v.hands[h].src_offset)] }
    pub fn pair(self, v: &HandVec)              -> (Number, Number) { (v.nums[self.handle() as usize], v.nums[self.handle() as usize + 1]) }

    const DATA_MSG_OFF: u32 = 0x00ffffff;
    const DATA_MSG_SIZE_SHIFT  : u32 = 24;
}

impl ActionType {
    pub fn is_all_in(self) -> bool {
        match self {
            Self::BetAllIn | Self::CallAllIn | Self::RaiseAllIn => true,
            _ => false
        }
    }
    
    pub fn can_have_num(self) -> bool {
        use ActionType::*;
        match self {
            Bet | BetAllIn | Call | CallAllIn | Raise | RaiseAllIn 
            | Ante | BigBlind | SmallBlind | BigSmallBlind | DeadBlind | ExtraBlind 
            | CollectMainPot | CollectSidePot1 | CollectSidePot2 | CollectSidePot3 
            | UncalledBetReturned
                => true,
            _ => false,
        }
    }

    pub fn can_have_all_in(self) -> bool {
        use ActionType::*;
        match self {
            Bet | BetAllIn | Call | CallAllIn | Raise | RaiseAllIn => true,
            _ => false
        }
    }

    pub fn can_have_pot(self) -> bool {
        use ActionType::*;
        match self {
            CollectMainPot | CollectSidePot1 | CollectSidePot2 | CollectSidePot3 => true,
            _ => false
        }
    }

    pub fn can_have_blind(self) -> bool {
        use ActionType::*;
        match self {
            Ante | BigBlind | SmallBlind | BigSmallBlind | DeadBlind | ExtraBlind => true,
            _ => false
        }
    }

    pub fn can_have_cards(self) -> bool {
        use ActionType::*;
        match self {
            Fold | Muck | Show | Dealt => true,
            _ => false,
        }
    }
}


//endregion

//region Span

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Span (u64);

pub trait SpanLike where Self: Sized {
    fn new(begin: usize, size: usize) -> Self;
    fn range(begin: usize, end: usize) -> Self;
    fn begin(&self)     -> usize;
    fn size(&self)      -> usize;
    fn is_empty(&self)  -> bool { self.size() == 0 }
    fn end(&self)       -> usize { self.begin() + self.size() }
}

impl Span {
    const SHIFT_SIZE : u64 = 40;
    const MASK_OFFSET: u64 = 0xffffffff_ffffffff >> (64 - Self::SHIFT_SIZE);

    pub fn from_str_slice(part: &str, whole_buffer: &str) -> Self {
        let offset = part.as_ptr() as usize - whole_buffer.as_ptr() as usize;
        Self::new(offset, part.len())
    }
}

impl SpanLike for Span {
    fn new(begin: usize, size: usize) -> Self { Self((begin as u64) | (size << Self::SHIFT_SIZE) as u64) }
    fn range(begin: usize, end: usize) -> Self { Self((begin as u64) | ((end - begin) << Self::SHIFT_SIZE) as u64) }

    fn size(&self)      -> usize { (self.0 >> Self::SHIFT_SIZE) as usize }
    fn begin(&self)     -> usize { (self.0 & Self::MASK_OFFSET) as usize }
}

impl std::default::Default for Span {
    fn default() -> Self { Self::new(0, 0) }
}

impl std::ops::Index<Span> for str {
    type Output = str;
    fn index(&self, index: Span) -> &Self::Output {
        <str as std::ops::Index<std::ops::Range<usize>>>::index(self, index.begin()..index.end())
    }
}

impl std::ops::Index<Span> for String {
    type Output = str;
    fn index(&self, index: Span) -> &Self::Output {
        <String as std::ops::Index<std::ops::Range<usize>>>::index(self, index.begin()..index.end())
    }
}

pub trait TypedSpanStorage<T> where T: SpanLike {
    fn begin_span(&self, _: T) -> T;
    fn end_span(&self, span: T) -> T;
}

macro_rules! define_typed_span {
    ($name:ident, $t:ident, $hand_vec_member:ident) => {
        #[derive(Default, Debug, Clone, Copy, PartialEq, Eq)]
        pub struct $name(Span);

        impl SpanLike for $name {
            fn new(begin: usize, size: usize) -> Self { Self(Span::new(begin, size)) }
            fn range(begin: usize, size: usize) -> Self { Self(Span::range(begin, size)) }
            fn begin(&self)     -> usize { self.0.begin() }
            fn size(&self)      -> usize { self.0.size() }
        }

        impl std::ops::Index<$name> for HandVec {
            type Output = [$t];
            fn index(&self, index: $name) -> &Self::Output {
                <[$t] as std::ops::Index<std::ops::Range<usize>>>::index(&self.$hand_vec_member, index.begin()..index.end())
            }
        }

        impl std::ops::IndexMut<$name> for HandVec {
            fn index_mut(&mut self, index: $name) -> &mut Self::Output {
                <[$t] as std::ops::IndexMut<std::ops::Range<usize>>>::index_mut(&mut self.$hand_vec_member, index.begin()..index.end())
            }
        }

        impl TypedSpanStorage<$name> for HandVec {
            fn begin_span(&self, _: $name) -> $name { $name::new(self.$hand_vec_member.len(), 0) }
            fn end_span(&self, span: $name) -> $name { $name::range(span.begin(), self.$hand_vec_member.len()) }
        }
    };
}

define_typed_span!(HandSpan     , Hand,   hands);
define_typed_span!(ActionSpan   , Action, actions);
define_typed_span!(PlayerSpan   , Player, players);
define_typed_span!(WinnerSpan   , Winner, winners);
define_typed_span!(FlopSpan     , Street, flops);
define_typed_span!(TurnSpan     , Street, turns);
define_typed_span!(RiverSpan    , Street, rivers);
define_typed_span!(ShowdownSpan , Street, showdowns);

//endregion

//region DateTime

#[derive(Default, Clone, Copy, Eq, PartialEq)]
pub struct DateTime(u32);

impl DateTime {
    pub fn year(self)   -> u32 { Self::YEAR_BEGIN + ((self.0 & Self::MASK_YEAR) >> Self::SHIFT_YEAR) }
    pub fn month(self)  -> u32 { 1 + ((self.0 & Self::MASK_MONTH) >> Self::SHIFT_MONTH) }
    pub fn day(self)    -> u32 { 1 + ((self.0 & Self::MASK_DAY) >> Self::SHIFT_DAY) }
    pub fn min(self)    -> u32 { (self.0 & Self::MASK_MIN) >> Self::SHIFT_MIN }
    pub fn hour(self)   -> u32 { (self.0 & Self::MASK_HOUR) >> Self::SHIFT_HOUR }
    pub fn sec(self)    -> u32 { self.0 & Self::MASK_SEC }

    pub fn new(year: u32, month: u32, day: u32, hour: u32, min: u32, sec: u32) -> Self {
        Self(
            sec
            | (min << Self::SHIFT_MIN)
            | (hour << Self::SHIFT_HOUR)
            | ((day - 1) << Self::SHIFT_DAY)
            | ((month - 1) << Self::SHIFT_MONTH)
            | ((year - Self::YEAR_BEGIN) << Self::SHIFT_YEAR)
        )
    }

    const YEAR_BEGIN: u32 = 2000;

    const MASK_SEC  : u32 = 0b00000000_00000000_00000000_00111111;
    const MASK_MIN  : u32 = 0b00000000_00000000_00001111_11000000;
    const MASK_HOUR : u32 = 0b00000000_00000001_11110000_00000000;
    const MASK_DAY  : u32 = 0b00000000_00111110_00000000_00000000;
    const MASK_MONTH: u32 = 0b00000011_11000000_00000000_00000000;
    const MASK_YEAR : u32 = 0b11111100_00000000_00000000_00000000;

    const SHIFT_MIN  : u32 = 6;
    const SHIFT_HOUR : u32 = 12;
    const SHIFT_DAY  : u32 = 17;
    const SHIFT_MONTH: u32 = 22;
    const SHIFT_YEAR : u32 = 26;
}

impl std::fmt::Debug for DateTime {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:04}/{:02}/{:02} {:02}:{:02}:{:02}", self.year(), self.month(), self.day(), self.hour(), self.min(), self.sec())
    }
}

//endregion

//region Default Size Calculator

#[derive(Default)]
pub struct HandVecExpectedSize {
    max_sizes: [usize; 11],
    total_sizes: [usize; 11],
    count: usize,
}

impl HandVecExpectedSize {
    
    pub fn update(&mut self, h: &[HandVec]) {
        for v in h {
            self.max_sizes[0] = std::cmp::max(v.src.len(), self.max_sizes[0]);
            self.max_sizes[1] = std::cmp::max(v.hands.len(), self.max_sizes[1]);
            self.max_sizes[2] = std::cmp::max(v.players.len(), self.max_sizes[2]);
            self.max_sizes[3] = std::cmp::max(v.flops.len(), self.max_sizes[3]);
            self.max_sizes[4] = std::cmp::max(v.turns.len(), self.max_sizes[4]);
            self.max_sizes[5] = std::cmp::max(v.rivers.len(), self.max_sizes[5]);
            self.max_sizes[6] = std::cmp::max(v.showdowns.len(), self.max_sizes[6]);
            self.max_sizes[7] = std::cmp::max(v.actions.len(), self.max_sizes[7]);
            self.max_sizes[8] = std::cmp::max(v.nums.len(), self.max_sizes[8]);
            self.max_sizes[9] = std::cmp::max(v.cards.len(), self.max_sizes[9]);
            self.max_sizes[10] = std::cmp::max(v.winners.len(), self.max_sizes[10]);

            self.total_sizes[0] += v.src.len();
            self.total_sizes[1] += v.hands.len();
            self.total_sizes[2] += v.players.len();
            self.total_sizes[3] += v.flops.len();
            self.total_sizes[4] += v.turns.len();
            self.total_sizes[5] += v.rivers.len();
            self.total_sizes[6] += v.showdowns.len();
            self.total_sizes[7] += v.actions.len();
            self.total_sizes[8] += v.nums.len();
            self.total_sizes[9] += v.cards.len();
            self.total_sizes[10] += v.winners.len();
        }
        self.count += h.len();
    }

    pub fn max_rounded_up(&self) -> [usize; 11] {
        self.max_sizes.map(|x| Self::round_up_pot2(x))
    }

    pub fn avg_rounded_up(&self) -> [usize; 11] {
        self.total_sizes.map(|x| Self::round_up_pot2(x / self.count))
    }

    pub fn round_up_pot2(mut v: usize) -> usize {
        v -= 1;
        v |= v >> 1;
        v |= v >> 2;
        v |= v >> 4;
        v |= v >> 8;
        v |= v >> 16;
        v |= v >> 32;
        v += 1;
        v
    }
}
/*
 */

//endregion

//region Print

use std::fmt::{Formatter, Write};

struct Fmt<F>(F) where F: Fn(&mut Formatter) -> std::fmt::Result;

impl<F> std::fmt::Debug for Fmt<F> where F: Fn(&mut Formatter) -> std::fmt::Result {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        (self.0)(f)
    }
}


impl HandVec {
    fn f<'i, A: PrintHandVecItem + ?Sized>(&'i self, a: &'i A, hand: usize) -> impl std::fmt::Debug + 'i { Fmt(move |f| a.fmt(f, hand, self)) }
}


pub trait PrintHandVecItem {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result;
}


pub trait PrintHandVecInline {}


pub trait PrintHandVec {
    fn print(&self, hand: usize, r: &HandVec) -> String;
    fn pprint(&self, hand: usize, r: &HandVec) -> String;
}


impl<T> PrintHandVec for T where T: PrintHandVecItem + Sized {
    fn print(&self, hand: usize, r: &HandVec) -> String { format!("{:?}", &r.f(self, hand)) }
    fn pprint(&self, hand: usize, r: &HandVec) -> String { format!("{:#?}", &r.f(self, hand)) }
}


impl<T> PrintHandVecItem for [T] where T: PrintHandVecItem {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        let mut l = f.debug_list();
        for v in self { l.entry(&r.f(v, hand)); }
        l.finish()
    }
}


macro_rules! define_print_typed_span {
    ($t:ident) => {
        impl PrintHandVecItem for $t { fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result { r[*self].fmt(f, hand, r) } }    };
}
define_print_typed_span!(FlopSpan);
define_print_typed_span!(TurnSpan);
define_print_typed_span!(RiverSpan);
define_print_typed_span!(ShowdownSpan);
define_print_typed_span!(ActionSpan);
define_print_typed_span!(PlayerSpan);
define_print_typed_span!(WinnerSpan);

impl PrintHandVecItem for HandSpan { 
    fn fmt(&self, f: &mut Formatter, _hand: usize, r: &HandVec) -> std::fmt::Result { 
        let mut l = f.debug_list();
        for (i, v) in r[*self].iter().enumerate() {
            l.entry(&r.f(v, self.begin() + i));
        }
        l.finish()
    } 
}    


impl PrintHandVecItem for Span {
    fn fmt(&self, f: &mut Formatter, _hand: usize, r: &HandVec) -> std::fmt::Result {
        write!(f, "'{}'", &r.src[*self])
    }
}


impl PrintHandVecItem for HandVec {
    fn fmt(&self, f: &mut Formatter, _hand: usize, r: &HandVec) -> std::fmt::Result {
        HandSpan::new(0, self.hands.len()).fmt(f, 0, r)
    }
}


impl PrintHandVecItem for Hand {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Hand")
            .field("header", &r.f(&self.header, hand))
            .field("preflop", &r.f(&self.preflop, hand))
            .field("flops", &r.f(self.street(StreetType::Flop, r), hand))
            .field("turns", &r.f(self.street(StreetType::Turn, r), hand))
            .field("rivers", &r.f(self.street(StreetType::River, r), hand))
            .field("showdowns", &r.f(self.street(StreetType::Showdown, r), hand))
            .field("summary", &r.f(&self.summary, hand))
            .finish()
    }
}


impl PrintHandVecItem for Header {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Header")
            .field("id", &r.f(&self.id, hand))
            .field("site", &self.site)
            .field("game_type", &self.game_type)
            .field("currency", &self.currency)
            .field("table_name", &r.f(&self.table_name, hand))
            .field("max_players", &self.max_players)
            .field("dealer", &self.dealer)
            .field("hero", &self.hero)
            .field("ante", &self.ante)
            .field("small_blind", &self.small_blind)
            .field("big_blind", &self.big_blind)
            .field("start_date", &self.start_date)
            .field("players", &r.f(&self.players, hand))
            .field("actions", &r.f(&self.actions, hand))
            .finish()
    }
}


impl PrintHandVecItem for Street {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Street")
            .field("cards", &r.f(&self.cards, hand))
            .field("actions", &r.f(&self.actions, hand))
            .finish()
    }
}


impl PrintHandVecItem for Summary {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Summary")
            .field("pots", &r.f(&self.pot, hand))
            .field("winners", &r.f(&self.winners, hand))
            .field("actions", &r.f(&self.actions, hand))
            .finish()
    }
}


impl PrintHandVecItem for PotInfo {
    fn fmt(&self, f: &mut Formatter, _hand: usize, _r: &HandVec) -> std::fmt::Result {
        f.debug_struct("PotInfo")
            .field("total", &self.total)
            .field("rake", &self.rake)
            .field("main", &self.main)
            .field("side_1", &self.side[0])
            .field("side_2", &self.side[1])
            .field("side_3", &self.side[2])
            .finish()
    }
}


impl PrintHandVecItem for Player {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Player")
            .field("name", &r.f(&self.name, hand))
            .field("seat", &self.seat)
            .field("chips", &self.chips)
            .finish()
    }
}


impl PrintHandVecItem for Winner {
    fn fmt(&self, f: &mut Formatter, _hand: usize, _r: &HandVec) -> std::fmt::Result {
        f.debug_struct("Winner")
            .field("player_id", &self.player_id)
            .field("amount", &self.amount)
            .field("game_id", &self.game_id)
            .finish()
    }
}


impl PrintHandVecItem for Action {
    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec) -> std::fmt::Result {
        let mut s = f.debug_struct("Action");
        s.field("type", &self.kind);
        s.field("player_id", &self.player_id);
        match self.kind {
            ActionType::Check | ActionType::Leave | ActionType::Sitout => {}
            _ => { s.field(ActionData::fmt_key(self.kind), &Fmt(move |f| self.data.fmt(f, hand, r, self.kind))); }
        }
        s.finish()
    }
}


impl ActionData {
    fn fmt_key(t: ActionType) -> &'static str {
        use ActionType::*;
        match t {
            Bet | BetAllIn | Call | CallAllIn | Raise | RaiseAllIn 
            | Ante | BigBlind | SmallBlind | BigSmallBlind | DeadBlind | ExtraBlind 
            | CollectMainPot | CollectSidePot1 | CollectSidePot2 | CollectSidePot3 | UncalledBetReturned 
                => "amount",
            
            Fold | Muck | Show | Dealt
                => "cards",

            Say
                => "msg",

            Join
                => "seat",

            _ 
                => "data",
        }
    }

    fn fmt(&self, f: &mut Formatter, hand: usize, r: &HandVec, t: ActionType) -> std::fmt::Result {
        use ActionType::*;
        match t {
            Bet | BetAllIn | Call | CallAllIn | Raise | RaiseAllIn 
            | Ante | BigBlind | SmallBlind | BigSmallBlind | DeadBlind | ExtraBlind 
            | CollectMainPot | CollectSidePot1 | CollectSidePot2 | CollectSidePot3 | UncalledBetReturned => 
            {
                write!(f, "{}", self.num())?;
            }
            
            Fold | Muck | Show | Dealt => {
                self.cards(r).fmt(f, hand, r)?;
            }

            Say => {
                write!(f, "'{}'", self.message(hand, r))?;
            }

            Join => {
                write!(f, "{}", self.handle())?;
            }

            CashOut => {
                let (amt, fee) = self.pair(r);
                f.debug_struct("CashOut")
                    .field("amount", &amt)
                    .field("fee", &fee)
                    .finish()?;
            }
            _ => {}
        }
        Ok(())
    }
}


// Card already has a nice display routine
impl PrintHandVecItem for Card {
    fn fmt(&self, f: &mut Formatter, _hand: usize, _: &HandVec) -> std::fmt::Result {
        write!(f, "{}", self)
    }
}

// Since len(Cards) is always <= 5, they should always be inlined
impl PrintHandVecItem for Cards {
    fn fmt(&self, f: &mut Formatter, _hand: usize, _: &HandVec) -> std::fmt::Result {
        write!(f, "{}", self)
    }
}

impl std::fmt::Display for Cards {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.write_char('[')?;
        f.write_char(' ')?;
        let mut space = false;
        for c in &self.values[..self.size as usize] {
            if space { f.write_char(' ')?; }
            write!(f, "{}", c)?;
            space = true;
        }
        f.write_char(' ')?;
        f.write_char(']')
    }
}

//endregion
