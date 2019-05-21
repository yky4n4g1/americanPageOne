class Player:
    def __init__(self, name):
        self.name = name
        self.hands = []

    # プレイヤーのHandにcardを追加
    def add_hand(self, card):
        self.hands.append(card)

    # ターンごとに表示される情報
    def print_data(self):
        print("Name:", self.name)
        print("Number of Hands:", len(self.hands))
        print("Hands:", {index: self.hands[index].get_card()
                         for index in range(len(self.hands))})

    def get_data(self):
        return {"name": self.name, "hands": {index: self.hands[index].get_card() for index in range(len(self.hands))}}

    def put_card_list(self, field_card, func):
        indexes = [i for i in range(len(self.hands)) if func(
            self.hands[i], field_card)]
        if indexes == []:
            return False
        else:
            return indexes

    def put_hand(self, num):
        return self.hands.pop(num)

    def choice_put_card(self, put_cards):
        print(put_cards)
        put_cards = [str(i) for i in put_cards]
        select = input("出すカードを選択：")
        while select not in put_cards:
            print("無いよ")
            select = input("出すカードを選択：")
        return self.put_hand(int(select))

    def effect_7(self):
        print("0:S 1:H 2:D 3:C")
        print("ランクを選んでね")
        new_suit = input(">")
        while new_suit not in ["0", "1", "2", "3"]:
            print("0~3で選んで")
            print("スートを選んでね")
            new_suit = input(">")
        return new_suit


class CpuPlayer(Player):
    def choice_put_card(self, put_cards):
        return self.put_hand(put_cards[0])

    def print_data(self):
        print("Name:", self.name)
        print("Number of Hands:", len(self.hands))

    def effect_7(self):
        new_suit = 0
        if len(self.hands):
            new_suit = self.hands[0].suit
        return new_suit
