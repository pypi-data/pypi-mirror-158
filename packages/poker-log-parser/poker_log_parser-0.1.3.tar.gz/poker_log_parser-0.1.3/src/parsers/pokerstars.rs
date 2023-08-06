use crate::pklp::*;
use crate::parsers::parser::*;

pub struct PokerStars {}
pub struct PokerStarsPluribus {}

//region General

trait ParseSummaryResultPlayerName {
    fn parse_summary_result_player_name<'a>(p: &mut Parser, part: &'a str, name_end: usize) -> &'a str;
}

trait ParseSummaryPokerStars {
    fn parse_summary_pots(p: &mut Parser, currency: char) -> Option<PotInfo>;
    fn parse_summary_actions_winners(p: &mut Parser, currency: char) -> Option<(ActionSpan, WinnerSpan)>;
    fn parse_summary_winners(p: &mut Parser, part: &str, player_id: u8, currency: char);
}

impl<T> ParseSummary for T where T: ParseSummaryResultPlayerName + ParseCurrency {
    fn parse_summary(p: &mut Parser, currency: char) -> Option<Summary> {
        p.advance();
        let pot = Self::parse_summary_pots(p, currency)?;
        let (actions, winners) = Self::parse_summary_actions_winners(p, currency)?;
        Some(Summary{pot, actions, winners})
    }
}

impl<T> ParseSummaryPokerStars for T where T: ParseSummaryResultPlayerName + ParseCurrency {
    fn parse_summary_pots(p: &mut Parser, currency: char) -> Option<PotInfo> {
        // Total pot $144.46 | Rake $0.06
        // Total pot $144.46 | 
        // Total pot $144.46 | Rake $2
        // Total pot $144.46 | Rake 2
        // Total pot $144.46 Main pot $122.38. Side pot $20.08. | Rake $2
        // Total pot $144.46 Main pot $122.38. Side pot-1 $10.04. Side pot-2 $10.04. | Rake $2

        let rake_begin = p.line.rfind('|').unwrap() + "| Rake ".len();
        let rake = if rake_begin >= p.line.len() {
            0.0
        } else {
            if p.line[rake_begin..].starts_with(currency) {
                Self::parse_float(&p.line[rake_begin+currency.len_utf8()..]).unwrap().0
            } else {
                Self::parse_float(&p.line[rake_begin..]).unwrap().0
            }
        };

        let (total, (_, tot_end)) = Self::find_currency(p.line, currency).unwrap();

        let (main, main_end) = if let Some(i) = &p.line[tot_end..].find("Main ") {
            let begin = tot_end + i + "Main pot ".len();
            let (n, offset) = Self::extract_currency(&p.line[begin..], currency, 0).unwrap();
            (n, begin + offset)
        } else {
            (total, tot_end)
        };
    
        let mut side_count = 0;
        let mut side_end = main_end;
        let mut side = [0.0, 0.0, 0.0];
        while let Some(i) = p.line[side_end..].find_after("Side ") {
            let pot_end = side_end + i + "pot".len();
            let pot_end = pot_end + if p.line[pot_end..].chars().next().unwrap() == '-' { 3 } else { 1 };
            let (amount, amount_end) = Self::extract_currency(p.line, currency, pot_end).unwrap();
            side_end = amount_end + 1;
            side[side_count] = amount;
            side_count += 1;
        }

        p.advance();
        while p.line.starts_with("Hand was") { 
            p.advance(); 
        }
        while let Some(_) = p.line.find("Board [") {
            p.advance();
        }   

        Some(PotInfo{total, rake, main, side})
    }
    
    fn parse_summary_actions_winners(p: &mut Parser, currency: char) -> Option<(ActionSpan, WinnerSpan)> {
        let actions = p.hands.begin_span(ActionSpan::default());
        let winners = p.hands.begin_span(WinnerSpan::default());
        while p.line.starts_with("Seat ") {
            let line = p.line;
            let name_begin = "Seat ".len() + line["Seat ".len()..].find(':').unwrap() + 2;
    
            // Seat 1: abcd folded
            if let Some(name_end) = line.ends_with_before(" folded") {
                p.hands.actions.push(p.action_no_data(ActionType::Fold, &line[name_begin..name_end]));
            }
            // Seat 1: abcd mucked
            else if let Some(name_end) = line.ends_with_before(" mucked") {
                p.hands.actions.push(p.action_no_data(ActionType::Muck, &line[name_begin..name_end]));
            }
            // Seat 1: abcd (button) folded before Flop (didn't bet)
            // Seat 1: abcd (button) folded before Flop
            // Seat 1: abcd (button) folded on the Flop
            // Seat 1: abcd (button) folded on the River
            // Seat 1: abcd (button) folded on the Turn
            else if line.ends_with("n't bet)")
                 || line.ends_with("re Flop") 
                 || line.ends_with("he Flop") 
                 || line.ends_with("he Turn") 
                 || line.ends_with("he River") 
            {
                let name_end = line[name_begin..].find(" folded ").unwrap();
                let name = Self::parse_summary_result_player_name(p, &line[name_begin..], name_end);
                p.hands.actions.push(p.action_no_data(ActionType::Fold, name));
            }
            // Seat 1: abcd showed [Tc Kc] and won ($3097.0)
            // Seat 1: abcd (button) showed [Kh 9c] and won ($1.19) with three of a kind, Sevens
            else if let Some(i) = line[name_begin..].find("wed [") {
                let name_end = i - 4;
                let cards_begin = i + 4;
                let name = Self::parse_summary_result_player_name(p, &line[name_begin..], name_end);
                let (cards, (_, cards_end)) = find_cards(&line[cards_begin..]);
                let a = p.action_cards(ActionType::Show, name, cards);
                Self::parse_summary_winners(p, &line[cards_begin+cards_end..], a.player_id, currency);
                p.hands.actions.push(a);
            }
            // Seat 1: abcd mucked [9s 9h]
            else if let Some(i) = line[name_begin..].rfind("ked [") {
                let name_end = i - 4;
                let cards_begin = i + 4;
                let name = Self::parse_summary_result_player_name(p, &line[name_begin..], name_end);
                let (cards, _) = find_cards(&line[cards_begin..]);
                let a = p.action_cards(ActionType::Muck, name, cards);
                p.hands.actions.push(a);
            }
            // Seat 1: abcd (button) collected ($4.51)
            else {
                let amount_begin = line.rfind('(').unwrap() + 1;
                let name_end = amount_begin - name_begin - " collected (".len();
                let (amount, _) = Self::find_currency(&line[amount_begin..], currency).unwrap();
                let name = Self::parse_summary_result_player_name(p, &line[name_begin..], name_end);
                let a = p.action_num(ActionType::CollectMainPot, name, amount);
                p.hands.winners.push(Winner{player_id: a.player_id, amount, game_id: 0});
                p.hands.actions.push(a);
            }
    
            p.advance();
        }
        if p.line.is_empty() || p.eof() {
            Some((p.hands.end_span(actions), p.hands.end_span(winners)))
        } else {
            None
        }
    }
    
    fn parse_summary_winners(p: &mut Parser, part: &str, player_id: u8, currency: char) {
        // Seat 1: abcd showed [Tc Kc] and won ($3097.0)
        // Seat 1: abcd (big blind) showed [Ac 5c] and won ($1.19) with a pair of Fives
        // Seat 1: abcd (button) showed [Jc Jd] and won ($46.95) with four of a kind, Jacks, and won ($46.94) with four of a kind, Jacks
        let mut did_win = false;
        let mut game_id = 0;
        for word in part.split(' ') {
            match word {
                "won" => {
                    p.hands.winners.push(Winner{amount: 0.0, player_id, game_id});
                    game_id += 1;
                    did_win = true;
                }
                "lost" => {
                    game_id += 1;
                    did_win = false;
                }
                _ => {
                    if did_win && word.starts_with('(') {
                        p.hands.winners.last_mut().unwrap().amount = Self::find_currency(&word[1..], currency).unwrap().0;
                    }
                    did_win = false;
                }
            }
        }
    }
}


pub trait ParseHeaderPokerStars {
    fn parse_header_hand_info(p: &mut Parser, h: &mut Header) -> Option<()>;
    fn parse_header_table_info(p: &mut Parser, h: &mut Header) -> Option<()>;
}

pub trait ParseHeaderPlayersPokerStars: ParseCurrency + ParseTrimPlayerName {
    fn parse_header_players(p: &mut Parser, header: &mut Header) -> Option<()> {
        while p.line.starts_with("Seat ") {
            let (seat_range, player_name, rest_begin) = parse_seat_name(p.line)?;
            let seat = str::parse::<u8>(&p.line[seat_range]).unwrap();
            let chips = Self::extract_currency(p.line, header.currency, rest_begin)?.0;
            let id = p.add_player(Self::trim_player_name(player_name), seat, chips);
            if seat == header.dealer { header.dealer = id; }
            p.advance();
        }
        Some(())
    }
}

impl<T> ParseHeader for T where T: ParseHeaderPokerStars + ParseHeaderPlayersPokerStars + ParseActionList {
    fn parse_header(p: &mut Parser) -> Option<Header> { 
        let mut h = Header::default();
        Self::parse_header_hand_info(p, &mut h)?;
        Self::parse_header_table_info(p, &mut h)?;
        Self::parse_header_players(p, &mut h)?;
        h.actions = Self::parse_action_list_header(p, h.currency)?;
        Some(h)
    }
}


pub trait ParseActionPokerStars: ParseCurrency + ParseTrimPlayerName {
    // toyochan: sits out
    // toyochan: is sitting out
    // toyochan is connected
    // toyochan is disconnected
    // toyochan leaves the table
    // toyochan has returned
    // toyochan has timed out
    // toyochan has timed out while disconnected
    // toyochan has timed out while being disconnected
    // toyochan was removed from the table for failing to post
    // toyochan will be allowed to play after the button
    #[inline(always)]
    fn parse_action_join_leave_timeout_etc_no_data(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            parse_action_suffix_only!(ActionType::Sitout,        "s out",                    ": sits out"),
            parse_action_suffix_only!(ActionType::Sitout,        "g out",                    ": is sitting out"),
            parse_action_suffix_only!(ActionType::Leave,         "med out",                  " has timed out"),
            parse_action_suffix_only!(ActionType::Join,          "s connected",              " is connected", ActionData::new_handle(SEAT_INITIAL as u32)),
            parse_action_suffix_only!(ActionType::Leave,         "s disconnected",           " is disconnected"),
            parse_action_suffix_only!(ActionType::Leave,         "e disconnected",           " has timed out while disconnected"),
            parse_action_suffix_only!(ActionType::Leave,         "g disconnected",           " has timed out while being disconnected"),
            parse_action_suffix_only!(ActionType::Leave,         "e table",                  " leaves the table"),
            parse_action_suffix_only!(ActionType::Leave,         "g to post",                " was removed from the table for failing to post"),
            parse_action_suffix_only!(ActionType::Join,          "e button",                 " will be allowed to play after the button", ActionData::new_handle(SEAT_AFTER_DEALER as u32)),
            parse_action_suffix_only!(ActionType::Join,          "s returned",               " has returned", ActionData::new_handle(SEAT_INITIAL as u32)),
        )
    }

    // toyochan: checks
    // toyochan: folds
    // toyochan: mucks hand
    // toyochan: doesn't show hand
    #[inline(always)]
    fn parse_action_fold_check_not_show_no_data(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            parse_action_suffix_only!(ActionType::Fold,          ": folds",                  ": folds"),
            parse_action_suffix_only!(ActionType::Check,         ": checks",                 ": checks"),
            parse_action_suffix_only!(ActionType::Fold,          "s hand",                   ": mucks hand"),
            parse_action_suffix_only!(ActionType::Muck,          "w hand",                   ": doesn't show hand"),
        )
    }

    // toyochan: folds [Qh]
    // toyochan: shows [Qh]
    #[inline(always)]
    fn parse_action_fold_show(p: &mut Parser, _: char) -> Option<Action> {
        if !p.line.ends_with(']') { return None; }
        let cards_begin = p.line.rfind('[').unwrap() + 1;
        let cards = parse_cards(&p.line[cards_begin..p.line.len()-1]);
        let cmd_begin = cards_begin - "folds [".len();
        let cmd = p.line[cmd_begin..cmd_begin+1].chars().next().unwrap();
        let name = &p.line[..cards_begin - ": folds [".len()];
        let kind = if cmd == 's' { ActionType::Show } else { ActionType::Fold };
        Some(p.action_cards(kind, Self::trim_player_name(name), cards))
    }
        
    // toyochan said, "ANYTHING"
    #[inline(always)]
    fn parse_action_say(p: &mut Parser, _: char) -> Option<Action> {
        if !p.line.ends_with('"') { return None; }
        let msg_begin = p.line.find('"').unwrap() + 1;
        let name = p.player_id(&p.line[..msg_begin - " said, '".len()]);
        let m = &p.line[msg_begin..p.line.len() - 1];
        let msg = p.push_str(&m[..std::cmp::min(255, m.len())]);
        let msg = Span::new(msg.begin() - p.src_offset, msg.size());
        Some(Action::new(ActionType::Say, name, ActionData::new_message(msg)))
    }

    // toyochan joins the table at seat #6
    #[inline(always)]
    fn parse_action_join(p: &mut Parser, _: char) -> Option<Action> { 
        let name = &p.line[..p.line.find(" joins ")?];
        let seat_begin = p.line.rfind('#').unwrap() + 1;
        let seat = Self::parse_integer(&p.line[seat_begin..]).unwrap().0;
        let player_id = p.player_id(name);
        p.player_mut(player_id).seat = seat as u8;
        Some(Action::new(ActionType::Join, player_id, ActionData::new_handle(seat as u32)))
    }

    // toyochan collected $14.81 from pot
    // toyochan collected $14.81 from main pot
    // toyochan collected $14.81 from side pot
    // toyochan collected $14.81 from side pot-1
    #[inline(always)]
    fn parse_action_collected_pot<const PARSE_SIDE_POT: bool>(p: &mut Parser, currency: char) -> Option<Action> {
        let (line, side_t) = if PARSE_SIDE_POT {
            let pot1 = p.line.ends_with("pot-1");
            let pot2 = p.line.ends_with("pot-2");
            if !pot1 && !pot2 { return None; }
            (&p.line[..p.line.len()-2], if pot1 { ActionType::CollectSidePot1 } else { ActionType::CollectSidePot2 })
        } else {
            if !p.line.ends_with("pot") { return None; }
            (p.line, ActionType::CollectSidePot1)
        };
        let (t, currency_end) = match line[line.len()-"x pot".len()..].chars().next().unwrap() {
            'm'         => (ActionType::CollectMainPot, line.len() - " from pot".len()),
            'n'         => (ActionType::CollectMainPot, line.len() - " from main pot".len()),
            'e'         => (side_t,                     line.len() - " from side pot".len()),
             _ => unreachable!(),
        };
        let (amount, (currency_begin, _)) = Self::rfind_currency(&line[..currency_end], currency).unwrap();
        let name = &line[..currency_begin - " collected ".len()];
        Some(p.action_num(t, Self::trim_player_name(name), amount))
    }
    
    // Uncalled bet ($8.58) returned to toyochan
    #[inline(always)]
    fn parse_action_uncalled_bet_returned(p: &mut Parser, currency: char) -> Option<Action> {
        if !p.line.starts_with("Uncalled ") { return None; }
        let amount = Self::find_currency(&p.line["Uncalled bet (".len()..], currency).unwrap().0;
        let name_begin = p.line.rfind("ed to ").unwrap() + "ed to ".len();
        Some(p.action_num(ActionType::UncalledBetReturned, Self::trim_player_name(&p.line[name_begin..]), amount))
    } 

    // toyochan: shows [Ac 6s] (a pair of Deuces)
    #[inline(always)]
    fn parse_action_show_with_card_description(p: &mut Parser, _: char) -> Option<Action> {
        let (name, rest_begin) = p.line.split_after(": shows")?;
        let cards = find_cards(&p.line[rest_begin + 1..]).0;
        Some(p.action_cards(ActionType::Show, name, cards))
    }

    // toyochan: bets $1.89
    // toyochan: bets $1.89 and is all-in
    // toyochan: calls $1.89
    // toyochan: calls $1.89 and is all-in
    // toyochan: raises $0.70 to $1.20
    // toyochan: raises $0.70 to $1.20 and is all in
    #[inline(always)]
    fn parse_action_bet_call_raise(p: &mut Parser, currency: char) -> Option<Action> {
        for (kinds, suffix) in [
            ([ActionType::Bet, ActionType::BetAllIn], ": bets"), 
            ([ActionType::Call, ActionType::CallAllIn], ": calls"),
            ([ActionType::Raise, ActionType::RaiseAllIn], ": raises")
        ] {
            if let Some((name, rest_begin)) = p.line.rsplit_after(suffix) {
                let bet = Self::find_currency(&p.line[rest_begin+1..], currency).unwrap().0;
                return Some(p.action_num(kinds[p.line.ends_with(" in") as usize], Self::trim_player_name(name), bet))
            }
        }
        None
    }

    // toyochan cashed out the hand for $1 | Cash Out Fee $2
    #[inline(always)]
    fn parse_action_cashout(p: &mut Parser, currency: char) -> Option<Action> {
        let (name, rest_begin) = p.line.split_after(" cashed o")?;
        let amount_begin = rest_begin + "ut the hand for ".len();
        let (amount, (_, currency_end)) = Self::find_currency(&p.line[amount_begin..], currency).unwrap();
        let fee = if let Some(i) = p.line[amount_begin + currency_end..].rfind_after(" Fee ") {
            Self::find_currency(&p.line[amount_begin + currency_end + i..], currency).unwrap().0
        } else {
            0.0
        };
        Some(p.action_num_pair(ActionType::CashOut, name, amount, fee))
    }
}

impl<T> ParseActionBlind for T where T: ParseActionPokerStars {
    
    // toyochan: posts small blind $0.25
    // toyochan: posts big blind $0.50
    // toyochan: posts small & big blinds $0.50
    // toyochan: posts the ante $0.50
    #[inline(always)]
    fn parse_action_blind(p: &mut Parser, currency: char) -> Option<Action> {
        let (name, rest_begin) = p.line.split_after(": posts")?;
        let (amount, (amount_begin, _)) = Self::rfind_currency(p.line, currency).unwrap();
        let blind = &p.line[rest_begin+1..amount_begin-1];
        let t = if blind.ends_with('s') {
            ActionType::BigSmallBlind
        } else {
            match blind.chars().next().unwrap() {
                's' => ActionType::SmallBlind,
                'b' => ActionType::BigBlind,
                't' => ActionType::Ante,
                c => unreachable!("Unexpected character '{}' in blind line: '{}'", c, p.line),
            }
        };
        Some(p.action_num(t, Self::trim_player_name(name), amount))
    }
}

//endregion

//region PokerStars

impl ParseSync for PokerStars {
    fn parse_sync(p: &mut Parser) {
        while !p.eof() && !p.line.starts_with("PokerStars ") {
            p.advance();
        }
    }
}

impl ParseNumber for PokerStars {}

impl ParseTrimPlayerName for PokerStars {}

impl ParseHeaderPlayersPokerStars for PokerStars {}

impl ParsePreFlopActionsOnly for PokerStars {}

impl ParseActionPokerStars for PokerStars {}
 
impl ParseActionList for PokerStars {
    fn is_section_line(line: &str) -> bool { line.starts_with("*** ") }
}


impl ParseHeaderPokerStars for PokerStars {
    fn parse_header_hand_info(p: &mut Parser, h: &mut Header) -> Option<()> {
        let line = p.line;
        
        // PokerStars Hand #208966191428:  Hold'em No Limit ($0.25/$0.50 -  $20 CAP  - USD) - 2020/02/08 4:04:48 ET
        h.site = PokerSite::PokerStars;
        h.dealer = SEAT_NONE;
        h.hero = SEAT_NONE;
        
        let hand_id_begin = "PokerStars Hand #".len();
        let hand_id_end = hand_id_begin + line[hand_id_begin..].find(':')?;
        h.id = p.push_str(&line[hand_id_begin.. hand_id_end]);

        let date_begin = line.rfind('-').unwrap() + 2;
        if date_begin <= hand_id_end { p.advance(); return None; }
    
        let (game_type, bet_type) = Self::parse_game_bet_type(&line[hand_id_end + 2..]);
        h.game_type = game_type;
        h.bet_type = bet_type;

        h.start_date = Self::parse_datetime(&line[date_begin..]);
        
        let buy_in_end = date_begin - 2;
        let buy_in_begin = line[..buy_in_end].rfind('(').unwrap() + 1;
        let (currency, currency_len) = parse_currency_char(&line[buy_in_begin..]).unwrap();
        h.currency = currency;
        let (small_blind, small_blind_end) = Self::parse_float(&line[buy_in_begin+currency_len..]).unwrap();
        h.small_blind = small_blind;
        let (big_blind, (_, big_blind_end)) = Self::find_currency(&line[buy_in_begin+currency_len+small_blind_end+1..], currency).unwrap();
        h.big_blind = big_blind;

        let big_blind_end = buy_in_begin+currency_len+small_blind_end+1+big_blind_end;
        if p.line[big_blind_end..].starts_with(" -") {
            h.bet_cap = Self::find_currency(&line[big_blind_end+3..], currency).unwrap().0;
        }

        p.advance();
        Some(())
    }
    
    fn parse_header_table_info(p: &mut Parser, h: &mut Header) -> Option<()> {
        let line = p.line;
        // Table 'Acamar V' 6-max Seat #1 is the button
        let name_begin = line.find('\'')? + 1;
        let name_end = name_begin + line[name_begin..].find('\'')?;
        h.table_name = p.push_str(&line[name_begin..name_end]);
        let seat_begin = name_end + 2;
    
        let (max_players, max_players_offset) = Self::parse_integer(&line[seat_begin..]).unwrap();
        h.max_players = max_players as u8;
    
        let dealer_seat_begin = seat_begin + max_players_offset + "-max Seat #".len();
        let dealer_seat = Self::parse_integer(&line[dealer_seat_begin..]).unwrap().0;
        h.dealer = dealer_seat as u8;
        
        p.advance();
        Some(())
    }
}

impl PokerStars {
    fn parse_game_bet_type(mut input: &str) -> (GameType, BetType) {
        while input.chars().next().unwrap().is_whitespace() { input = &input[1..]; }
        
        let (game_type, name) = match input.chars().next().unwrap() {
            'H' => (GameType::HoldEm, "Hold'em"),
            'O' => (GameType::Omaha,  "Omaha"),
            c => unreachable!("Unexpected character '{}' while parsing game type in '{}'", c, input),
        };

        let (game_type, name) = if input[name.len() + 1..].chars().next().unwrap() == 'H' {
            (GameType::OmahaHiLo, "Omaha Hi/Lo")
        } else {
            (game_type, name)
        };

        match input[name.len() + 1..].chars().next().unwrap() {
            'N' => (game_type, BetType::NoLimit),
            'L' => (game_type, BetType::Limit),
            'P' => (game_type, BetType::PotLimit),
            _ => unreachable!(),
        }
    }

    fn parse_datetime(input: &str) -> DateTime {
        let year_end = input.find('/').unwrap();
        let month_end = year_end + 1 + input[year_end+1..].find('/').unwrap();
        let day_end = month_end + 1 + input[month_end+1..].find(' ').unwrap();
        let hour_end = day_end + 1 + input[day_end+1..].find(':').unwrap();
        let min_end = hour_end + 1 + input[hour_end+1..].find(':').unwrap();
        let year = Self::parse_integer(&input[..year_end]).unwrap().0 as u32;
        let month = Self::parse_integer(&input[year_end+1..month_end]).unwrap().0 as u32;
        let day = Self::parse_integer(&input[month_end+1..day_end]).unwrap().0 as u32;
        let hour = Self::parse_integer(&input[day_end+1..hour_end]).unwrap().0 as u32;
        let min = Self::parse_integer(&input[hour_end+1..min_end]).unwrap().0 as u32;
        let sec = Self::parse_integer(&input[min_end+1..]).unwrap().0 as u32;
        DateTime::new(year, month, day, hour, min, sec)
    }
}


impl ParseStreet for PokerStars {
    fn is_summary_line(line: &str) -> bool { line.starts_with("*** SU") }

    fn parse_street_header(p: &mut Parser) -> (StreetType, Cards) {
        let line = p.line;
        // *** FLOP *** [4c 8s 5h]
        // *** TURN *** [4c 8s 5h] [6d]
        // *** RIVER *** [4c 8s 5h 6d] [2h]
        // *** SHOW DOWN ***
        // *** SHOWDOWN ***
        let header_name_end = 8 + line[8..].find(" *").unwrap();
        let street_type = match &line[header_name_end-2..header_name_end] {
            "OP" => StreetType::Flop,
            "ER" => StreetType::River,
            "RN" => StreetType::Turn,
            "WN" => StreetType::Showdown,
            _ => unreachable!(),
        };
        let cards = if street_type != StreetType::Showdown {            
            parse_cards(&line[line.rfind('[').unwrap() + 1..line.len() - 1])
        } else {
            Cards::default()
        };
        p.advance();
        (street_type, cards)
    }
}


impl ParseSummaryResultPlayerName for PokerStars {
    fn parse_summary_result_player_name<'a>(_p: &mut Parser, part: &'a str, name_end: usize) -> &'a str {
        // Seat 1: abcd (button)
        // Seat 1: abcd (small blind)
        // Seat 1: abcd (big blind)
        // Seat 1: abcd (small & big blinds)
        if let Some(space) = part[..name_end].rfind(' ') {
            if part[space + 1..].starts_with("(b") || part[space + 1..].starts_with("(s") {
                return &part[..space];
            }
        }
        &part[..name_end]
    }
    
}


impl ParseActionHeader for PokerStars {
    fn parse_action_header(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            Self::parse_action_blind,
            Self::parse_action_join_leave_timeout_etc_no_data,
            Self::parse_action_say,
            Self::parse_action_join,
        )
    }
}

impl ParseActionPreFlop for PokerStars {
    fn parse_action_preflop(p: &mut Parser, currency: char) -> Option<Action> {
        Self::parse_action_street(p, currency)
    }
}

impl ParseActionStreet for PokerStars {
    fn parse_action_street(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            Self::parse_action_fold_check_not_show_no_data,
            Self::parse_action_fold_show,
            Self::parse_action_join_leave_timeout_etc_no_data,
            Self::parse_action_say,
            Self::parse_action_collected_pot::<false>,
            Self::parse_action_uncalled_bet_returned,
            Self::parse_action_bet_call_raise,
            Self::parse_action_show_with_card_description,
            Self::parse_action_cashout,
            Self::parse_action_join,
            Self::parse_action_collected_pot::<true>,
        )
    }
}

//endregion

//region Pluribus

impl ParseSync for PokerStarsPluribus {}

impl ParseNumber for PokerStarsPluribus {}

impl ParseHeaderPlayersPokerStars for PokerStarsPluribus {}

impl ParsePreFlopDealtTo for PokerStarsPluribus {}
impl ParsePreFlopActionsOnly for PokerStarsPluribus {}

impl ParseActionDealtTo for PokerStarsPluribus {}
impl ParseActionPokerStars for PokerStarsPluribus {}
impl ParseActionHeaderBlindOnly for PokerStarsPluribus {}

impl ParseActionList for PokerStarsPluribus {
    fn is_section_line(line: &str) -> bool { PokerStars::is_section_line(line) }
}

impl ParseTrimPlayerName for PokerStarsPluribus {
    fn trim_player_name(name: &str) -> &str {
        &name[if name.starts_with("Mr") { 2 } else { 0 }..]
    }
}


impl ParseHeader for PokerStarsPluribus {
    fn parse_header(p: &mut Parser) -> Option<Header> { 
        let mut h = PokerStars::parse_header(p)?;
        h.site = PokerSite::PokerStarsPluribus;
        Some(h)
    }
}


impl ParseStreet for PokerStarsPluribus {
    fn is_summary_line(line: &str) -> bool { PokerStars::is_summary_line(line) }
    fn parse_street_header(p: &mut Parser) -> (StreetType, Cards) { PokerStars::parse_street_header(p) }
}


impl ParseSummaryResultPlayerName for PokerStarsPluribus {
    fn parse_summary_result_player_name<'a>(_p: &mut Parser, part: &'a str, name_end: usize) -> &'a str {
        Self::trim_player_name(&part[..name_end])
    }
}


impl ParseActionStreet for PokerStarsPluribus {
    fn parse_action_street(p: &mut Parser, currency: char) -> Option<Action> {
        parse_action_lines!(p, currency,
            Self::parse_action_fold_check_not_show_no_data,
            Self::parse_action_fold_show,
            Self::parse_action_collected_pot::<false>,
            Self::parse_action_uncalled_bet_returned,
            Self::parse_action_bet_call_raise,
            Self::parse_action_collected_pot::<true>,
        )
    }
}

//endregion

//region Tests

#[cfg(test)]
pub mod tests {
    use super::*;

    macro_rules! test_parse {
        ($p:ident, $parse:ident, $src:expr, $r:expr, $f:expr) => {
            let hands = {
                let mut hands = HandVec::default();
                let mut p = Parser::new($src, &mut hands);
                let r = $p::$parse(&mut p, '$').unwrap();
                assert_eq!(r, $r);
                hands
            };
            $f(&hands);
        };

        ($p:ident, $parse:ident, $src:expr, $r:expr) => {
            test_parse!($p, $parse, $src, $r, |h: &HandVec|{});
        };
    }

    macro_rules! test_parse2 {
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
            test_parse2!($p, $parse, $src, $r, |_h: &HandVec|{});
        };
    }

    #[test]
    fn parse_file_pokerstars() {
        let src = std::fs::read_to_string("tests/data/example/pokerstars.txt").unwrap();
        let mut hands = HandVec::default();
        let mut p = Parser::new(&src, &mut hands);
        PokerStars::parse(&mut p);
        assert_eq!(hands.hands.len(), 305);
    }

    #[test]
    fn parse_file_pokerstars_pluribus() {
        let src = std::fs::read_to_string("tests/data/example/pluribus.txt").unwrap();
        let mut hands = HandVec::default();
        let mut p = Parser::new(&src, &mut hands);
        PokerStarsPluribus::parse(&mut p);
        assert_eq!(hands.hands.len(), 88);
    }

    //region Header

    #[test]
    fn parse_header() {
        let src = concat!( 
            "PokerStars Hand #123456789:  Hold'em No Limit ($0.25/$0.50 USD) - 2020/02/08 4:01:19 ET\n",
            "Table 'Acamar V' 6-max Seat #3 is the button\n",
            "Seat 1: a: d ($49.50 in chips)\n",
            "Seat 2: e: h ($50 in chips)\n",
            "Seat 3: i: l ($50.50 in chips)\n",
            "a: d: posts small blind $0.25\n",
            "e: h: posts big blind $0.50\n",
            "*** HOLE CARDS ***\n",
        );
        let mut hands = HandVec::default();
        let mut p = Parser::new(src, &mut hands);
        assert_eq!(
            PokerStars::parse_header(&mut p).unwrap(), 
            Header{
                site: PokerSite::PokerStars, 
                game_type: GameType::HoldEm,
                bet_type: BetType::NoLimit,
                max_players: 6,
                dealer: 2,
                hero: SEAT_NONE,
                small_blind: 0.25,
                big_blind: 0.5,
                currency: '$',
                start_date: DateTime::new(2020, 2, 8, 4, 1, 19),
                actions: ActionSpan::new(0, 2),
                id: Span::new(0, 9),
                table_name: Span::new(9, 8),
                ..Default::default()
            },
        );
        assert_eq!(p.hands.src, "123456789Acamar Va: de: hi: l");
        assert_eq!(3, p.hands.players.len());
        assert_eq!(p.hands.players[0], Player{name: Span::new(17, 4), chips: 49.5, seat: 1});
        assert_eq!(p.hands.players[1], Player{name: Span::new(21, 4), chips: 50.0, seat: 2});
        assert_eq!(p.hands.players[2], Player{name: Span::new(25, 4), chips: 50.5, seat: 3});
    }

    macro_rules! test_parse_header_game_type {
        ($game_type:expr, $bet_type:expr, $game_type_str:literal) => {
            let mut hands = HandVec::default();
            let mut p = Parser::new(concat!( 
                "PokerStars Hand #123456789:  ",
                $game_type_str,
                " ($0.25/$0.50 USD) - 2020/02/08 4:01:19 ET\n",
                "Table 'Acamar V' 6-max Seat #3 is the button\n",
                "Seat 1: a: d ($49.50 in chips)\n",
                "Seat 2: e: h ($50 in chips)\n",
                "a: d: posts small blind $0.25\n",
                "e: h: posts big blind $0.50\n",
                "*** HOLE CARDS ***\n",
            ), &mut hands);
            let h = PokerStars::parse_header(&mut p).unwrap();
            assert_eq!($game_type, h.game_type);
            assert_eq!($bet_type, h.bet_type);
        };
    }

    #[test]
    fn parse_header_game_type() {
        test_parse_header_game_type!(GameType::HoldEm       , BetType::NoLimit,   "Hold'em No Limit");
        test_parse_header_game_type!(GameType::HoldEm       , BetType::Limit,     "Hold'em Limit");
        test_parse_header_game_type!(GameType::HoldEm       , BetType::PotLimit,  "Hold'em Pot Limit");
        test_parse_header_game_type!(GameType::Omaha        , BetType::NoLimit,   "Omaha No Limit");
        test_parse_header_game_type!(GameType::Omaha        , BetType::PotLimit,  "Omaha Pot Limit");
        test_parse_header_game_type!(GameType::OmahaHiLo    , BetType::NoLimit,   "Omaha Hi/Lo No Limit");
        test_parse_header_game_type!(GameType::OmahaHiLo    , BetType::PotLimit,  "Omaha Hi/Lo Pot Limit");
    }

    #[test]
    fn parse_header_bet_cap() {
        let mut hands = HandVec::default();
        let mut p = Parser::new(concat!( 
            "PokerStars Hand #123456789:  Hold'em No Limit ($0.25/$0.50 - $20 Cap -  USD) - 2020/02/08 4:01:19 ET\n",
            "Table 'Acamar V' 6-max Seat #3 is the button\n",
            "Seat 1: a: d ($49.50 in chips)\n",
            "Seat 2: e: h ($50 in chips)\n",
            "a: d: posts small blind $0.25\n",
            "e: h: posts big blind $0.50\n",
            "*** HOLE CARDS ***\n",
        ), &mut hands);
        let h = PokerStars::parse_header(&mut p).unwrap();
        assert_eq!(20.0, h.bet_cap);
    }

    //endregion

    //region PreFlop

    #[test]
    fn preflop() {
        test_parse2!(PokerStars, parse_preflop,
            concat!(
                "*** HOLE CARDS ***\n",
                "a: d: folds\n",
                "*** FLOP *** [Qh Qh Qh]"
            ),
            Street{cards: Cards::default(), id: 0, actions: ActionSpan::new(0, 1)}
        );

        test_parse2!(PokerStarsPluribus, parse_preflop,
            concat!(
                "*** HOLE CARDS ***\n",
                "Dealt to a: d [Qh Td]\n",
                "a: d: folds\n",
                "*** FLOP *** [Qh Qh Qh]"
            ),
            Street{cards: Cards::default(), id: 0, actions: ActionSpan::new(0, 2)},
            |r: &HandVec| {
                assert_eq!(Action::new(ActionType::Dealt, 0, ActionData::new_handle(0)), r.actions[0]);
                assert_eq!(Action::no_data(ActionType::Fold, 0), r.actions[1]);
                assert_eq!(cards!(Qh Td), r.cards[0]);
            }
        );
    }

    //endregion

    //region Streets

    macro_rules! test_parse_streets {
        ($p:ident, $src:expr, $r:expr, $f:expr) => {
            test_parse!($p, parse_streets, $src, $r, $f);
        };

        ($p:ident, $src:expr, $r:expr) => {
            test_parse!($p, parse_streets, $src, $r);
        };
    }

    fn test_street_flop<T: Parse>() {
        test_parse_streets!(T, 
            concat!(
                "*** FLOP *** [Qh Td As]\n",
                "a: d: folds\n",
                "*** SUMMARY ***",
            ),
            (FlopSpan::new(0, 1), TurnSpan::default(), RiverSpan::default(), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(Qh Td As), r.flops[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    fn test_street_turn<T: Parse>() {
        test_parse_streets!(T, 
            concat!(
                "*** TURN *** [Qh Td As] [5c]\n",
                "a: d: folds\n",
                "*** SUMMARY ***",
            ),
            (FlopSpan::default(), TurnSpan::new(0, 1), RiverSpan::default(), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(5c), r.turns[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    fn test_street_river<T: Parse>() {
        test_parse_streets!(T, 
            concat!(
                "*** RIVER *** [Qh Td As 5c] [6c]\n",
                "a: d: folds\n",
                "*** SUMMARY ***",
            ),
            (FlopSpan::default(), TurnSpan::default(), RiverSpan::new(0, 1), ShowdownSpan::default()),
            |r: &HandVec| {
                assert_eq!(cards!(6c), r.rivers[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    fn test_street_showdown<T: Parse>() {
        test_parse_streets!(T, 
            concat!(
                "*** SHOW DOWN ***\n",
                "a: d: folds\n",
                "*** SUMMARY ***",
            ),
            (FlopSpan::default(), TurnSpan::default(), RiverSpan::default(), ShowdownSpan::new(0, 1)),
            |r: &HandVec| {
                assert_eq!(Cards::default(), r.showdowns[0].cards);
                assert_eq!(ActionType::Fold, r.actions[0].kind);
            }
        );
    }

    #[test]
    fn street_flop() {
        test_street_flop::<PokerStars>();
        test_street_flop::<PokerStarsPluribus>();
    }

    #[test]
    fn street_turn() {
        test_street_turn::<PokerStars>();
        test_street_turn::<PokerStarsPluribus>();
    }

    #[test]
    fn street_river() {
        test_street_river::<PokerStars>();
        test_street_river::<PokerStarsPluribus>();
    }

    #[test]
    fn street_showdown() {
        test_street_showdown::<PokerStars>();
        test_street_showdown::<PokerStarsPluribus>();
    }

    //endregion

    //region Summary
    
    fn make_summary_pots(total: Number, main: Number, side: Number, rake: Number) -> Summary {
        Summary{
            pot: PotInfo{total, rake, main, side: [side, 0.0, 0.0]},
            winners: WinnerSpan::default(), 
            actions: ActionSpan::new(0, 1)
        }
    }
    
    fn test_summary_pots<T: Parse>() {
        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            make_summary_pots(1.23, 1.23, 0.0, 0.15)
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake 0\n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            make_summary_pots(1.23, 1.23, 0.0, 0.0)
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | \n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            make_summary_pots(1.23, 1.23, 0.0, 0.0)
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Main pot $1.00. Side pot $0.23. | \n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            make_summary_pots(1.23, 1.00, 0.23, 0.0)
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Main pot $1.00. Side pot-1 $0.12. Side pot-2 $0.11. | \n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, rake: 0.0, main: 1.00, side: [0.12, 0.11, 0.0]},
                winners: WinnerSpan::default(), 
                actions: ActionSpan::new(0, 1)
            }
        );
    }

    fn test_summary_boards<T: Parse>() {
        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Board [Qh Td Jc]\n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::default(), 
                actions: ActionSpan::new(0, 1)
            }
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Hand was run twice\n",
                "FIRST Board [Qh Td Jc]\n",
                "SECOND Board [Jc Td Qh]\n",
                "Seat 1: a: d folded on the Flop\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::default(), 
                actions: ActionSpan::new(0, 1)
            }
        );
    }

    fn test_summary_winners<T: Parse>() {
        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Board [2c Th 7d]\n",
                "Seat 1: a: d folded before Flop (didn't bet)\n",
                "Seat 2: efgh collected ($9.26)\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::new(0, 1),
                actions: ActionSpan::new(0, 2)
            },
            |r: &HandVec| {
                assert_eq!("efgh", &r.src[Span::new(4, 4)]);
                assert_eq!(Winner{player_id: 1, amount: 9.26, game_id: 0}, r.winners[0]);
            }
        );        
        
        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Board [2c Th 7d]\n",
                "Seat 1: a: d folded before Flop (didn't bet)\n",
                "Seat 2: efgh showed [Qh Qd] and won ($9.26) with a pair of Queens\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::new(0, 1),
                actions: ActionSpan::new(0, 2)
            },
            |r: &HandVec| {
                assert_eq!("efgh", &r.src[Span::new(4, 4)]);
                assert_eq!(Winner{player_id: 1, amount: 9.26, game_id: 0}, r.winners[0]);
            }
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Board [2c Th 7d]\n",
                "Seat 1: a: d showed [Jh Jd] and lost with a pair of Jacks\n",
                "Seat 2: efgh showed [Qh Qd] and won ($9.26) with a pair of Queens\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::new(0, 1),
                actions: ActionSpan::new(0, 2)
            },
            |r: &HandVec| {
                assert_eq!("efgh", &r.src[Span::new(4, 4)]);
                assert_eq!(Winner{player_id: 1, amount: 9.26, game_id: 0}, r.winners[0]);
            }
        );

        test_parse2!(T, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "FIRST Board [2c Th 7d]\n",
                "SECOND Board [2c Th 7d]\n",
                "Seat 1: a: d showed [Jh Jd] and lost with a pair of Jacks, and won ($9.26) with a pair of Jacks\n",
                "Seat 2: efgh showed [Qh Qd] and won ($9.36) with a pair of Queens, and lost with a pair of Queens\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::new(0, 2),
                actions: ActionSpan::new(0, 2)
            },
            |r: &HandVec| {
                assert_eq!("a: d", &r.src[Span::new(0, 4)]);
                assert_eq!("efgh", &r.src[Span::new(4, 4)]);
                assert_eq!(Winner{player_id: 0, amount: 9.26, game_id: 1}, r.winners[0]);
                assert_eq!(Winner{player_id: 1, amount: 9.36, game_id: 0}, r.winners[1]);
            }
        ); 
    }

    fn test_summary_actions<T: ParseSummaryPokerStars>() {
        test_parse2!(T, parse_summary_actions_winners,
            "Seat 1: a: d mucked\n",
            (ActionSpan::new(0, 1), WinnerSpan::new(0, 0)),
            |r: &HandVec| {
                assert_eq!(Action::no_data(ActionType::Muck, 0), r.actions[0]);
            }
        );

        test_parse2!(T, parse_summary_actions_winners,
            "Seat 1: a: d mucked [8s 8h]\n",
            (ActionSpan::new(0, 1), WinnerSpan::new(0, 0)),
            |r: &HandVec| {
                assert_eq!(Action::new(ActionType::Muck, 0, ActionData::new_handle(0)), r.actions[0]);
                assert_eq!(cards!(8s 8h), r.cards[0]);
            }
        );

        test_parse2!(T, parse_summary_actions_winners,
            "Seat 1: a: d folded before Flop (didn't bet)\n",
            (ActionSpan::new(0, 1), WinnerSpan::new(0, 0)),
            |r: &HandVec| {
                assert_eq!(Action::no_data(ActionType::Fold, 0), r.actions[0]);
            }
        );

        test_parse2!(T, parse_summary_actions_winners,
            "Seat 1: a: d showed [Kh Kc] and won ($51.40) with two pair, Kings and Fours\n",
            (ActionSpan::new(0, 1), WinnerSpan::new(0, 1)),
            |r: &HandVec| {
                assert_eq!(Action::new(ActionType::Show, 0, ActionData::new_handle(0)), r.actions[0]);
                assert_eq!(cards!(Kh Kc), r.cards[0]);
            }
        );
    }

    #[test]
    fn summary_pots() {
        test_summary_pots::<PokerStars>();
        test_summary_pots::<PokerStarsPluribus>();
    }

    #[test]
    fn summary_boards() {
        test_summary_boards::<PokerStars>();
        test_summary_boards::<PokerStarsPluribus>();
    }

    #[test]
    fn summary_winners() {
        test_summary_winners::<PokerStars>();
        test_summary_winners::<PokerStarsPluribus>();

        test_parse2!(PokerStars, parse_summary,
            concat!(
                "*** SUMMARY ***\n",
                "Total pot $1.23 | Rake $0.15\n",
                "Board [2c Th 7d]\n",
                "Seat 1: a: d folded before Flop (didn't bet)\n",
                "Seat 2: efgh (big blind) collected ($9.26)\n",
            ),
            Summary{
                pot: PotInfo{total: 1.23, main: 1.23, side: [0.0, 0.0, 0.0], rake: 0.15},
                winners: WinnerSpan::new(0, 1),
                actions: ActionSpan::new(0, 2)
            },
            |r: &HandVec| {
                assert_eq!("efgh", &r.src[Span::new(4, 4)]);
                assert_eq!(Winner{player_id: 1, amount: 9.26, game_id: 0}, r.winners[0]);
            }
        );
    }

    #[test]
    fn summary_actions() {
        test_summary_actions::<PokerStars>();
        test_summary_actions::<PokerStarsPluribus>();

        for src in [
            "Seat 1: a: d (button) mucked\n",
            "Seat 1: a: d (big blind) mucked\n",
            "Seat 1: a: d (small blind) mucked\n",
            "Seat 1: a: d (button blind) mucked\n",
        ] {
            test_parse2!(PokerStars, parse_summary_actions_winners,
                src,
                (ActionSpan::new(0, 1), WinnerSpan::new(0, 0)),
                |r: &HandVec| {
                    assert_eq!(Action::no_data(ActionType::Muck, 0), r.actions[0]);
                }
            );
    
        }
    }

    //endregion

    //region Action

    macro_rules! test_parse_action_suffix_only {
        ($p:ident, $parse:ident, $player_id:expr, $($line:literal => $kind:expr),*) => {
            $(
                test_parse2!($p, $parse, $line, Action::no_data($kind, $player_id));
            )*
        };
        
        ($p:ident, $parse:ident, $player_id:expr, $($line:literal => $kind:expr,)*) => {
            test_parse_action_suffix_only!($p, $parse, $player_id, $($line=>$kind),*)
        };
    }

    fn test_action_check<T: ParseAction>() {
        test_parse_action_suffix_only!(T, parse_action_street, 0, 
            "a: d: checks" => ActionType::Check
        );
    }

    fn test_action_not_show<T: ParseAction>() {
        test_parse_action_suffix_only!(T, parse_action_street, 0, 
            "a: d: doesn't show hand" => ActionType::Muck
        );
    }
    
    fn test_action_fold<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "a: d: folds",
            Action::no_data(ActionType::Fold, 0)
        );
        test_parse2!(T, parse_action_street,
            "a: d: mucks hand",
            Action::no_data(ActionType::Fold, 0)
        );
        test_parse2!(T, parse_action_street,
            "a: d: folds [Qh]",
            Action::new(ActionType::Fold, 0, ActionData::new_handle(0)),
            |r: &HandVec| {
                assert_eq!(cards!(Qh), r.cards[0]);
            }
        );
    }

    fn test_action_show<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "a: d: shows [Qh]",
            Action::new(ActionType::Show, 0, ActionData::new_handle(0)),
            |r: &HandVec| {
                assert_eq!(cards!(Qh), r.cards[0]);
            }
        );
    }
    
    fn test_action_collected_pot<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "a: d collected $1.23 from pot",
            Action::new(ActionType::CollectMainPot, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d collected $1.23 from main pot",
            Action::new(ActionType::CollectMainPot, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d collected $1.23 from side pot",
            Action::new(ActionType::CollectSidePot1, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d collected $1.23 from side pot-2",
            Action::new(ActionType::CollectSidePot2, 0, ActionData::new_num(1.23))
        );
    }

    fn test_action_uncalled_bet_returned<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "Uncalled bet ($1.23) returned to a: d",
            Action::new(ActionType::UncalledBetReturned, 0, ActionData::new_num(1.23))
        );
    }

    fn test_action_bet_call<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "a: d: bets $1.23",
            Action::new(ActionType::Bet, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d: bets $1.23 and is all in",
            Action::new(ActionType::BetAllIn, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d: calls $1.23",
            Action::new(ActionType::Call, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d: calls $1.23 and is all in",
            Action::new(ActionType::CallAllIn, 0, ActionData::new_num(1.23))
        );
    }

    fn test_action_raise<T: ParseAction>() {
        test_parse2!(T, parse_action_street,
            "a: d: raises $1.23 to $1.24",
            Action::new(ActionType::Raise, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_street,
            "a: d: raises $1.23 to $1.24 and is all in",
            Action::new(ActionType::RaiseAllIn, 0, ActionData::new_num(1.23))
        );
    }

    fn test_action_blind<T: ParseAction>() {
        test_parse2!(T, parse_action_header,
            "a: d: posts small blind $1.23",
            Action::new(ActionType::SmallBlind, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_header,
            "a: d: posts big blind $1.23",
            Action::new(ActionType::BigBlind, 0, ActionData::new_num(1.23))
        );
        test_parse2!(T, parse_action_header,
            "a: d: posts small & big blinds $1.23",
            Action::new(ActionType::BigSmallBlind, 0, ActionData::new_num(1.23))
        );
    }

    #[test]
    fn action_check() {
        test_action_check::<PokerStars>();
        test_action_check::<PokerStarsPluribus>();
    }

    #[test]
    fn action_not_show() {
        test_action_not_show::<PokerStars>();
        test_action_not_show::<PokerStarsPluribus>();
    }

    #[test]
    fn action_fold() {
        test_action_fold::<PokerStars>();
        test_action_fold::<PokerStarsPluribus>();
    }

    #[test]
    fn action_show() {
        test_action_show::<PokerStars>();
        test_action_show::<PokerStarsPluribus>();

        test_parse2!(PokerStars, parse_action_street,
            "a: d: shows [Qh] (a Queen of Hearts)",
            Action::new(ActionType::Show, 0, ActionData::new_handle(0)),
            |r: &HandVec| {
                assert_eq!(cards!(Qh), r.cards[0]);
            }
        );
    }

    #[test]
    fn action_collected_pot() {
        test_action_collected_pot::<PokerStars>();
        test_action_collected_pot::<PokerStarsPluribus>();
    }

    #[test]
    fn action_uncalled_bet_returned() {
        test_action_uncalled_bet_returned::<PokerStars>();
        test_action_uncalled_bet_returned::<PokerStarsPluribus>();
    }

    #[test]
    fn action_bet_call() {
        test_action_bet_call::<PokerStars>();
        test_action_bet_call::<PokerStarsPluribus>();
    }

    #[test]
    fn action_raise() {
        test_action_raise::<PokerStars>();
        test_action_raise::<PokerStarsPluribus>();
    }

    #[test]
    fn action_blind() {
        test_action_blind::<PokerStars>();
        test_action_blind::<PokerStarsPluribus>();
        
        test_parse2!(PokerStars, parse_action_header,
            "a: d: posts the ante $1.23",
            Action::new(ActionType::Ante, 0, ActionData::new_num(1.23))
        );
    }

    #[test]
    fn action_say() {
        test_parse2!(PokerStars, parse_action_header,
            "a: d said, \"hello\"",
            Action::new(ActionType::Say, 0, ActionData::new_message(Span::new(8, 5))),
            |r: &HandVec| {
                assert_eq!(r.src, "a: defghhello");
            }
        );
    }

    #[test]
    fn action_sit_out() {
        test_parse_action_suffix_only!(PokerStars, parse_action_header, 0, 
            "a: d: sits out" => ActionType::Sitout,
            "a: d: is sitting out" => ActionType::Sitout,
        );
    }
    
    #[test]
    fn action_connect_disconnect() {
        test_parse_action_suffix_only!(PokerStars, parse_action_header, 0, 
            "a: d is disconnected" => ActionType::Leave,
        );
        test_parse2!(PokerStars, parse_action_header,
            "a: d is connected",
            Action::new(ActionType::Join, 0, ActionData::new_handle(SEAT_INITIAL as u32))
        );
    }

    #[test]
    fn action_timeout() {
        test_parse_action_suffix_only!(PokerStars, parse_action_header, 0, 
            "a: d has timed out" => ActionType::Leave,
            "a: d has timed out while disconnected" => ActionType::Leave,
            "a: d has timed out while being disconnected" => ActionType::Leave,
            "a: d was removed from the table for failing to post" => ActionType::Leave,
        );
    }

    #[test]
    fn action_join() {
        test_parse2!(PokerStars, parse_action_header,
            "a: d will be allowed to play after the button",
            Action::new(ActionType::Join, 0, ActionData::new_handle(SEAT_AFTER_DEALER as u32))
        );
        test_parse2!(PokerStars, parse_action_header,
            "a: d joins the table at seat #6",
            Action::new(ActionType::Join, 0, ActionData::new_handle(6))
        );
        test_parse2!(PokerStars, parse_action_header,
            "a: d has returned",
            Action::new(ActionType::Join, 0, ActionData::new_handle(SEAT_INITIAL as u32))
        );
    }

    #[test]
    fn action_cashout() {
        // toyochan cashed out the hand for $1 | Cash Out Fee $2
        test_parse2!(PokerStars, parse_action_street,
            "a: d cashed out the hand for $1.23 | Cash Out Fee $1.24",
            Action::new(ActionType::CashOut, 0, ActionData::new_handle(0)),
            |r: &HandVec| {
                assert_eq!(1.23, r.nums[0]);
                assert_eq!(1.24, r.nums[1]);
            }
        );
        test_parse2!(PokerStars, parse_action_street,
            "a: d cashed out the hand for $1.23 | ",
            Action::new(ActionType::CashOut, 0, ActionData::new_handle(0)),
            |r: &HandVec| {
                assert_eq!(1.23, r.nums[0]);
                assert_eq!(0.0, r.nums[1]);
            }
        );
    }

    //endregion

}

//endregion
