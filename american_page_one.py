import random

from trump import Deck, Card, FieldCard
from player import Player, CpuPlayer
from func import normal_mutch_card, rank_mutch_card


class AmericanPageOne:
    """
    アメリカンページワンのゲームデータや関数を持つ

    Attributes
    ----------
    players:list of player.Player, player.CpuPlayer
        ゲームに参加しているプレイヤーを格納するリスト

    deck:trump.Deck
        山札にあるカードを格納するリスト

    turn_player_index:int
        現在のターンプレイヤーの添字

    game_flag:bool
        ゲームの継続のフラグ

    flag_2:int
        2のランクのカードが何枚連続で出たかを持つ

    flag_3:int
        上の3のランクのもの

    flag_j:bool
        ターンを飛ばすかを判別する

    flag_q:int
        ターン順の制御、0:正順 ,1:逆順

    field_cards:list of trump.Card
        捨て札を格納した配列
    """

    def __init__(self, player_num):

        init_hand = 5  # 初期手札

        # プレイヤー処理
        self.players = [CpuPlayer('CPU ' + str(i))
                        for i in range(player_num - 1)]
        self.players.append(Player(input("名前を入力：")))
        random.shuffle(self.players)

        # デッキ処理
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.hands = [self.deck.pull()
                            for i in range(init_hand)]
        self.turn_player_index = 0
        self.game_flag = True  # gameの継続フラグ
        self.flag_2 = 0
        self.flag_3 = 0
        self.flag_j = False
        self.flag_q = 0
        self.field_cards = [self.deck.pull()]
        while self.field_cards[0].rank in [1, 2, 7, 10, 11]:
            self.field_cards.insert(0, self.deck.pull())
        self.update_field_card()

    def update_field_card(self):
        card = self.field_cards[0]
        self.field_card = FieldCard(card)
        self.card_effect()

    def card_effect(self):
        rank = self.field_card.rank
        if rank == 1:
            print("----------2:Two!----------")
            self.flag_2 += 1
        elif rank == 2:
            print("----------3:Three!----------")
            self.flag_3 += 1
        elif rank == 7:
            print("----------8:Eight!----------")
            new_suit = self.players[self.turn_player_index].effect_7()
            self.field_card.suit = int(new_suit)
            print("新しいSuitは、"+["s", "h", "d", "c"][self.field_card.suit]+"です。")
        elif rank == 10:
            print("----------J:Jump!----------")
            self.flag_j = True
        elif rank == 11:
            print("----------Q:Quick Turn!----------")
            self.flag_q = (self.flag_q + 1) % 2
        else:
            pass

    # deckが無くなったときにfield_cardsから[0]を残し残りをdeckにする
    def deck_reset(self):
        if len(self.deck.cards) <= 0:
            self.deck.cards = [self.field_cards.pop(
                1) for i in range(len(self.field_cards) - 1)]
            self.deck.shuffle()

    def print_data(self):
        [player.print_data() for player in self.players]
        [card.print_card() for card in self.field_cards]

    def print_field_card(self):
        print("Field:", self.field_cards[0].get_card())

    def turn(self):
        self.players[self.turn_player_index].print_data()
        self.print_field_card()

        # ターンスキップ
        if not self.flag_j:
            # 2か3が出されているか
            if self.flag_2 or self.flag_3:
                self.t_turn()
            else:
                self.normal_turn()
        else:
            print("ターンが飛ばされます")
            self.flag_j = False

        self.deck_reset()

        if len(self.players[self.turn_player_index].hands):
            if self.flag_q:
                self.turn_player_index = (self.turn_player_index - 1) % 4
            else:
                self.turn_player_index = (self.turn_player_index + 1) % 4
        else:
            self.game_flag = False

    def t_turn(self):
        num = self.flag_2 or self.flag_3
        selectedCards = self.players[self.turn_player_index].put_card_list(
            self.field_card, rank_mutch_card)

        if selectedCards:
            self.field_cards.insert(
                0, self.players[self.turn_player_index].choice_put_card(selectedCards))
            print(self.players[self.turn_player_index].name,
                  "は", self.field_cards[0].get_card(), "を出します")
            self.update_field_card()
        else:
            print(self.players[self.turn_player_index].name, "は",
                  num*(self.field_card.rank+1), "枚引きます")
            for i in range(num * (self.field_card.rank+1)):
                self.players[self.turn_player_index].add_hand(self.deck.pull())
                self.deck_reset()
            self.flag_2 = 0
            self.flag_3 = 0

    def win(self):
        print("WINNER", self.players[self.turn_player_index].name, "!!!!!")

    def normal_turn(self):
        selectedCards = self.players[self.turn_player_index].put_card_list(
            self.field_card, normal_mutch_card)
        if selectedCards:   # 出せるカードがあるか
            self.field_cards.insert(
                0, self.players[self.turn_player_index].choice_put_card(selectedCards))
            print(self.players[self.turn_player_index].name,
                  "は", self.field_cards[0].get_card(), "を出します")
            self.update_field_card()
        else:   # カードを引く、それが出せるか判断する
            tmpCard = self.deck.pull()
            if tmpCard.mutch_card(self.field_cards[0]):
                self.field_cards.insert(0, tmpCard)
                print(self.players[self.turn_player_index].name,
                      "は", self.field_cards[0].get_card(), "を出します")
                self.update_field_card()
            else:
                self.players[self.turn_player_index].add_hand(tmpCard)
