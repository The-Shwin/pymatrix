from random import randint
from place import Place
from someone import Someone
from time import sleep
import sys

class Matrix:
    def __init__(self, eventPerLine, startX, endX, startY, endY, placesNumber, startPeople):
        self.eventPerLine = eventPerLine
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        self.usedCases = []
        self.limit = (endX - startX) * (endY - startX) - placesNumber
        self.workplaces = []
        self.malls = []
        self.people = []
        self.events = ['B','W','S']
        self.startPeople = startPeople
        for _ in range(placesNumber+1):
            placeType = randint(1, 2)
            coords = self.generateCoords()

            if placeType == 1:
                self.workplaces.append(Place(coords[0], coords[1]))
            else:
                self.malls.append(Place(coords[0], coords[1]))
    
    # Generate coords that are not already used
    def generateCoords(self):
        x = 0
        y = 0
        while x in self.usedCases or y in self.usedCases:
            x = randint(self.startX, self.endX)
            y = randint(self.startY, self.endY)
        self.usedCases.append(x)
        self.usedCases.append(y)
        return [x, y]

    """ 
    # Print generated places
    def showPlaces(self):
        print('--- Workplaces ---')
        for workplace in self.workplaces:
            workplace.showCoords()
        print('--- Malls ---')
        for mall in self.malls:
            mall.showCoords()
    """

    # Get random events
    def getEvent(self):
        i = randint(0, len(self.events)-1)
        return self.events[i]

    # Get random workplace
    def getWorkplace(self):
        i = randint(0, len(self.workplaces)-1)
        return self.workplaces[i]

    # Get random mall
    def getMall(self):
        i = randint(0, len(self.malls)-1)
        return self.malls[i]

    # Generate and plays random event on random people
    def randomEvent(self):
        event = self.getEvent()

        if len(self.people) < self.startPeople:
            event = 'B'
        else:
            someone = self.people[randint(0, len(self.people))-1]
            if someone.partner == False:
                while event == 'B':
                    event = self.getEvent()
                    
            if event == 'W':
                if someone.x == someone.workplace.x and someone.y == someone.workplace.y:
                    coords = someone.goToHome()
                    print(coords[0],':',coords[1],':',someone.identifiant,':H/')
                else:
                    coords = someone.goToWork()
                    print(coords[0],':',coords[1],':',someone.identifiant,':W/')
            elif event == 'S':
                if someone.x == someone.mall.x and someone.y == someone.mall.y:
                    coords = someone.goToHome()
                    print(coords[0],':',coords[1],':',someone.identifiant,':H/')
                else:
                    coords = someone.goToShop()
                    print(coords[0],':',coords[1],':',someone.identifiant,':S/')

        if event == 'B':
            if len(self.people)+1 < (self.limit - len(self.people)):
                coords = self.generateCoords()
                someone = Someone(len(self.people)+1, coords[0], coords[1], self.getMall(), self.getWorkplace())
                self.people.append(someone)
                print(coords[0],':',coords[1],':',someone.identifiant,':',event,'/')
            else:
                print('Too much people there')

    # Make people meet each other
    def meetPeople(self):
        peopleCoords = {}
        for someone in self.people:
            coords = str(someone.x)+':'+str(someone.y)
            if coords in peopleCoords:
                for identifiant in peopleCoords[coords]:
                    for somebody in self.people:
                        if somebody.identifiant == identifiant:
                            if someone.isNotInRelationWith(identifiant):
                                chance = randint(1, 10)
                                if chance <= 6:
                                    someone.nothingSpecials.append(identifiant)
                                    somebody.nothingSpecials.append(someone.identifiant)
                                    print(someone.x,':',someone.y,':',someone.identifiant,':M',somebody.identifiant,'/')
                                    #print(someone.identifiant,' become nothing with ', identifiant)
                                elif chance > 6 and chance < 9:
                                    someone.friends.append(identifiant)
                                    somebody.friends.append(someone.identifiant)
                                    print(someone.x,':',someone.y,':',someone.identifiant,':M',somebody.identifiant,'/')
                                    #print(someone.identifiant, " become friend with ",identifiant)
                                elif chance == 10:
                                    if someone.partner == False:
                                        someone.partner = identifiant
                                        somebody.partner = someone.identifiant
                                        print(someone.x,':',someone.y,':',someone.identifiant,':P',somebody.identifiant,'/')
                                    else:
                                        someone.friends.append(identifiant)
                                        somebody.friends.append(someone.identifiant)
                                        print(someone.x,':',someone.y,':',someone.identifiant,':M',somebody.identifiant,'/')
                                        #print(someone.identifiant, " become friend with ",identifiant)

                peopleCoords[coords].append(someone.identifiant)
            else:
                peopleCoords[coords] = [someone.identifiant]

def main():
    print('Hello ...')
    sleep(0.5)
    print('Welcome in the Mytrix')
    # World coords have to be positive
    world = Matrix(5, 0, 200, 0, 200, 20, 20)
    round = 0
    while 1==1:
        round += 1
        world.randomEvent()
        world.meetPeople()
        #world.older()
        #world.kill()
        sleeptime = randint(200, 800)
        sleep(sleeptime/1000)

if __name__ == '__main__':
    main()