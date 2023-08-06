
use crate::pklp::*;
use crate::parsers::parser::*;
use crate::parsers::pokerstars::*;

pub struct OnGame {}

impl ParseSync for OnGame {
    fn parse_sync(p: &mut Parser) {
        while !p.eof() && !p.line.starts_with("***** ") {
            p.advance();
        }
        if !p.eof() && p.line.starts_with("***** End"){
            p.advance();
        }
    }
}

impl ParseNumberWithComma for OnGame {}

impl ParseTrimPlayerName for OnGame {}

impl ParseHeaderPlayersPokerStars for OnGame {}

impl ParseActionHeaderBlindOnly for OnGame {}

impl ParsePreFlopActionsOnly for OnGame {
    const PREFLOP_HEADER_LINE_COUNT: usize = 2;
}

impl ParseActionList for OnGame {
    fn is_section_line(line: &str) -> bool { line.starts_with("---") }
}


impl ParseHeaderPokerStars for OnGame {
    fn parse_header_hand_info(p: &mut Parser, h: &mut Header) -> Option<()> {
        // ***** History for hand R5-1631690-1825 *****
        h.site = PokerSite::OnGame;
        h.dealer = SEAT_NONE;
        h.hero = SEAT_NONE;
        h.id = p.push_str(&p.line["***** History for hand R5-".len()..p.line.len() - "-1825 *****".len()]);
        p.advance();

        // Start hand: Wed Jul 01 00:00:00 GMT-0910 2009
        p.advance(); // Time
        Some(())
    }

    fn parse_header_table_info(p: &mut Parser, h: &mut Header) -> Option<()> {
        // Table: YAT4jKACpEQGFsSRkTUtLA [1631690] (NO_LIMIT TEXAS_HOLDEM $3/$6, Real money)
        h.game_type = GameType::HoldEm;

        let table_name_begin = "Table: ".len();
        let table_name_end = table_name_begin + p.line[table_name_begin..].find('[')? - 1;
        h.table_name = p.push_str(&p.line[table_name_begin..table_name_end]);

        // TODO: Bet limit and game type
        // let game_desc_begin = table_name_end + h.id.size() + " [] (".len();

        let blind_sep = p.line.rfind('/')?;
        h.currency = parse_currency_char(&p.line[blind_sep+1..]).unwrap().0;
        h.big_blind = Self::parse_float(&p.line[blind_sep+1+h.currency.len_utf8()..]).unwrap().0;
        h.small_blind = Self::rfind_currency(&p.line[..blind_sep], h.currency).unwrap().0;

        p.advance();
        
        // Button: seat 5
        // Button: IMIT, R5
        let button = &p.line[p.line.rfind(' ')? + 1..];
        h.dealer = if !button.starts_with('R') { Self::parse_integer(button )?.0 as u8 } else { SEAT_NONE };
        p.advance();
        
        // Players in round:  4
        h.max_players = Self::parse_integer(&p.line[p.line.rfind(' ')? + 1..])?.0 as u8;
        p.advance();
        Some(())
    }
}


impl ParseStreet for OnGame {
    fn is_summary_line(line: &str) -> bool { line == "---" }

    fn parse_street_header(p: &mut Parser) -> (StreetType, Cards) {
        let street_type = match p.line["--- Dealing ".len()..].chars().next().unwrap() {
            'f' => StreetType::Flop,
            'r' => StreetType::River,
            't' => StreetType::Turn,
            _ => unreachable!(),
        };
        let cards_begin = p.line.rfind('[').unwrap() + 1;
        let cards = parse_cards(&p.line[cards_begin..p.line.len()-1]);
        p.advance();
        (street_type, cards)
    }
}


impl ParseSummary for OnGame {
    fn parse_summary(p: &mut Parser, currency: char) -> Option<Summary> {
        p.advance();
        p.advance();

        let actions = p.hands.begin_span(ActionSpan::default());
        let winners = p.hands.begin_span(WinnerSpan::default());

        let (total, total_end) = Self::extract_currency(p.line, currency, "Main pot: ".len()).unwrap();
        let name_begin = total_end + " won by ".len();
        let win_begin = p.line.rfind('(').unwrap();
        let win = Self::extract_currency(p.line, currency, win_begin + 1).unwrap().0;
        let winner_name = &p.line[name_begin..win_begin - 1];
        let winner_id = p.player_id(winner_name);
        let pot = PotInfo{total, main: total, side: [0.0, 0.0, 0.0], rake: total - win};
        p.hands.winners.push(Winner{amount: win, player_id: winner_id, game_id: 0});
        p.advance();
        
        while !p.line.starts_with('*') {
            if p.line.ends_with(']') {
                let cards = parse_cards(&p.line[p.line.rfind('[').unwrap() + 1..p.line.len()-1]);
                let (_, player_name, _) = parse_seat_name(p.line)?;
                let a = p.action_cards(ActionType::Show, player_name, cards);
                p.hands.actions.push(a);
            }
            p.advance();
        }
        p.advance();
        Some(Summary{pot, actions: p.hands.end_span(actions), winners: p.hands.end_span(winners)})
    }
}


impl ParseActionPreFlop for OnGame {  
    fn parse_action_preflop(p: &mut Parser, currency: char) -> Option<Action> {
        Self::parse_action_street(p, currency)
    }
}

impl ParseActionStreet for OnGame {  
    fn parse_action_street(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            parse_action_suffix_only!(ActionType::Fold,     "ds", " folds"),
            parse_action_suffix_only!(ActionType::Check,    "ks", " checks"),
            Self::parse_action_bet_call_raise,
        )
    }
}

impl ParseActionBlind for OnGame {
    fn parse_action_blind(p: &mut Parser, currency: char) -> Option<Action> {
        let (amount, (amount_begin, _)) = Self::rfind_currency(p.line, currency).unwrap();
        let cmd_end = amount_begin - "x blind (".len();
        let (t, suffix) = match p.line[cmd_end..].chars().next().unwrap() {
            'l' => (ActionType::SmallBlind, " posts smal"),
            'g' => (ActionType::BigBlind, " posts bi"),
            _ => unreachable!(),
        };
        Some(p.action_num(t, &p.line[..cmd_end - suffix.len()], amount))
    }
}    

impl OnGame {
    fn parse_action_bet_call_raise(p: &mut Parser, currency: char) -> Option<Action> {
        let all_in = p.line.ends_with(']');
        let (amount, (amount_begin, _)) = Self::find_currency(p.line, currency)?;
        let (kinds, suffix) = match p.line[amount_begin - 3..].chars().next().unwrap() {
            't' => ([ActionType::Bet, ActionType::BetAllIn], " bets "),
            'l' => ([ActionType::Call, ActionType::CallAllIn], " calls "),
            'e' =>  ([ActionType::Raise, ActionType::RaiseAllIn], " raises "),
            _ => return None,
        };
        Some(p.action_num(kinds[all_in as usize], &p.line[..amount_begin - suffix.len()], amount))
    }
}


#[cfg(test)]
pub mod tests {
    use super::*;

    macro_rules! test_parse {
        ($p:ident, $parse:ident, $src:expr, $r:expr, $f:expr) => {
            let hands = {
                let mut hands = HandVec::default();
                let mut p = Parser::new($src, &mut hands);
                let mut header = Header::default();
                header.currency = '$';
                p.add_player("a: d", 0, 0.0);
                p.add_player("efgh", 1, 0.0);
                let r = $p::$parse(&mut p, header.currency).unwrap();
                assert_eq!(r, $r);
                hands
            };
            $f(&hands);
        };

        ($p:ident, $parse:ident, $src:expr, $r:expr) => {
            test_parse!($p, $parse, $src, $r, |_h: &HandVec|{});
        };
    }

    #[test]
    fn parse_file() {
        let src = std::fs::read_to_string("tests/data/example/ongame_obf.txt").unwrap();
        let mut hands = HandVec::default();
        let mut p = Parser::new(&src, &mut hands);
        OnGame::parse(&mut p);
        assert_eq!(p.hands.hands.len(), 1000);
    }

    //region Header

    // Header

    #[test]
    fn header_blinds() {
        test_parse!(OnGame, parse_action_list_header,
            "a: d posts small blind ($1.23)\n---",
            ActionSpan::new(0, 1),
            |r: &HandVec| {
                assert_eq!(r.actions[0], Action::new(ActionType::SmallBlind, 0, ActionData::new_num(1.23)));
            }
        );

        test_parse!(OnGame, parse_action_list_header,
            "a: d posts big blind ($1.23)\n---",
            ActionSpan::new(0, 1),
            |r: &HandVec| {
                assert_eq!(r.actions[0], Action::new(ActionType::BigBlind, 0, ActionData::new_num(1.23)));
            }
        );
    }

    //endregion

    //region PreFlop

    #[test]
    fn preflop() {
        let src = concat!(
            "---\nDealing pocket cards\n",
            "a: d folds\n",
            "--- Dealing flop [Qh, Qh, Qh]"
        );
        let mut hands = HandVec::default();
        let mut p = Parser::new(src, &mut hands);
        let r = OnGame::parse_preflop(&mut p, '$').unwrap();
        assert_eq!(r, Street{cards: Cards::default(), id: 0, actions: ActionSpan::new(0, 1)});
    }

    //endregion

    //region Streets

    #[test]
    fn street_flop() {
        test_parse!(OnGame, parse_streets, 
            concat!(
                "--- Dealing flop [Qh Td As]\n",
                "a: d folds\n",
                "---",
            ),
            (FlopSpan::new(0, 1), TurnSpan::default(), RiverSpan::default(), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(Qh Td As), r.flops[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    #[test]
    fn street_turn() {
        test_parse!(OnGame, parse_streets, 
            concat!(
                "--- Dealing turn [5c]\n",
                "a: d folds\n",
                "---",
            ),
            (FlopSpan::default(), TurnSpan::new(0, 1), RiverSpan::default(), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(5c), r.turns[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    #[test]
    fn street_river() {
        test_parse!(OnGame, parse_streets, 
            concat!(
                "--- Dealing river [6c]\n",
                "a: d folds\n",
                "---",
            ),
            (FlopSpan::default(), TurnSpan::default(), RiverSpan::new(0, 1), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(6c), r.rivers[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    //endregion

    //region Summary

    //endregion

    //region Action

    #[test]
    fn action_fold_check() {
        test_parse!(OnGame, parse_action_street,
            "a: d folds",
            Action::no_data(ActionType::Fold, 0)
        );

        test_parse!(OnGame, parse_action_street,
            "a: d checks",
            Action::no_data(ActionType::Check, 0)
        );
    }

    
    #[test]
    fn action_bet_call() {
        test_parse!(OnGame, parse_action_street,
            "a: d bets $1,234.56",
            Action::new(ActionType::Bet, 0, ActionData::new_num(1234.56))
        );

        test_parse!(OnGame, parse_action_street,
            "a: d bets $1,234.56 [all in]",
            Action::new(ActionType::BetAllIn, 0, ActionData::new_num(1234.56))
        );

        test_parse!(OnGame, parse_action_street,
            "a: d calls $1,234.56",
            Action::new(ActionType::Call, 0, ActionData::new_num(1234.56))
        );

        test_parse!(OnGame, parse_action_street,
            "a: d calls $1,234.56 [all in]",
            Action::new(ActionType::CallAllIn, 0, ActionData::new_num(1234.56))
        );
    }

    #[test]
    fn action_raise() {
        test_parse!(OnGame, parse_action_street,
            "a: d raises $1,234.56 to $5,678.9",
            Action::new(ActionType::Raise, 0, ActionData::new_num(1234.56))
        );

        test_parse!(OnGame, parse_action_street,
            "a: d raises $1,234.56 to $5,678.9 [all in]",
            Action::new(ActionType::RaiseAllIn, 0, ActionData::new_num(1234.56))
        );
    }

    //endregion
}
