from american_page_one import AmericanPageOne

game = AmericanPageOne(4)
game.print_data()

while game.game_flag:
    game.turn()
game.win()
