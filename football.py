#import numpy
import heapq
#import tensorflow as tf
from csv import reader

#each row of data is a player in a play
#Getting all the plays into a dictionary
trainingData = open("train.csv", 'r')
next(trainingData)
plays = {} #playID, PlayersInAPlay

X = []
Y = []

#play direction calculation (todo: care about other players directions?)
def normalizeDirection(playDirection, rusherDir):
    if playDirection == "left":
            rusherDir = 360 - rusherDir
    return rusherDir
            
#if possession team == team player is on
def isPlayerOnTeamWithPosesssion(player):
    currentPlayersAllegiance = player[2]
    posessionTeam = player[17] 
    homeTeamAbbr = player[37]  #probably right number?
    
    if posessionTeam == homeTeamAbbr:
        teamWithBall = "home"
    else:
        teamWithBall = "away"
    
    return currentPlayersAllegiance == teamWithBall
    
def kClosest(ballCarrier, points, K):
    """
    :type points: List[List[int]]
    :type K: int
    :rtype: List[List[int]]
    """
    h = []
    heap_items = 0
    for point in points:
        x = point[0] - ballCarrier[0]
        y = point[1] - ballCarrier[1]
        dist = -1 * (x*x + y*y)
        if heap_items < K:
            heapq.heappush(h, (dist,point))
            heap_items += 1
        else:
            if dist > h[0][0]:
                heapq.heapreplace(h, (dist,point))
    result = []
    for item in h:
      result.append(item[1])
    return result

def getPlayerPosition(player):
    return [float(player[3]), float(player[4])]

for row in reader(trainingData):
    playId = row[1]
    if playId in plays:
        plays[playId].append(row) #adds players to play
    else:
        plays[playId] = [row]
    
#Fill the "play" array with stuff we think is valuable
for playId in plays.keys():
    playersInPlay = plays[playId]

    rusherId = playersInPlay[0][23] #not sure if this is right number
    
    play = [] #0-rusher, 1-playDirection, 2-rusherX, 3-rusherY, 4-rusherSpeed, 
    #5-rusherAccel, 6-rusherDir, 7-closestBadX, 8-ClosestBadY
    
    play.append(int(rusherId))
    if playersInPlay[0][28] == "left":
        play.append(0)
    else:
        play.append(1)
    
    listOfBadPlayerPositions = []
    listOfGoodPlayerPositions = []
    for player in playersInPlay:
        if isPlayerOnTeamWithPosesssion(player):
            listOfGoodPlayerPositions.append(getPlayerPosition(player)) #maybe exclude rusher?
        else:
            listOfBadPlayerPositions.append(getPlayerPosition(player))
    
    for player in playersInPlay:
        playerId = player[10]
        if playerId == rusherId:
            play.append(float(player[3])) # x position
            play.append(float(player[4])) # y position
            play.append(float(player[5])) # speed
            play.append(float(player[6])) # acceleration
            play.append(normalizeDirection(player[28], float(player[9]))) #direction
            play.extend(kClosest([float(player[3]), float(player[4])], listOfBadPlayerPositions, 1)[0]) #closest enemy's x and y
            play.append(float(player[18]))
            Y.append(float(player[7])) #distance traveled by rusher
        
    X.append(play)
    print(play)
