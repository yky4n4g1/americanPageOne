def normal_mutch_card(card, field_card):
    return card.suit == field_card.suit or card.rank == field_card.rank or card.rank == 7


def rank_mutch_card(card, field_card):
    return card.rank == field_card.rank
