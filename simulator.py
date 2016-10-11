#################TWITCH PLAYS POKEMON STADIUM 2: MATCH SIMULATOR################
############################CREATED BY INFORTUNATUS#############################
from math import floor
from math import ceil
from string import capwords

typeIndices = {'normal': 0, 'fighting': 1, 'flying': 2, 'poison': 3,
                'ground': 4, 'rock': 5, 'bug': 6, 'ghost': 7, 'steel': 8,
                'fire': 9, 'water': 10, 'grass': 11, 'electric': 12,
                'psychic': 13, 'ice': 14, 'dragon': 15, 'dark': 16}

##################################SET-UP########################################

def pokeDict():
    #Reads the file 'pokeList.txt' to generate a dictionary containing
    #each Pokemon's name, type(s), Stadium 2 stats, and moves.       

    dictionary = {} 
    pokeFile = open('data/pokeList.txt', 'r')

    #Converts each line of the file to a list of the Pokemon's data.
    #The slice [:-1] eliminates the '\n' at the end of each line.
    lines = [line[:-1].strip().split('\t') for line in pokeFile.readlines()]
    pokeFile.close()

    #Converts strings into lowercase and stats into floats for later calcs.
    for dataList in lines:
        species = dataList[0].lower()
        types = tuple([entry.lower() for entry in dataList[1:3]])
        stats = tuple([float(num) for num in dataList[3:9]])
        moves = tuple([entry.lower() for entry in dataList[9:]])

        dictionary[species] = (types,stats,moves)

    return dictionary

def moveDict():
    #Generates a dictionary of "regular" damaging moves with their
    #names, types, attributes (physical/special), base powers, turn counts,
    #and accuracies.
    
    dictionary = {}
    moveFile = open('data/moves.txt', 'r')

    #Converts file lines to lists
    lines = [line[:-1].strip().split('\t') for line in moveFile.readlines()]
    moveFile.close()
    
    #Note: Although 'move_turns' is stored, multi-turn moves like Fly are
    #treated as one-turn moves if the charging turn grants invulnerability.
    for dataList in lines:
        name = dataList[0].lower()
        move_type = dataList[1].lower()
        move_attr = dataList[2].lower()
        move_power = float(dataList[3])
        move_turns = int(dataList[4])
        move_accuracy = int(dataList[5])
        move_code = dataList[6].lower()

        #Appends move info to move dictionary
        dictionary[name] = (move_type,move_attr,move_power,move_turns,
                            move_accuracy,move_code)

    return dictionary

def types():
    #Creates a table of type matchups to assist in damage calculation.
    typeFile = open('data/typeChart.txt','r')

    #Reads the file's lines, then splits by whitespace, converting the string
    #for each damage modifier into a float
    typeChart = [[float(entry) for entry in row.strip().split()]\
                  for row in typeFile.readlines()]
    typeFile.close()

    return typeChart

##############################DISPLAY FUNCTIONS##################################

def header(text):
    #Makes a visible header out of a selected string for prominent viewing.
    #For example, header('hello') becomes '###### HELLO ######'

    #Calculates how many octothorpes are needed to fill blank space
    numHashes = 78 - len(text)

    #Distributes between right and left sides
    numHashesLeft = numHashes//2
    numHashesRight = numHashes - numHashesLeft

    #Smashes together into a string
    return "#"*numHashesLeft + " " + text.upper() + " " + "#"*numHashesRight\
           +'\n'

def displayTypes(types):
    #Reads the types tuple and outputs a neat display of the Pokemon's type(s)
    if types[1] == 'none':
        return types[0].capitalize()
    else:
        return types[0].capitalize() + ", " + types[1].capitalize()

def displayMoves(moveNames):
    #Reads the moves tuple and outputs a display of the Pokemon's move(s)
    string = "Moves: {0}".format(capwords(moveNames[0]))

    #Adds second through fourth moves if they exist (i.e. aren't 'none')
    for name in moveNames[1:]:
        if name != 'none':
            string += ", {0}".format(capwords(name))

    return string

def displayDamaging(moveNames):
    #Displays a Pokemon's damaging moves using its self.moves tuple
    string = "Damaging moves: "

    #Adds each move to the string to be printed
    for name in moveNames:
        if name in md:
            string += "{0}, ".format(capwords(name))

    return string[:-2]

def displayStats(stats):
    #Reads the stats tuple and outputs a display of the Pokemon's stats
    hp = int(stats[0])
    attack = int(stats[1])
    defense = int(stats[2])
    spAtk = int(stats[3])
    spDef = int(stats[4])
    speed = int(stats[5])    

    #Compiles stats into string to be printed
    string = "HP: {0}  Attack: {1}  Defense: {2}  Sp. Atk: {3}  Sp. Def: {4}  "\
             .format(hp, attack, defense, spAtk, spDef) + "Speed: {0}"\
             .format(speed)

    return string

def printInfo(pkmn,order='n'):
    #Uses the functions above to display all of a Pokemon's relevant info.
    #This function is used in two places: At the start of a match (to provide
    #an initial display of each team) and during an individual matchups.

    #If an integer argument 'order' is defined, lists the Pokemon's order
    #in its team lineup along with its data.
    if type(order) == int:
        print("Member {0}: {1}\t Level {2}\t Type(s): {3}"\
              .format(order, pkmn.name, pkmn.lvl, displayTypes(pkmn.types)))
        
    #If 'order' is left unchanged, the Pokemon's order is not displayed.
    else:
        print("{0}: Level {1}\t Type(s): {2}"\
              .format(pkmn.name, pkmn.lvl, displayTypes(pkmn.types)))

    #Displays the Pokemon's moves, its damaging moves, and finally its stats.
    print(displayMoves(pkmn.moves))
    print(displayDamaging(pkmn.moves))
    print(displayStats(pkmn.stats))
    print('\n')
    
def teamBuilder(blues,reds):
    #Runs printInfo for the members of each team at the start of a battle.
    print(header("BLUE TEAM"))
    printInfo(blues[0],order=1)
    printInfo(blues[1],order=2)
    printInfo(blues[2],order=3)
    
    print(header("RED TEAM"))
    printInfo(reds[0],order=1)
    printInfo(reds[1],order=2)
    printInfo(reds[2],order=3)

def cPrint(string,pMode):
    #Conditional print: prints as normal only if pMode is set to 'p'
    if pMode == 'p':
        print(string)

############################POKEMON AND MOVE CLASSES############################

class Pokemon(object):
    #Used to store data for individual Pokemon in an easily referenced way
    def __init__(self,name,level=100):
        self.name = capwords(name)
        self.lvl = level
        self.types = pd[name][0]        
        self.stats = pd[name][1]
        self.moves = pd[name][2]

    #Used at the beginning of a battle to designate each Pokemon's team
    def selectTeam(self,teamName):
        self.team = teamName
        

class Move(object):
    #Stores data for damaging moves when they are referenced in the lineup
    def __init__(self,name):
        self.name = capwords(name)
        self.type = md[name][0]
        self.attr = md[name][1]
        self.pwr = md[name][2]
        self.turns = md[name][3]
        self.accr = md[name][4]
        self.code = md[name][5]

##########################DAMAGE CALCULATION FUNCTIONS##########################

def stab(atypes,mtype):
    #Determines whether STAB (Same-type attack bonus) applies by reading the
    #attacker's types and the move's type
    if mtype in atypes:
        return 1.5
    else:
        return 1.0

def effectiveness(dtypes,mtype):
    #Calculates the damage multiplier for type advantages
    #Separates the defender's types
    type1 = dtypes[0]
    type2 = dtypes[1]
    
    if mtype != 'none':

        #Effectiveness against first defender type
        row = typeIndices[mtype]
        if type1 != 'none':
            col_1 = typeIndices[type1]
            mult_1 = tc[row][col_1]
        else:
            mult_1 = 1

        #Effectiveness against second type, if it exists
        if type2 != 'none':
            col_2 = typeIndices[type2]
            mult_2 = tc[row][col_2]
        else:
            mult_2 = 1

    #A handful of moves are typeless, in which case there is no STAB    
    else:
        mult_1 = 1
        mult_2 = 1

    return mult_1*mult_2

def baseDamage(attacker,defender,mAttr,mPwr,mType,explosion='n'):
    #Determines the base damage done by a move that utilizes base power.

    #Attacker's info
    aTypes = attacker.types
    aStats = attacker.stats
    aLvl = attacker.lvl

    #Defender's info
    dTypes = defender.types
    dStats = defender.stats

    #Uses move's attribute to decide whether physical or special stats are used
    if mAttr ==  'physical':
        att = aStats[1]
        dfs = dStats[2]
    elif mAttr == 'special':
        att = aStats[3]
        dfs = dStats[4]
    else:
        print("ERROR: Move attribute not recognized")

    #Halves the opponent's defense if the keyword variable explosion is 'y'
    if explosion == 'y':
        dfs = floor(dfs/2)
    
    #Uses Pokemon damage formula to calculate damage before typing and STAB
    raw = (2*aLvl + 10)/250.0 *att/dfs * mPwr + 2

    #Calculates the modifier using STAB and typing
    modifier = stab(aTypes,mType) * effectiveness(dTypes,mType)

    base = raw * modifier

    return base

def regular(attacker,defender,move):
    #Calculates max, min, and average damage for moves that operate based on
    #a signle hit using base power for damage calculation

    maxdmg = baseDamage(attacker,defender,move.attr,move.pwr,move.type)
    mindmg = 0.85*maxdmg
    avgdmg = 0.925*maxdmg

    return (mindmg,maxdmg,avgdmg)

def multistrike(attacker,defender,move):
    #Calculates max, min, and average damage for multistrike moves, excluding
    #Triple Kick

    #A multi-strike move hits from 2-5 times. Each number of strikes has a
    #different probability, and the weighted average is three strikes.
    maxdmg = baseDamage(attacker,defender,move.attr,5*move.pwr,move.type)
    mindmg = 0.85*baseDamage(attacker,defender,move.attr,2*move.pwr,move.type)
    avgdmg = 0.925*baseDamage(attacker,defender,move.attr,3*move.pwr,move.type)

    return (mindmg,maxdmg,avgdmg)

def triplekick(attacker,defender,move):
    #Calculates damages for Triple Kick, which hits up to three times.
    #Kick 1 has 10 power, kick 2 has 20, and kick 3 has 30, but each kick has
    #its own accuracy check (90%), which makes the average power 47.07.

    minPwr = 10.0
    maxPwr = 60.0
    avgPwr = 47.07

    maxdmg = baseDamage(attacker,defender,move.attr,maxPwr,move.type)
    mindmg = 0.85*baseDamage(attacker,defender,move.attr,minPwr,move.type)
    avgdmg = 0.925*baseDamage(attacker,defender,move.attr,avgPwr,move.type)

    return (mindmg,maxdmg,avgdmg)

def magnitude(attacker,defender,move):
    #Calculates damage for Magnitude. Magnitude has a variety of base powers,
    #each with its own probability weight; the base power ranges from 10 to 150,
    #with an average of 71.

    minPwr = 10.0
    maxPwr = 150.0
    avgPwr = 71.0

    maxdmg = baseDamage(attacker,defender,move.attr,maxPwr,move.type)
    mindmg = 0.85*baseDamage(attacker,defender,move.attr,minPwr,move.type)
    avgdmg = 0.925*baseDamage(attacker,defender,move.attr,avgPwr,move.type)

    return (mindmg,maxdmg,avgdmg)

def sonicboom(attacker,defender):
    #Deals exactly 20 damage if the defender is not a ghost
    if 'ghost' in defender.types:
        return (0.0,0.0,0.0)
    else:  
        return (20.0,20.0,20.0)

def dragonrage(attacker,defender):
    #Deals exactly 40 damage
    return (40.0,40.0,40.0)

def nightshade(attacker,defender):
    #Deals damage exactly equal to the attacker's level if the defender
    #is not Normal
    if 'normal' in defender.types:
        return (0.0,0.0,0.0)
    else:
        dmg = float(attacker.lvl)
        return (dmg,dmg,dmg)

def seismictoss(attacker,defender):
    #Deals damage exactly equal to the attacker's level if the defender
    #is not Ghost
    if 'ghost' in defender.types:
        return (0.0,0.0,0.0)
    else:
        dmg = float(attacker.lvl)
        return (dmg,dmg,dmg)

def psywave(attacker,defender):
    #Deals a random amount of damage between 0.5 and 1.5 times the user's level
    #unless the defender is Dark-type
    if 'dark' in defender.types:
        return (0.0,0.0,0.0)
    else:
        basedmg = float(attacker.lvl)
        return (0.5*basedmg,1.5*basedmg,basedmg)

def explosion(attacker,defender,move):
    #Identical to the regular function, except the explosion flag is activated,
    #halving the opponent's Defense in damage calculation

    maxdmg = baseDamage(attacker,defender,move.attr,move.pwr,move.type,
                        explosion='y')
    mindmg = 0.85*maxdmg
    avgdmg = 0.925*maxdmg

    return (mindmg,maxdmg,avgdmg)

def flail(attacker,defender,move):
    #Has various base powers depending on the user's remaining HP.
    #The "average power" is based on a weighted average of all the user's
    #possible HP states and their corresponding Flail powers.

    minPwr = 20.0
    maxPwr = 200.0
    avgPwr = 59.5

    maxdmg = baseDamage(attacker,defender,move.attr,maxPwr,move.type)
    mindmg = 0.85*baseDamage(attacker,defender,move.attr,minPwr,move.type)
    avgdmg = 0.925*baseDamage(attacker,defender,move.attr,avgPwr,move.type)

    return (mindmg,maxdmg,avgdmg)

def superfang(defender):
    #Deals half the defender's HP in damage if the defender is not a ghost
    if 'ghost' in defender.types:
        return (0.0,0.0,0.0)
    else:
        defenderhp = defender.stats[0]
        dmg = floor(0.5*defenderhp)
        return (dmg,dmg,dmg)

def rollout(attacker,defender,move,remainingHealth='N/A'):
    #Rollout's power doubles each turn. As a result, the kill turns cannot be
    #calculated in the same way as they are in the main body of the program.

    #The first time rollout is run, it uses the defender's max HP.
    #If it is being run recursively (see below), it uses remaining HP.
    if remainingHealth == 'N/A':
        defHP = defender.stats[0]
    elif type(remainingHealth) == float:
        defHP = remainingHealth

    #The damage done so far, and the turns taken to kill the target
    rollingMin = 0.0
    rollingMax = 0.0
    rollingAvg = 0.0
    killTurns = 0

    #The power starts at the move's base power (30 for Rollout)
    power = move.pwr
    
    turns = 1

    while turns <=5:
        #Runs rollout's current power through the damage formula and adds
        #the damages to the rolling totals until a kill occurs.

        turnMaxDmg = baseDamage(attacker,defender,move.attr,power,move.type)
        turnMinDmg = 0.85*turnMaxDmg
        turnAvgDmg = 0.925*turnMaxDmg

        rollingMin += floor(turnMinDmg)
        rollingMax += floor(turnMaxDmg)
        rollingAvg += floor(turnAvgDmg)

        #If Rollout deals enough average damage to kill the defender within
        #5 turns, the loop breaks, and returns the damages and the number
        #of turns taken to kill the opponent
        if floor(rollingAvg) >= defHP:
            killTurns += turns
            dataList = [rollingMin,rollingMax,rollingAvg,killTurns]
            break

        #Doubles Rollout's power if it has turns left
        power *= 2
        turns += 1

    else:
        #If rollout is too weak to kill within five turns, its power resets.
        #In this case, the function saves the damage done and turns taken so far,
        #and runs itself again, this time using the amount of HP the defender
        #has left. This recursion continues until the defender is killed.
        killTurns += 5
        defHP -= rollingAvg
        oldList = [rollingMin,rollingMax,rollingAvg,killTurns]
        newList = rollout(attacker,defender,move,remainingHealth=defHP)

        #When Rollout finally kills and the deepest recursion terminates,
        #the damages and kill turns are added to those from each previous round,
        #finally culminating in the final damage done and turns to kill.
        dataList = map(sum,zip(oldList,newList))

    return dataList

def furycutter(attacker,defender,move):
    #Fury Cutter is identical to Rollout, except that once its power hits
    #the cap, it stays there without resetting until a miss or move switch.
    defHP = defender.stats[0]
    
    rollingMin = 0.0
    rollingMax = 0.0
    rollingAvg = 0.0
    killTurns = 0

    #Starts at base power (10 for Fury Cutter in Gen 2)
    power = move.pwr
    
    turns = 1

    while True:
        #Runs FC's current power through the damage formula and adds
        #the damages to the rolling totals until a kill occurs.
        
        turnMaxDmg = baseDamage(attacker,defender,move.attr,power,move.type)
        turnMinDmg = 0.85*turnMaxDmg
        turnAvgDmg = 0.925*turnMaxDmg

        rollingMin += floor(turnMinDmg)
        rollingMax += floor(turnMaxDmg)
        rollingAvg += floor(turnAvgDmg)

       #Breaks the loop if Fury Cutter kills
        if floor(rollingAvg) >= defHP:
            killTurns += turns
            dataList = [rollingMin,rollingMax,rollingAvg,killTurns]
            break

        #Doubles move power if the current turn is not yet 5
        if turns < 5:
            power *= 2
            
        turns += 1

    return dataList

#############################CALCULATOR MAIN BODY###############################
    
def killStrikes(defenderHP,dmg):
    #Expects a defending Pokemon's HP and damage dealt by an attacker
    #(as a float) and calculates the number of strikes the move takes to kill.
    #This is returned as both an int and a float; the int is what counts
    #for actual turns, but the float is needed to decide which among a group of
    #moves with the same integer kill time is actually the better move.

    #Damage calculation rounds damage down. At first we use a decimal quotient.
    gameDmg = floor(dmg)
    fltStrikes = defenderHP/gameDmg

    #If the defender's HP is not exactly divisible by gameDmg, the remainder
    #must be counted as an additional turn, requiring the ceil function.
    intStrikes = int(ceil(fltStrikes))

    return(fltStrikes,intStrikes)
    
def damageInterpreter(attacker,defender,move,damages,pMode):
    #Refines the damage list into displayable info about a move's kill speed.
    #Prints that info if the simulator is in replay mode.
    defenderHP = defender.stats[0]
    
    mindmg = damages[0]
    maxdmg = damages[1]
    avgdmg = damages[2]
    mTurns = move.turns
    mAcc = move.accr

    mindmgpc = round(100*mindmg/defenderHP,1)
    maxdmgpc = round(100*maxdmg/defenderHP,1)
    avgdmgpc = round(100*avgdmg/defenderHP,1)


    if move.code != 'superfang':
        if mindmg == maxdmg:
            cPrint("{0} will deal exactly {1}% damage."\
                   .format(move.name,avgdmgpc),pMode)
        else:
            cPrint("{0} will deal from {1}% to {2}% damage, on average {3}%."\
                   .format(move.name, mindmgpc, maxdmgpc, avgdmgpc),pMode)
    else:
        cPrint("If {0} is at max health, {1} will deal {2}% damage."\
               .format(defender.name,move.name,avgdmgpc),pMode)
        
    
    #If the move deals no damage, it is announced to be ineffective.
    if maxdmg == 0:
        cPrint("The move has no effect! \n",pMode)
        killTurns = 'N/A'

    #Otherwise, the program computes about how many hits the move takes to kill.
    else:

        strikes = killStrikes(defenderHP,avgdmg)
        fltStrikes = strikes[0]
        intStrikes = strikes[1]
        
        if move.code != 'superfang' and move.code != 'flail':
            cPrint("{0} will take about {1} strike(s) to kill {2}."\
                  .format(move.name,intStrikes,defender.name),pMode)

        if move.code == 'explosion' and intStrikes >1:
            cPrint(("Since this move kills the user, it should not be used "\
                   +"first."),pMode)
            
        #If the move has perfect accuracy and executes in one turn, then
        #the number of strikes to kill equals the number of turns to kill.
        #Note that moves with invulnerable turns, like Dig, count as one turn.
        if mAcc == 100 and mTurns == 1:
            killTurns = fltStrikes
            cPrint('',pMode)

        #If the move executes in one turn but has imperfect accuracy,
        #the program increases the decimal kill turns accordingly.
        elif mAcc != 100 and mTurns == 1:
            accMult = 100.0/mAcc
            killTurns = fltStrikes * accMult

            #Rounds up to the nearest whole number for display
            intKillTurns = int(ceil(killTurns))
            
            if move.code != 'superfang' and move.code != 'flail':
                cPrint(("However, this move has {0} accuracy. Thus it will "\
                        +"take about {1} turn(s) to kill.\n")\
                       .format(mAcc,intKillTurns),pMode)
            else:
                print("\n")

        #If the move has perfect accuracy but executes in multiple turns,
        #the number of kill strikes is rounded up and multiplied by the number
        #of move turns to obtain the number of turns needed to kill.
        elif mAcc == 100 and mTurns != 1:
            killTurns = ceil(fltStrikes)*mTurns
            intKillTurns = int(killTurns)        
            
            cPrint(("However, this move takes {0} turns to strike.\n"\
                    + "Thus it will take about {1} turns to kill.\n")\
                   .format(mTurns,intKillTurns),pMode)

        #If the move executes in multiple turns AND has imperfect accuracy,
        #the number of kill strikes is first recalculated according to accuracy,
        #then multiplied by the number of move turns to obtain the kill turns.
        elif mAcc != 100 and mTurns != 1:
            accMult = 100.0/mAcc
            killTurns = (ceil(fltStrikes * accMult))*mTurns

            #Hyper Beam counts as a two-turn move but fires on the first turn.
            #One turn is subtracted from the kill turns, since the recharge
            #turn has no effect on the current matchup.
            if move.name == 'Hyper Beam':
                killTurns -= 1
                
            intKillTurns = int(killTurns)
            cPrint(("However, this move has {0} mAccuracy and takes {1} turns "\
                    +"to complete.\nThus it will take about {2} turn(s) "\
                    +"to kill.\n").format(mAcc,mTurns,intKillTurns),pMode)

    return killTurns

def moveInterpreter(attacker,defender,move,pMode):
    #Uses the attacker's and defender's stats and a move's info to calculate
    #damage, then runs those damages through damageInterpreter to obtain
    #kill turns.


    cPrint("If {0} uses {1} on {2}:"
           .format(attacker.name,move.name,defender.name),pMode)
    
    #First, we start with moves that cause a matchup to be flagged-- i.e. moves
    #whose effects the user should inspect in replay mode.
    if move.code == 'explosion':
        damages = explosion(attacker,defender,move)
        killTurns = damageInterpreter(attacker,defender,move,damages,pMode)

        #If Explosion/Selfdestruct is not an OHKO, the move is not considered
        #in damageIterator.
        if killTurns != 'N/A' and ceil(killTurns) > 1.0:
            killTurns = 'N/A'

        flag = move.name

    elif move.code == 'flail':
        damages = flail(attacker,defender,move)
        killTurns = damageInterpreter(attacker,defender,move,damages,pMode)

        #killTurns is run above only for the sake of printing info about the
        #move in replay mode. Flail is not considered in damageIterator.
        killTurns = 'N/A'

        flag = move.name

    elif move.code == 'superfang':
        damages = superfang(defender)
        killTurns = damageInterpreter(attacker,defender,move,damages,pMode)

        #Like above, Super Fang is not considered in damageIterator.
        killTurns = 'N/A'

        flag = move.name

    elif move.code == 'rollout':
        #Runs the rollout function to obtain info about the move
        dataList = rollout(attacker,defender,move)
        defenderHP = defender.stats[0]

        minDmgPc = round(100*dataList[0]/defenderHP,1)
        maxDmgPc = round(100*dataList[1]/defenderHP,1)
        avgDmgPc = round(100*dataList[2]/defenderHP,1)
        killTurns = dataList[3]
        
        #In replay mode, prints a unique message about the effectiveness of
        #Rollout, since damageInterpreter is not used
        cPrint(("Over the course of {0} turns, {1} deals from {2}% to {3}% "\
                + "damage, \naveraging {4}%. Note that this assumes the move "\
                + "does not miss.\n").format(killTurns,move.name,minDmgPc,
                                           maxDmgPc,avgDmgPc),pMode)

        flag = move.name

    elif move.code == 'furycutter':
        #Runs the Fury Cutter function to obtain info about the move
        dataList = furycutter(attacker,defender,move)
        defenderHP = defender.stats[0]

        minDmgPc = round(100*dataList[0]/defenderHP,1)
        maxDmgPc = round(100*dataList[1]/defenderHP,1)
        avgDmgPc = round(100*dataList[2]/defenderHP,1)
        killTurns = dataList[3]
        
        #In replay mode, prints a unique message about the effectiveness of
        #Fury Cutter, since damageInterpreter is not used
        cPrint(("Over the course of {0} turns, {1} deals from {2}% to {3}% "\
                + "damage, \naveraging {4}%. Note that this assumes the move "\
                + "does not miss.\n").format(killTurns,move.name,minDmgPc,
                                           maxDmgPc,avgDmgPc),pMode)

        flag = move.name

    #The five moves below take only two arguments, as opposed to the rest of the
    #remaining moves
    elif move.code in ('sonicboom', 'dragonrage', 'nightshade', 'seismictoss',
                       'psywave'):
        damages = globals()[move.code](attacker,defender)
        killTurns = damageInterpreter(attacker,defender,move,damages,pMode)

        flag = 'N/A'

    #All remaining damaging moves take three arguments: attacker, defender, move
    else:
        damages = globals()[move.code](attacker,defender,move)
        killTurns = damageInterpreter(attacker,defender,move,damages,pMode)

        flag = 'N/A'

    return (killTurns,flag)

def damageIterator(faster,slower,pMode,bMode):
    #Runs through both Pokemon's move lineups to determine which wins the match.
    
    #Creates dictionaries of the opponents' moves' kill speeds.
    #Keys are the kill speeds and values are the move names.
    fKT = {}
    sKT = {}
    flagList = []
  
    for moveName in faster.moves:
        #If a move in the faster Pokemon's lineup is in the dictionary of
        #damaging moves, damageInterpreter is executed to determine how fast it
        #kills the opponent. This info is then added to fKT.
        if moveName in md:
            move = Move(moveName)
            info = moveInterpreter(faster,slower,move,pMode)
            fasterKillSpeed = info[0]
            fKT[fasterKillSpeed]=move.name

            #If the moveset contains a flagged move, it is added to flagList.
            flag = info[1]
            if flag != 'N/A':
                flagList.append(flag)
           
    cPrint("-"*80 + "\n",pMode)

    for moveName in slower.moves:
        #Repeats the process with the slower Pokemon, adding to sKT.
        if moveName in md:
            move = Move(moveName)
            info = moveInterpreter(slower,faster,move,pMode)
            slowerKillSpeed = info[0]
            sKT[slowerKillSpeed]=move.name

            #If the moveset contains a flagged move, it is added to flagList.
            flag = info[1]
            if flag != 'N/A':
                flagList.append(flag)

    #Creates lists of the kill turns for the damaging moves of each combatant
    fasterTurns = [num for num in fKT.keys() if num != 'N/A']
    slowerTurns = [num for num in sKT.keys() if num != 'N/A']
    

    #First, if both lists are empty, neither Pokemon wins; a draw is declared
    if not(fasterTurns or slowerTurns):
        cPrint("Neither Pokemon can damage the other.\nPROJECTED WINNER: None",
               pMode)
        winner = 'No winner'
        winningCondition = 'no winning move'

    #If exactly one Pokemon is unable to deal damage, the other Pokemon wins.
    elif not slowerTurns:
        cPrint("{0} cannot damage {1}.".format(slower.name,faster.name),pMode)
        cPrint("PROJECTED WINNER: {0}".format(faster.name),pMode)
        winner = faster
        winningCondition = 'by immunity'
        
    elif not fasterTurns:
        cPrint("{0} cannot damage {1}.".format(faster.name,slower.name),pMode)
        cPrint("PROJECTED WINNER: {0}".format(slower.name),pMode)
        winner = slower
        winningCondition = 'by immunity'

    #Otherwise, both Pokemon are capable of dealing damage.
    else:

        #If the two Pokemon are identical, the iterator calls a draw.
        if faster.name == slower.name:
            cPrint("The combatants are identical. \nPROJECTED WINNER: None",
                   pMode)
            winner = 'No winner'
            winningCondition = 'no winning move'

        #Finally, if everything has been normal until now, the iterator proceeds
        #on the assumption that each Pokemon uses its most efficient damaging
        #move against the other by taking the minima of the turn lists.
        else:
            fastMin = min(fasterTurns)
            slowMin = min(slowerTurns)

            #Since whole-number turns are what count, each is rounded up.
            #If the numbers are different, the lower number wins. If there is
            #a tie, the faster Pokemon wins.
            if ceil(fastMin) <= ceil(slowMin):
                winningMove = fKT[fastMin]
                winner = faster

                #Roughly measures how many extra turns the winner has as an
                #indication of how even the matchup is
                spareTurns = int(ceil(slowMin) - ceil(fastMin))

            else:
                winningMove = sKT[slowMin]
                winnerTurns = int(ceil(slowMin))
                winner= slower

                #If the slower Pokemon wins, it has one less spare turn
                spareTurns = int(ceil(fastMin) - ceil(slowMin)) - 1

                    
            cPrint ("PROJECTED WINNER: {0}, using {1}"\
                      .format(winner.name, winningMove),pMode)

            winningCondition=('using {0}, with {1} turn(s) to spare.')\
                              .format(winningMove,spareTurns)

    #Adds a line break if the iterator is in print mode, for easier viewing
    cPrint('',pMode)

    #If the iterator is running in 'b' mode, as it is during the initial
    #simulation, the function returns the winning information for use in
    #the outcome display. Otherwise, the iterator is probably in replay mode,
    #and returning winners is unnecessary.
    if bMode == 'b':
        if winner == 'No winner':
            return (winner,winningCondition,flagList)
        else:
            return (winner.name,winner.team,winningCondition,flagList)

#############################PROCESSING WINNER INFO#############################
     
def matchup(matchNumber,poke1,poke2,pMode,bMode='b'):
    #Streamlines printing match information in replay mode

    matchName = "{0} vs. {1}".format(poke1.name,poke2.name)

    #Prints the match name in replay mode
    if pMode == 'p':
        announcement = ("Match {0}: {1}")\
                       .format(matchNumber,matchName)
        print(header(announcement))
    
        printInfo(poke1)
        printInfo(poke2)

    #Determines which Pokemon is faster
    speed1 = poke1.stats[5]
    speed2 = poke2.stats[5]

    #Decides which Pokemon wins, and prints info about speed in replay mode
    if speed1 == speed2:
        cPrint("{0} and {1} are equally fast.\n".format(poke1.name,poke2.name),
               pMode)
        cPrint ("-"*80 + "\n",pMode)
        winningInfo = damageIterator(poke1,poke2,pMode,bMode)
        
    elif speed1 > speed2:
        cPrint ("{0} outspeeds {1}.\n".format(poke1.name,poke2.name),pMode)
        cPrint ("-"*80 + "\n",pMode)
        winningInfo = damageIterator(poke1,poke2,pMode,bMode)
        
    elif speed1 < speed2:
        cPrint("{1} outspeeds {0}.\n".format(poke1.name,poke2.name),pMode)
        cPrint ("-"*80 + "\n",pMode)
        winningInfo = damageIterator(poke2,poke1,pMode,bMode)

    if bMode == 'b':
        return (matchName,winningInfo)


def battle(blues,reds,pMode='np'):
    #Runs the battle. Huzzah.
    outcomes = []
    
    matchNumber = 1
    for combatant in blues:
        for opponent in reds:
            #Requests a tuple containing the match name and its results
            outcome = matchup(matchNumber,combatant,opponent,pMode)

            #Appends to a list of outcomes
            outcomes.append(outcome)
            matchNumber += 1
    
    return outcomes

###########################OUTPUT AND USER INTERFACE############################

def displayOutcomes(outcomeList,names):
    #Displays the projected outcome of each battle neatly.
    winningPokes = []
    winningTeams = []

    n = 1
    for entry in outcomeList:
        #Starts out with match name, as stored in each entry in outcomeList
        matchName = entry[0]
        notification = "Match {0}: {1}. \n".format(n,matchName)

        #Adds information about winner to notification
        winnerInfo = entry[1]        
        if len(winnerInfo) == 4: #Occurs if the match has a winner
            #Adds winner name, team, and condition
            winnerName = winnerInfo[0]
            winnerTeam = winnerInfo[1]
            winnerCondition = winnerInfo[2]
            flagList = winnerInfo[3]
            
            notification += "{0} from Team {1} wins {2} \n"\
                            .format(winnerName,winnerTeam,winnerCondition)
            winningPokes.append(winnerName)
            winningTeams.append(winnerTeam)

            if flagList:
                #If a match is flagged, adds flagged moved to the notification
                notification +="NOTE: This match contains "\
                              +"the following flagged moves:\n"
                for moveName in flagList:
                    notification += "{0}, ".format(moveName)
            
        if len(winnerInfo) == 3: #Occurs if the match has no winner
            #Adds notification that there was no winner
            notification += "{0}, and {1}. \n".format(winnerInfo[0],
                                                            winnerInfo[1])
            flagList = winnerInfo[2]

            if flagList:
                notification +="Note, however, that this match contains "\
                              +"the following flagged moves:\n"
                for moveName in flagList:
                    notification += "{0}, ".format(moveName)
            
        print(notification[:-2] + "\n")
        n+=1

    #Uses winningPokes and winningTeams to print the win record of each
    #Pokemon and each team.
    blueNames = names[:3]
    blueWins = winningTeams.count('Blue')
    blueSummary = "Blue Team: {0} wins.\n".format(blueWins)
    for pokeName in blueNames:
        wins = winningPokes.count(pokeName)
        blueSummary += "{0}: {1} \t".format(pokeName,wins)
    print(blueSummary + "\n")

    redNames = names[3:]
    redWins = winningTeams.count('Red')
    redSummary = "Red Team: {0} wins.\n".format(redWins)
    for pokeName in redNames:
        wins = winningPokes.count(pokeName)
        redSummary += "{0}: {1} \t".format(pokeName,wins)
    print(redSummary + "\n")


def replay(time=1):
    #Prompts the user to see a replay of a given match.
    #The 'time' parameter affects the matchup number in the matchup function.
    prompt = raw_input("To see the breakdown of a match, enter the names of "\
                       +"the two Pokemon,\nseparated by a comma.\n"\
                       +"To exit, enter the letter 'X'. To reset, enter"\
                       " 'R'. ").lower()
    print("\n")
    
    if not prompt in ('r','x'):
        #If prompt is not 'r' or 'x', checks to see if both Pokemon are in the
        #Pokemon dictionary. If not, gives the user another chance to input.
        fixed = [string.strip() for string in prompt.split(',')]
        
        if len(fixed) == 2:
            if fixed[0] in pd and fixed[1] in pd:
                #Creates instances of class Pokemon for the match display
                poke1 = Pokemon(fixed[0])
                poke2 = Pokemon(fixed[1])

                #Displays the matchup by running matchup() in pMode 'p'
                matchup(time,poke1,poke2,pMode='p',bMode='r')

                #Prompts the user to see another match by restarting
                time +=1
                replay(time)
                    
            elif fixed[1] in pd:
                print("Pokemon 1 not recognized. Try again.")
                replay(time)
            elif fixed[0] in pd:
                print("Pokemon 2 not recognized. Try again.")
                replay(time)
            else:
                print("Neither Pokemon recognized. Try again.")
                replay(time)
        else:
            print("Input not recognized. Try again.")
            replay(time)

    #If the prompt is 'r', the simulator resets.
    elif prompt == 'r':
        print("\n")
        simulator()

    #If prompt is 'x', the function terminates and nothing happens.  
        
def simulator():
    #Prompts user to input Pokemon's names
    blueName1=raw_input("Enter the name of Blue Team's first Pokemon. ").strip().lower()
    blueName2=raw_input("Enter the name of Blue Team's second Pokemon. ").strip().lower()
    blueName3=raw_input("Enter the name of Blue Team's third Pokemon. ").strip().lower()

    redName1=raw_input("Enter the name of Red Team's first Pokemon. ").strip().lower()
    redName2=raw_input("Enter the name of Red Team's second Pokemon. ").strip().lower()
    redName3=raw_input("Enter the name of Red Team's third Pokemon. ").strip().lower()
        
    print("\n")

    #Scans the list of names for errors
    lowcaseNames = [blueName1,blueName2,blueName3,redName1,redName2,redName3]
    mistakes = False
    index = 1
    for entry in lowcaseNames:
        if entry not in pd:
            print("Pokemon {0} not recognized.".format(index))
            if mistakes == False:
                mistakes = True
        index +=1

    #If at least one error is found, prompts user to reset
    if mistakes:
        print("\n")
        retry = raw_input("Enter 'R' to reset. Enter any other key to exit.")
        if retry.lower() == 'r':
            print("\n")
            simulator()
    
    else:
        #If no errors are found, the program assigns the Pokemon to their teams
        blues = (Pokemon(blueName1),Pokemon(blueName2),Pokemon(blueName3))
        for pkmn in blues:
            pkmn.selectTeam('Blue')
            
        reds = (Pokemon(redName1),Pokemon(redName2),Pokemon(redName3))
        for pkmn in reds:
            pkmn.selectTeam('Red')

        #Displays team info
        teamBuilder(blues,reds)

        print('-'*80    )

        #Runs the battle function to determine the outcomes, then displays them.
        outcomeList = battle(blues,reds,pMode='np')
        properNames = [capwords(name) for name in lowcaseNames]
        displayOutcomes(outcomeList,properNames)

        replay()

##############################HOPEFULLY THIS WORKS##############################

pd = pokeDict()
tc = types()
md = moveDict()

simulator()
