#![feature(portable_simd)]

pub mod simd;
#[macro_use]
pub mod pklp;
pub mod parsers;
pub mod api;
pub mod json;
pub mod combine;

use json::{Json, JsonCompact, JsonOHH};
use pklp::*;
use std::sync::Arc;

/*
*/

use pyo3::exceptions::{PyIndexError, PyValueError, PyRuntimeError, PyTypeError};
use pyo3::{PyObject, PyRef, PyClass, prelude::*, types::{PySlice, PyDateTime}};

type    HandVecRef = Arc<HandVec>;

//region Helpers

#[derive(FromPyObject)]
enum SequenceIndex<'a> {
    Integer(isize),
    Slice(&'a PySlice),
}


fn py_index(i: isize, len: usize) -> PyResult<usize> {
    if (i >= len as isize) || (i < -(len as isize)) { return Err(PyIndexError::new_err(())); }
    Ok(if i < 0 { len as isize + i } else { i } as usize)
}

trait PyMake where Self: PyClass + Into<PyClassInitializer<Self>> {
    type T;
    fn new(h: &HandVecRef, i: usize, o: Self::T) -> Self;

    fn make(py: Python<'_>, h: &HandVecRef, i: usize, o: Self::T) -> PyResult<Py<Self>> { 
        Py::new(py, Self::new(h, i, o))
    }
}

trait GetHandIndexStored { 
    fn hand_index(&self) -> usize; 
}

trait GetHandIndex {
    fn get_hand_index(&self, index: usize) -> usize;
}

impl<T> GetHandIndex for T where T: GetHandIndexStored {
    fn get_hand_index(&self, index: usize) -> usize { self.hand_index() }
}

macro_rules! py_wrapper {
    ($py_name:ident, $name:ident, $name_str:literal) => {
        #[pyclass(module="poker_log_parser", name=$name_str)]
        struct $py_name {
            h: HandVecRef,
            i: usize,
            o: $name,
        }
        impl PyMake for $py_name {
            type T = $name;
            fn new(h: &HandVecRef, i: usize, o: Self::T) -> Self { $py_name{h: h.clone(), i, o} }
        }
    };
}

macro_rules! py_view_getitem {
    ($span_t:ident, $pyt:ident) => {
        fn __getitem__(slf: PyRef<'_, Self>, i: SequenceIndex<'_>) -> PyResult<PyObject> { 
            match i {
                SequenceIndex::Integer(index) => {
                    let i = py_index(index, slf.__len__())?;
                    let hand = slf.get_hand_index(i);
                    Ok($pyt::make(slf.py(), &slf.h, hand, slf.h[slf.o][i])?.into_py(slf.py()))
                }
                SequenceIndex::Slice(slice) => {
                    let idx = slice.indices(slf.__len__() as i32)?;
                    if idx.step != 1 { return Err(PyValueError::new_err(())); }
                    let range = $span_t::range(slf.o.begin() + idx.start as usize, slf.o.begin() + idx.stop as usize);
                    Ok(Self::make(slf.py(), &slf.h, slf.i, range)?.into_py(slf.py()))
                }
            }
        }
    };
}

macro_rules! py_view {
    ($py_name:ident, $name:literal, $span_t:ident, $pyt:ident) => {
        #[pyclass(module="poker_log_parser", name=$name)]
        struct $py_name {
            h: HandVecRef,
            i: usize,
            o: $span_t,
        }

        impl PyMake for $py_name {
            type T = $span_t;
            fn new(h: &HandVecRef, i: usize, o: Self::T) -> Self { $py_name{h: h.clone(), i, o} }
        }

        #[pymethods]
        impl $py_name {
            fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
            fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }
            fn __len__(&self) -> usize { self.o.size() as usize }
            py_view_getitem!($span_t, $pyt);

            fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }

        }
    };
}


macro_rules! py_enum {
    ($py_name:ident, $name:ident, $name_str:literal, $($key:ident,)*) => {
        #[pyclass(module="poker_log_parser", name=$name_str)]
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        enum $py_name {
            $( $key = $name::$key as isize, )*
        }

        #[pymethods]
        impl $py_name {
            fn __repr__(&self) -> String { format!("{:?}", self) }
            fn __str__(&self) -> String { format!("{:?}", self) }
        }

        impl $py_name {
            fn from(v: $name) -> $py_name {
                match v {
                    $( $name::$key => $py_name::$key, )*
                }
            }
            fn to(&self) -> $name {
                match self {
                    $( $py_name::$key => $name::$key, )*
                }
            }
        }
    };
}

impl GetHandIndex for PyHandView { 
    fn get_hand_index(&self, index: usize) -> usize {
        self.o.begin() + index
    } 
}

impl GetHandIndexStored for PyActionView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyFlopView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyRiverView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyTurnView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyShowdownView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyPlayerView { fn hand_index(&self) -> usize { self.i } }
impl GetHandIndexStored for PyWinnerView { fn hand_index(&self) -> usize { self.i } }

fn py_player(py: Python<'_>, h: &HandVecRef, hand: usize, id: u8) -> PyResult<Py<PyPlayer>> {
    PyPlayer::make(py, h, hand, *h.hands[hand].header.player(id, h))
}

fn py_json<'a, T: Json<JsonCompact<'a>>>(v: &T, h: &'a HandVecRef) -> PyResult<String> {
    match crate::json::to_json(v, h.as_ref()) {
        Ok(v) => Ok(v),
        Err(e) => Err(PyRuntimeError::new_err(format!("Failed to write json: {}", e)))
    }
}

fn py_json_ohh<'a, T: Json<JsonOHH<'a>>>(v: &T, h: &'a HandVecRef) -> PyResult<String> {
    match crate::json::to_json_ohh(v, h.as_ref()) {
        Ok(v) => Ok(v),
        Err(e) => Err(PyRuntimeError::new_err(format!("Failed to write json: {}", e)))
    }
}

//endregion

//region Views

py_view!(PyActionView   , "ActionView"  , ActionSpan    , PyAction);
py_view!(PyFlopView     , "FlopView"    , FlopSpan      , PyStreet);
py_view!(PyRiverView    , "RiverView"   , RiverSpan     , PyStreet);
py_view!(PyTurnView     , "TurnView"    , TurnSpan      , PyStreet);
py_view!(PyShowdownView , "ShowdownView", ShowdownSpan  , PyStreet);
py_view!(PyPlayerView   , "PlayerView"  , PlayerSpan    , PyPlayer);
py_view!(PyWinnerView   , "WinnerView"  , WinnerSpan    , PyWinner);

py_enum!(PyPot, Pot, "Pot", 
    Main, Side1, Side2, Side3, );

py_enum!(PyBlind, Blind, "Blind", 
    Ante, Small, Big, Both, Dead, Extra, );

py_enum!(PyStreetType, StreetType, "StreetType", 
    Flop, Turn, River, Showdown,);

py_enum!(PyBetType, BetType, "BetType", 
    NoLimit, Limit, PotLimit, );

py_enum!(PySuit, Suit, "Suit", 
    Heart, Spade, Diamond, Club, );

py_enum!(PyGameType, GameType, "GameType",
    HoldEm,
    Omaha,
    OmahaHiLo,
);

py_enum!(PyPokerSite, PokerSite, "PokerSite",
    PokerStars,
    PokerStarsPluribus,
    OnGame,

    Absolute,
    EverLeaf,
    BetOnline,
    FullTiltPoker,
    PacificPoker,
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
);

//region PyActionType

#[pyclass(module="poker_log_parser", name="ActionType")]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum PyActionType {
    Bet,
    Call,
    Raise,

    Check,
    Fold,
    Muck,
    Show,
    Dealt,

    Blind,
    CashOut,
    CollectPot,
    UncalledBetReturned,

    Join,
    Leave,
    Sitout,
    Say,
}

#[pymethods]
impl PyActionType {
    fn __repr__(&self) -> String { format!("{:?}", self) }
    fn __str__(&self) -> String { format!("{:?}", self) }
}

impl PyActionType {
    fn from(v: ActionType) -> PyActionType {
        match v {
            ActionType::Bet |
            ActionType::BetAllIn => PyActionType::Bet,
            ActionType::Call |
            ActionType::CallAllIn => PyActionType::Call,
            ActionType::Raise |
            ActionType::RaiseAllIn => PyActionType::Raise,
            ActionType::Check => PyActionType::Check,
            ActionType::Fold => PyActionType::Fold,
            ActionType::Muck => PyActionType::Muck,
            ActionType::Show => PyActionType::Show,
            ActionType::Dealt => PyActionType::Dealt,
            ActionType::Ante => PyActionType::Blind,
            ActionType::BigBlind |
            ActionType::SmallBlind |
            ActionType::BigSmallBlind |
            ActionType::DeadBlind |
            ActionType::ExtraBlind => PyActionType::Blind,
            ActionType::CashOut => PyActionType::CashOut,
            ActionType::CollectMainPot |
            ActionType::CollectSidePot1 |
            ActionType::CollectSidePot2 |
            ActionType::CollectSidePot3 => PyActionType::CollectPot,
            ActionType::UncalledBetReturned => PyActionType::UncalledBetReturned,
            ActionType::Join => PyActionType::Join,
            ActionType::Leave => PyActionType::Leave,
            ActionType::Sitout => PyActionType::Sitout,
            ActionType::Say => PyActionType::Say,
        }
    }
}

//endregion

//endregion

//region HandView

#[pyclass(module="poker_log_parser", name="HandView")]
struct PyHandView {
    h: HandVecRef,
    i: usize,
    o: HandSpan,
}

impl PyMake for PyHandView {
    type T = HandSpan;
    fn new(h: &HandVecRef, i: usize, o: Self::T) -> Self { PyHandView{h: h.clone(), i, o} }
}

#[pymethods]
impl PyHandView {
    fn __len__(&self) -> usize { self.o.size() as usize }
    py_view_getitem!(HandSpan, PyHand);
    
    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }

    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
    
    fn to_json_ohh(&self) -> PyResult<String> { py_json_ohh(&self.o, &self.h) }

    // combine

    // load(path: str) -> 'HandView': ...
    // save(self, path: str): ...
    
    // from_bytes(data: bytes) -> 'HandView': ...
    // to_bytes(self) -> bytes: ...

    // sort
}


//endregion

//region Hand

py_wrapper!(PyHand, Hand, "Hand");

#[pymethods]
impl PyHand {
    #[getter] fn header(slf: PyRef<'_, Self>)   -> PyResult<Py<PyHeader>>       { PyHeader::make(slf.py(), &slf.h, slf.i, slf.o.header.clone()) }
    #[getter] fn preflop(slf: PyRef<'_, Self>)  -> PyResult<Py<PyStreet>>       { PyStreet::make(slf.py(), &slf.h, slf.i, slf.o.preflop.clone()) }
    #[getter] fn flops(slf: PyRef<'_, Self>)    -> PyResult<Py<PyFlopView>>     { PyFlopView::make(slf.py(), &slf.h, slf.i, slf.o.flops()) }
    #[getter] fn turns(slf: PyRef<'_, Self>)    -> PyResult<Py<PyTurnView>>     { PyTurnView::make(slf.py(), &slf.h, slf.i, slf.o.turns()) }
    #[getter] fn rivers(slf: PyRef<'_, Self>)   -> PyResult<Py<PyRiverView>>    { PyRiverView::make(slf.py(), &slf.h, slf.i, slf.o.rivers()) }
    #[getter] fn showdowns(slf: PyRef<'_, Self>)-> PyResult<Py<PyShowdownView>> { PyShowdownView::make(slf.py(), &slf.h, slf.i, slf.o.showdowns()) }
    #[getter] fn summary(slf: PyRef<'_, Self>)  -> PyResult<Py<PySummary>>      { PySummary::make(slf.py(), &slf.h, slf.i, slf.o.summary.clone()) }

    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }

    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }

    fn to_json_ohh(&self) -> PyResult<String> { py_json_ohh(&self.o, &self.h) }
}

//endregion

//region Header

// Header
py_wrapper!(PyHeader, Header, "Header");

#[pymethods]
impl PyHeader {
    #[getter] fn id(&self)                      -> &str                         { &self.h.src[self.o.id] }
    #[getter] fn table_name(&self)              -> &str                         { &self.h.src[self.o.table_name] }
    #[getter] fn site(&self)                    -> PyPokerSite                  { PyPokerSite::from(self.o.site) }
    #[getter] fn game_type(&self)               -> PyGameType                   { PyGameType::from(self.o.game_type) }
    #[getter] fn bet_type(&self)                -> PyBetType                    { PyBetType::from(self.o.bet_type) }
    #[getter] fn currency(&self)                -> char                         { self.o.currency }
    #[getter] fn currency_iso(&self)            -> &str                         { self.o.currency_iso() }
    #[getter] fn dealer(&self)                  -> u8                           { self.o.dealer }
    #[getter] fn hero(&self)                    -> u8                           { self.o.hero }
    #[getter] fn max_players(&self)             -> u8                           { self.o.max_players }
    #[getter] fn ante(&self)                    -> Number                       { self.o.ante }
    #[getter] fn small_blind(&self)             -> Number                       { self.o.small_blind }
    #[getter] fn big_blind(&self)               -> Number                       { self.o.big_blind }
    #[getter] fn bet_cap(&self)                 -> Number                       { self.o.bet_cap }
    #[getter] fn is_tournament(&self)           -> bool                         { self.o.is_tournament }
    #[getter] fn players(slf: PyRef<'_, Self>)  -> PyResult<Py<PyPlayerView>>   { PyPlayerView::make(slf.py(), &slf.h, slf.i, slf.o.players) }
    #[getter] fn actions(slf: PyRef<'_, Self>)  -> PyResult<Py<PyActionView>>   { PyActionView::make(slf.py(), &slf.h, slf.i, slf.o.actions) }

    #[getter] fn datetime<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDateTime> {
        PyDateTime::new(py, 
            self.o.start_date.year() as i32, 
            self.o.start_date.month() as u8, 
            self.o.start_date.day() as u8, 
            self.o.start_date.hour() as u8, 
            self.o.start_date.min() as u8, 
            self.o.start_date.sec() as u8, 
            0, 
            None
        )
    }
    
    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }

    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
}

//endregion

//region Street

py_wrapper!(PyStreet, Street, "Street");

#[pymethods]
impl PyStreet {
    #[getter] fn id(&self)                      -> u8                           { self.o.id }
    #[getter] fn cards(slf: PyRef<'_, Self>)    -> PyResult<Py<PyCards>>        { Py::new(slf.py(), PyCards{o: slf.o.cards}) }
    #[getter] fn actions(slf: PyRef<'_, Self>)  -> PyResult<Py<PyActionView>>   { PyActionView::make(slf.py(), &slf.h, slf.i, slf.o.actions) }
    
    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }

    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
}

//endregion

//region Summary

py_wrapper!(PySummary, Summary, "Summary");

#[pymethods]
impl PySummary {
    #[getter] fn total_pot(&self)              -> Number                      { self.o.pot.total }
    #[getter] fn main_pot(&self)               -> Number                      { self.o.pot.main }
    #[getter] fn side_pots(&self)              -> [Number; 3]                 { self.o.pot.side }
    #[getter] fn side_pot_1(&self)             -> Number                      { self.o.pot.side[0] }
    #[getter] fn side_pot_2(&self)             -> Number                      { self.o.pot.side[1] }
    #[getter] fn side_pot_3(&self)             -> Number                      { self.o.pot.side[2] }
    #[getter] fn rake(&self)                   -> Number                      { self.o.pot.rake }
    #[getter] fn actions(slf: PyRef<'_, Self>) -> PyResult<Py<PyActionView>>  { PyActionView::make(slf.py(), &slf.h, slf.i, slf.o.actions) }
    #[getter] fn winners(slf: PyRef<'_, Self>) -> PyResult<Py<PyWinnerView>>  { PyWinnerView::make(slf.py(), &slf.h, slf.i, slf.o.winners) }
    
    fn side_pot(&self, i: usize)               -> PyResult<Number>            { 
        if i > 2 { return Err(PyIndexError::new_err(())); }
        Ok(self.o.pot.side[i])
    }
    
    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }
    
    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
}

//endregion

//region Player

py_wrapper!(PyPlayer, Player, "Player");

#[pymethods]
impl PyPlayer {
    #[getter] fn name(&self)                    -> &str                         { &self.h.src[self.o.name]  }
    #[getter] fn seat(&self)                    -> u8                           { self.o.seat }
    #[getter] fn chips(&self)                   -> Number                       { self.o.chips }
    
    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }
}

//endregion

//region Winner

py_wrapper!(PyWinner, Winner, "Winner");

#[pymethods]
impl PyWinner {
    #[getter] fn player_id(&self)               -> u8                           { self.o.player_id }
    #[getter] fn amount(&self)                  -> Number                       { self.o.amount }    
    #[getter] fn player(slf: PyRef<'_, Self>)   -> PyResult<Py<PyPlayer>>       { py_player(slf.py(), &slf.h, slf.i, slf.o.player_id) }

    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }
    
    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
}

//endregion

//region Action

py_wrapper!(PyAction, Action, "Action");

#[pyclass(module="poker_log_parser", name="Cashout")]
struct PyCashout  {
    #[pyo3(get)] amount: Number, 
    #[pyo3(get)] fee: Number,
}

#[pymethods]
impl PyAction {
    #[getter] fn r#type(&self)                  -> PyActionType                 { PyActionType::from(self.o.kind) }
    #[getter] fn player_id(&self)               -> u8                           { self.o.player_id  }
    #[getter] fn all_in(&self)                  -> bool                         { self.o.kind.is_all_in() }
    #[getter] fn player(slf: PyRef<'_, Self>)   -> PyResult<Py<PyPlayer>>       { py_player(slf.py(), &slf.h, slf.i, slf.o.player_id) }

    #[getter] fn data(slf: PyRef<'_, Self>)     -> PyResult<Py<PyAny>>          {
        Ok(if slf.o.kind.can_have_num() {
            slf.o.data.num().into_py(slf.py())
        }
        else if slf.o.kind.can_have_cards() {
            PyCards{o: slf.o.data.cards(slf.h.as_ref())}.into_py(slf.py())
        }
        else if slf.o.kind == ActionType::Say {
            slf.o.data.message(slf.i, slf.h.as_ref()).into_py(slf.py())
        } 
        else if slf.o.kind == ActionType::Join {
            slf.o.data.handle().into_py(slf.py())
        }
        else if slf.o.kind == ActionType::CashOut {
            let (a, f) = slf.o.data.pair(slf.h.as_ref());
            PyCashout{amount: a, fee: f}.into_py(slf.py())
        }
        else {
            return Err(PyRuntimeError::new_err(format!("Invalid action kind: {:?}", slf.o.kind)));
        })
    }
    
    #[getter] fn blind(&self)                   -> PyResult<PyBlind>            { 
        if !self.o.kind.can_have_blind() {
            return Err(PyTypeError::new_err("Can only use 'blind' property on actions with type 'Blind'"));
        }
        Ok(PyBlind::from(Blind::from(self.o.kind)))
    }

    #[getter] fn pot(&self)                     -> PyResult<PyPot>              {
        if !self.o.kind.can_have_pot() {
            return Err(PyTypeError::new_err("Can only use 'pot' property on actions with type 'CollectPot'"));
        }
        Ok(PyPot::from(Pot::from(self.o.kind)))
    }

    fn __repr__(&self) -> String { self.o.print(self.i, self.h.as_ref()) }
    fn __str__(&self) -> String { self.o.pprint(self.i, self.h.as_ref()) }
    
    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &self.h) }
}

//endregion

//region Cards

#[pyclass(module="poker_log_parser", name="Card")]
struct PyCard { o: Card, }

#[pyclass(module="poker_log_parser", name="Cards")]
struct PyCards { o: Cards, }


#[pymethods]
impl PyCard {
    #[getter] fn n(&self)                       -> u8                           { self.o.n() }
    #[getter] fn suit(&self)                    -> PySuit                       { PySuit::from(self.o.suit()) }
    
    fn __repr__(&self) -> String { format!("{}", self.o) }
    fn __str__(&self) -> String { format!("{}", self.o) }

    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &HandVecRef::new(HandVec::default())) }
}


#[pymethods]
impl PyCards {
    fn __repr__(&self) -> String { format!("{}", self.o) }
    fn __str__(&self) -> String { format!("{}", self.o) }
    
    fn to_json(&self) -> PyResult<String> { py_json(&self.o, &HandVecRef::new(HandVec::default())) }

    fn __len__(&self) -> usize { self.o.size as usize }
    fn __getitem__(slf: PyRef<'_, Self>, i: SequenceIndex<'_>) -> PyResult<PyObject> { 
        match i {
            SequenceIndex::Integer(index) => {
                Ok(PyCard{o: slf.o[py_index(index, slf.__len__())?]}.into_py(slf.py()))
            }
            SequenceIndex::Slice(slice) => {
                let mut c = Cards::default();
                let idx = slice.indices(slf.__len__() as i32)?;
                let mut offset = idx.start;
                while offset < idx.stop {
                    c.push(slf.o[offset as usize]);
                    offset += idx.step;
                }
                Ok(PyCards{o: c}.into_py(slf.py()))
            }
        }
    }
}

//endregion

//region Funcs

#[pyfunction(module="poker_log_parser")]
fn parse_str(py: Python, src: &str) -> PyResult<PyHandView> {
    let r = py.allow_threads(move || api::parse_string(src));
    match r {
        Ok(v) => Ok(to_hand_view(v)),
        Err(e) => Err(PyRuntimeError::new_err(e))
    }
}


#[pyfunction(module="poker_log_parser")]
fn parse_path(py: Python, path: &str) -> PyResult<PyHandView> {
    let r = py.allow_threads(move || api::parse_path(path));
    match r {
        Ok(v) => Ok(to_hand_view(v)),
        Err(e) => Err(PyRuntimeError::new_err(e))
    }
}


#[pyfunction(module="poker_log_parser")]
fn parse_strs(py: Python, srcs: Vec<String>) -> Vec<PyHandView> {
    py.allow_threads(move || api::parse_strings(srcs))
        .into_iter()
        .map(|x| to_hand_view(x))
        .collect()
}


#[pyfunction(module="poker_log_parser")]
fn parse_paths(py: Python, paths: Vec<String>) -> Vec<PyHandView> {
    py.allow_threads(move || api::parse_paths(&paths))
        .into_iter()
        .map(|x| to_hand_view(x))
        .collect()
}


// TODO: Python - Combine


// TODO: Python - To bytes


// TODO: Python - From bytes


// TODO: Python - Load


// TODO: Python - Save


#[pyfunction(module="poker_log_parser")]
fn to_json(py: Python, view: &PyHandView) -> PyResult<String> {
    py.allow_threads(move || view.to_json())
}


// TODO: Python - From json


#[pyfunction(module="poker_log_parser")]
fn to_json_ohh(py: Python, view: &PyHandView) -> PyResult<String> {
    py.allow_threads(move || view.to_json_ohh())
}


// TODO: Python - From json OHH


fn to_hand_view(hands: HandVec) -> PyHandView {
    let n = hands.hands.len();
    PyHandView{h: Arc::new(hands), i: 0, o: HandSpan::range(0, n)}
}

//endregion

//region Module

/// A blazingly fast parser for poker hand histories
#[pymodule]
fn poker_log_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_str, m)?)?;
    m.add_function(wrap_pyfunction!(parse_strs, m)?)?;
    m.add_function(wrap_pyfunction!(parse_path, m)?)?;
    m.add_function(wrap_pyfunction!(parse_paths, m)?)?;

    // combine
    // from bytes
    // to bytes
    // load
    // save
    m.add_function(wrap_pyfunction!(to_json, m)?)?;
    // from json
    m.add_function(wrap_pyfunction!(to_json_ohh, m)?)?;
    // from json ohh
    
    // PyHandView is the only class with static methods, all other classes can remain internal
    m.add_class::<PyHandView>()?;

    Ok(())
}

//endregion
 