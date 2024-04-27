import random

class Fighter():
    def __init__(self, name):
        self.name = name
        self.atk = 20
        self.hp = 100

    def punch(self, opponent):
        opponent.hp -= self.atk
        print(f"{opponent.name} got punched by {self.name}")
        print(f"Player: {self.hp}hp")
        print(f"Opponent: {opponent.hp}hp")

    def kick(self, opponent):
        opponent.hp -= self.atk * 1.25
        print (f"{opponent.name} was kicked by {self.name}")
        print(f"Player: {self.hp}hp")
        print(f"Opponent: {opponent.hp}hp")

class Ninja(Fighter):
    def __init__(self, name):
        super().__init__(name)

    def ninja_kick(self, opponent):
        opponent.hp -= self.atk * 1.35
        print(f"{opponent.name} was ninja kicked by {self.name}")
        print(f"Player: {self.hp}hp")
        print(f"Opponent: {opponent.hp}hp")

class Boxer(Fighter):
    def __init__(self, name):
        super().__init__(name)

    def uppercut(self, opponent):
        opponent.hp -= self.atk * 1.35
        print(f"{opponent.name} got uppercutted by {self.name}")
        print(f"Player: {self.hp}hp")
        print(f"Opponent: {opponent.hp}hp")

player = Ninja('Mr poopy butthole')
opponent = Boxer('Johnathon')

while player.hp > 0 and opponent.hp > 0:
    while True:
        play = input("Do you want to punch, kick or ninja kick").upper()
        if play == 'PUNCH':
            player.punch(opponent)
            break
        elif play == 'KICK':
            player.kick(opponent)
            break
        elif play == 'NINJA KICK':
            player.ninja_kick(opponent)
            break
        else:
            print("Not a valid option M8")
    
    opp_play = random.randint(1,3)
    if opp_play == 1:
        opponent.punch(player)
    elif opp_play == 2:
        opponent.kick(player)
    else:
        opponent.uppercut(player)

if player.hp > 0:
    print("player wins")
else:
    print("opponent wins")