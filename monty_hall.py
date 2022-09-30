import random
import time
random.seed(time.time())
#There are 3 doors, one of them contains a car while the two contains goats
doors = ['a','b','c']
switch = True
def simulate_monty():
    #Chooses one of the 3 doors to hide the prize behind
    prize = random.choice(doors)
    prize_dict = {}
    for door in doors:
        if (door == prize):
            prize_dict[door] = "Car"
        else:
            prize_dict[door] = "Goat"
    #print(prize_dict)

    #Contestant chooses one door
    chosen_door = random.choice(doors)

    #Host opens one of the doors that doesn't have the car in it and isn't the
    #chosen door
    for i in range(len(doors)):
        if ((doors[i] != chosen_door) and (doors[i] != prize)):
            host_opened_door = doors[i]
            break
    #Now there are only two doors left to pick
    remaining_doors = []
    for door in doors:
        if (door != host_opened_door):
            remaining_doors.append(door)
    #Determines whether the contestant wins the prize or not
    if (switch == False):
        if (chosen_door == prize):
            return("Win")
        else:
            return("Lose")
    elif (switch == True):
        if (chosen_door == prize):
            return("Lose")
        else:
            return("Win")
    print("an error has occured")
simulations = []
print("Starting simulation...")
for i in range(1000000):
    current_sim = simulate_monty()
    simulations.append(current_sim)
wins = simulations.count("Win")
loses = simulations.count("Lose")
winrate = wins/(wins+loses)*100
print("Win rate when switch {switch}: {winrate}% \nWin {win} Lose {lose}"
.format(switch=switch,winrate=winrate,win=wins,lose=loses))
if (switch == True) and winrate > 50:
    print("Switching makes you more likely to win the prize.")
elif (switch == False) and winrate > 50:
    print("Not switching makes you more likely to win the prize.")
else:
    print("Switching makes you more likely to win the prize.")
