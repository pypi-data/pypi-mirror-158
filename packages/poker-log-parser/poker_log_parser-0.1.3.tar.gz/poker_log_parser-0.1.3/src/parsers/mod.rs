#[macro_use]
pub mod parser;
pub mod pokerstars;
pub mod ongame;

pub use pokerstars::{PokerStars, PokerStarsPluribus};
pub use ongame::OnGame;

use parser::Parse;
use crate::pklp::{PokerSite, HandVec};

pub fn detect_site(input: &str) -> Result<PokerSite, String> 
{
    use PokerSite::*;
    
    let trimmed = input.trim_start();
    Ok(if trimmed.starts_with("PokerStars ") {
        let line = trimmed.lines().nth(1).unwrap();
        if line.starts_with("Table 'Pluribus") {
            PokerStarsPluribus
        } else {
            PokerStars
        }
    }
    else if trimmed.starts_with("***** History") {
        OnGame
    }
    else if trimmed.starts_with("BetOnline ") {
        BetOnline
    }
    else if trimmed.starts_with("Bodog ") {
        Bovada
    } 
    else if trimmed.starts_with("Full Tilt ") {
        FullTiltPoker
    }
    else if trimmed.starts_with("Everleaf ") {
        EverLeaf
    }
    else if trimmed.starts_with("Winamax ") {
        Winamax
    }
    else if trimmed.starts_with("Stage ") {
        Absolute
    }
    else if trimmed.starts_with("#Game No ") {
        PacificPoker
    }
    else if trimmed.starts_with("Poker Hand #") {
        GGPoker
    }
    else if trimmed.starts_with("MERGE_GAME ") {
        PokerTracker
    }
    else if trimmed.starts_with("Hand#") {
        Cake
    }
    else if trimmed.starts_with("Table #") {
        Pkr
    }
    else if trimmed.starts_with("Game started ") {
        Winning
    }
    else if trimmed.starts_with('#') && trimmed[1..].chars().next().unwrap_or('a').is_numeric() {
        KingsClub
    }
    else if trimmed.starts_with("Game #") {
        let line = trimmed.lines().next().unwrap();
        if line.ends_with("starts.") {
            PartyPoker
        } else {
            Enet
        }
    }
    else {
        return Err(format!("Invalid poker website - '{}'", trimmed.lines().next().unwrap_or("@@@")));
    })
}

pub fn parse_str<'a>(site: PokerSite, s: &'a str, hands: &'a mut HandVec) {
    let mut p = parser::Parser::new(s, hands);
    match site {
        PokerSite::PokerStars           => PokerStars::parse(&mut p),
        PokerSite::PokerStarsPluribus   => PokerStarsPluribus::parse(&mut p),
        PokerSite::OnGame               => OnGame::parse(&mut p),
        _ => panic!("Parser has not been implemented for {:?}", site),
    }
}
