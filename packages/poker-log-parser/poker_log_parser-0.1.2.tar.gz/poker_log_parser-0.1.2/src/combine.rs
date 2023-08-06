use crate::pklp::*;
use rayon::prelude::*;


impl HandVec {
    // TODO: Sort hands in parallel

    pub fn sort(&mut self) {
        unimplemented!("Sort HandVec");
    }

    pub fn combine(mut vecs: Vec<HandVec>) -> HandVec {
        assert!(vecs.len() >= 1);
        if vecs.len() == 1 { return vecs.pop().unwrap(); }
        let n = vecs.len() - 1;
        let mut cur = ConcatOffsets::default();
        let mut offsets = Vec::with_capacity(vecs.len());
        // This must be sequential
        Self::combine_begin(&mut cur, &vecs[n]);
        for v in &vecs[..n] { 
            offsets.push(Self::combine_begin(&mut cur, v)); 
        }
        // This is embarassingly parallel
        vecs[..n].par_iter_mut()
            .enumerate()
            .for_each(|(i, v)| v.combine_update(&offsets[i]));
        
        // Initial resizes must be sequential, then copies can be done in parallel
        let mut v = vecs.pop().unwrap();
        for o in vecs.into_iter() {
            unsafe { v.src.as_mut_vec().extend(o.src.bytes().into_iter()) }
            v.hands.extend(o.hands);
            v.players.extend(o.players);
            v.winners.extend(o.winners);
            v.nums.extend(o.nums);
            v.cards.extend(o.cards);
            v.actions.extend(o.actions);
            v.flops.extend(o.flops);
            v.turns.extend(o.turns);
            v.rivers.extend(o.rivers);
            v.showdowns.extend(o.showdowns);
        }

        // let mut v = HandVec::default();
        // v.hands.resize(cur.hands_offset, Hand::default());
        // vecs.into_par_iter()
        //     .enumerate()
        //     .for_each(|(i, o)| {
        //         v.hands[offsets[i].hands_offset..offsets[i].hands_offset + o.hands.len()].copy_from_slice(&o.hands);
        //         v.players[offsets[i].players_offset..offsets[i].players_offset + o.players.len()].copy_from_slice(&o.players);
        //         v.winners[offsets[i].winners_offset..offsets[i].winners_offset + o.winners.len()].copy_from_slice(&o.winners);
        //         v.nums[offsets[i].nums_offset..offsets[i].nums_offset + o.nums.len()].copy_from_slice(&o.nums);
        //         v.cards[offsets[i].cards_offset..offsets[i].cards_offset + o.cards.len()].copy_from_slice(&o.cards);
        //         v.actions[offsets[i].actions_offset..offsets[i].actions_offset + o.actions.len()].copy_from_slice(&o.actions);
        //         v.flops[offsets[i].flops_offset..offsets[i].flops_offset + o.flops.len()].copy_from_slice(&o.flops);
        //         v.turns[offsets[i].turns_offset..offsets[i].turns_offset + o.turns.len()].copy_from_slice(&o.turns);
        //         v.rivers[offsets[i].rivers_offset..offsets[i].rivers_offset + o.rivers.len()].copy_from_slice(&o.rivers);
        //         v.showdowns[offsets[i].showdowns_offset..offsets[i].showdowns_offset + o.showdowns.len()].copy_from_slice(&o.showdowns);
        //     });

        v
    }
}


#[derive(Default)]
struct ConcatOffsets {
    src_offset: usize,
    hands_offset: usize,
    players_offset: usize,
    winners_offset: usize,
    nums_offset: usize,
    cards_offset: usize,
    actions_offset: usize,
    flops_offset: usize,
    turns_offset: usize,
    rivers_offset: usize,
    showdowns_offset: usize,
}

macro_rules! replace_actions {
    ($self:expr, $hand:expr, $actions:expr, $offsets:expr) => {
        $self.replace_action_data($hand, $actions, $offsets.src_offset, $offsets.nums_offset, $offsets.cards_offset);
        Self::replace_span(&mut $actions, $offsets.actions_offset);
    };
}

impl HandVec {
    fn combine_begin(cur: &mut ConcatOffsets, o: &HandVec) -> ConcatOffsets {
        let off = ConcatOffsets{
            src_offset: cur.src_offset,
            hands_offset: cur.hands_offset,
            players_offset: cur.players_offset,
            winners_offset: cur.winners_offset,
            nums_offset: cur.nums_offset,
            cards_offset: cur.cards_offset,
            actions_offset: cur.actions_offset,
            flops_offset: cur.flops_offset,
            turns_offset: cur.turns_offset,
            rivers_offset: cur.rivers_offset,
            showdowns_offset: cur.showdowns_offset,
        };

        cur.src_offset += o.src.len();
        cur.hands_offset += o.hands.len();
        cur.players_offset += o.players.len();
        cur.winners_offset += o.winners.len();
        cur.nums_offset += o.nums.len();
        cur.cards_offset += o.cards.len();
        cur.actions_offset += o.actions.len();
        cur.flops_offset += o.flops.len();
        cur.turns_offset += o.turns.len();
        cur.rivers_offset += o.rivers.len();
        cur.showdowns_offset += o.showdowns.len();

        off
    }

    fn combine_update(&mut self, o: &ConcatOffsets) {
        for i in 0..self.hands.len() {
            self.hands[i].src_offset += o.src_offset;

            Self::replace_str(&mut self.hands[i].header.id, o.src_offset);
            Self::replace_str(&mut self.hands[i].header.table_name, o.src_offset);
            for j in 0..self.hands[i].header.players.size() {
                Self::replace_str(&mut self.players[self.hands[i].header.players.begin() + j].name, o.src_offset);
            }
            Self::replace_span(&mut self.hands[i].header.players, o.players_offset);
            replace_actions!(self, i, self.hands[i].header.actions, o);
            
            replace_actions!(self, i, self.hands[i].preflop.actions, o);

            Self::replace_span(&mut self.hands[i].summary.winners, o.winners_offset);
            replace_actions!(self, i, self.hands[i].summary.actions, o);
            
            let mut flops = self.hands[i].flops();
            for j in 0..flops.size() { replace_actions!(self, i, self[flops][j].actions, o); }
            Self::replace_span(&mut flops, o.flops_offset);

            let mut turns = self.hands[i].turns();
            for j in 0..turns.size() { replace_actions!(self, i, self[turns][j].actions, o); }
            Self::replace_span(&mut turns, o.turns_offset);

            let mut rivers = self.hands[i].rivers();
            for j in 0..rivers.size() { replace_actions!(self, i, self[rivers][j].actions, o); }
            Self::replace_span(&mut rivers, o.rivers_offset);

            let mut showdowns = self.hands[i].showdowns();
            for j in 0..showdowns.size() { replace_actions!(self, i, self[showdowns][j].actions, o); }
            Self::replace_span(&mut showdowns, o.showdowns_offset);

            self.hands[i].streets = (flops, turns, rivers, showdowns);
        }
    }

    fn replace_str(s: &mut Span, offset: usize) {
        *s = Span::new(s.begin() + offset, s.size())
    }

    fn replace_span<T: SpanLike>(s: &mut T, offset: usize) {
        *s = T::new(s.begin() + offset, s.size())
    }
    
    fn replace_action_data(&mut self, hand: usize, actions: ActionSpan, src_offset: usize, nums_offset: usize, cards_offset: usize) {
        for a in &mut self[actions] {
            if a.kind.can_have_cards() && a.data != ActionData::invalid() {
                a.data = ActionData::new_handle(a.data.handle() + cards_offset as u32);
            }
            else if a.kind == ActionType::Say {
                let mut span = a.data.message_span(hand);
                Self::replace_str(&mut span, src_offset);
                a.data = ActionData::new_message(span);
            }
            else if a.kind == ActionType::CashOut {
                a.data = ActionData::new_handle(a.data.handle() + nums_offset as u32);
            }
        }
    }
}


mod tests {
    use super::*;

    fn make_hand_vec(index: usize) -> HandVec {
        let mut h = HandVec::default();
        let mut hand = Hand::default();
        
        // Info
        hand.header.currency = '$';
        hand.header.max_players = 2;
        hand.header.id = h.push_str(&format!("Id{}", index));
        hand.header.table_name = h.push_str(&format!("Name{}", index));
        let p1 = h.push_str(&format!("abcd{}", index));
        let p2 = h.push_str(&format!("efgh{}", index));
        
        // Players
        h.players.push(Player{name: p1, seat: 1, chips: 1.0});
        h.players.push(Player{name: p2, seat: 2, chips: 1.0});
        hand.header.players = PlayerSpan::new(0, 2);

        // Action
        h.actions.push(Action::no_data(ActionType::Fold, 0));
        hand.header.actions = ActionSpan::new(0, 1);

        // All Action types
        h.cards.push(cards!(Qh));
        h.actions.push(Action::new(ActionType::Fold, 0, ActionData::new_handle(0)));

        let msg = h.push_str(&format!("Message{}", index));
        h.actions.push(Action::new(ActionType::Say, 0, ActionData::new_message(msg)));

        h.nums.push(1.23 + index as Number);
        h.nums.push(1.24 + index as Number);
        h.actions.push(Action::new(ActionType::CashOut, 0, ActionData::new_handle(0)));

        hand.preflop.actions = ActionSpan::new(1, 3);

        // Summary
        h.winners.push(Winner{player_id: 0, game_id: 0, amount: 10.0});
        hand.summary.winners = WinnerSpan::new(0, 1);

        h.hands.push(hand);
        h
    }

    #[test]
    fn combine_hand_vec() {
        let c = HandVec::combine(vec![make_hand_vec(0), make_hand_vec(1)]);

        assert_eq!(2, c.hands.len());
        assert_eq!(8, c.actions.len());
        assert_eq!(4, c.players.len());
        assert_eq!(2, c.winners.len());
        assert_eq!(4, c.nums.len());
        assert_eq!(2, c.cards.len());

        assert_eq!("Id0", &c.src[c.hands[1].header.id]);
        assert_eq!("Name0", &c.src[c.hands[1].header.table_name]);

        assert_eq!("Id1", &c.src[c.hands[0].header.id]);
        assert_eq!("Name1", &c.src[c.hands[0].header.table_name]);

        
        assert_eq!("abcd0", &c.src[c[c.hands[1].header.players][0].name]);
        assert_eq!("efgh0", &c.src[c[c.hands[1].header.players][1].name]);
        
        assert_eq!("abcd1", &c.src[c[c.hands[0].header.players][0].name]);
        assert_eq!("efgh1", &c.src[c[c.hands[0].header.players][1].name]);
    }
}