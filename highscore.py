class HighScore(object):
    """High score"""

    def __init__(self, config):

        self.config = config
        self.result = 0
        self.state = 'init'
        self.currentLetter = 'A'
        self.currentPos = 0
        self.name = ''
        self.upPressed = False
        self.downPressed = False
        self.rightPressed = False
        self.leftPressed = False
        self.nextPressed = False
        self.highScore = []
        self.showCount = 10

    def reset(self, mode, result):
        self.currentLetter = 'A'
        self.currentPos = 0
        self.name = ''

        self.result = result
        self.text = ""

        self.state = 'enter'

        #load highScore file

        with open("highscore.txt", 'rw') as highScoreFile:
        #    lines = highScoreFile.readlines()
            line = highScoreFile.readline()
            self.highScore = []
            while line != '':
                score = line
                name = highScoreFile.readline()
                name = name.rstrip('\n')
                self.highScore.append((int(score), name ))

                line = highScoreFile.readline()

        self.highScore.sort(None, None, True)

        posInScore = 1
        for x in self.highScore:
            if x[0] < self.result:
                break
            posInScore += 1


        #for x in lines:
        #    splited = x.split(' ')
        #    splited.pop(0)
        #    name = ''.join(splited)

    def inHighScore(self, score):

        return True

    def processControl(self, events):
        if 'drag' not in events:
            self.nextPressed = False

        if 'drag' in events and not self.nextPressed:
            if self.state == 'enter':
                self.highScore.append((int(self.result), self.name))
                self.highScore.sort(None, None, True)
                with open("highscore.txt", 'w') as highScoreFile:
                    for touple in self.highScore:
                        highScoreFile.write(str(touple[0]) + '\n')
                        highScoreFile.write(touple[1] + '\n')
                self.state = 'show'
            elif self.state == 'show':
                self.state = 'ending'
            self.nextPressed = True

        if 'up' not in events:
            self.upPressed = False
        if 'down' not in events:
            self.downPressed = False
        if 'left' not in events:
            self.leftPressed = False
        if 'right' not in events:
            self.rightPressed = False

        for ev in events:
            if ev == 'up' and not self.upPressed:
                self.upPressed = True
                self.currentLetter = chr(ord(self.currentLetter) + 1)
            if ev == 'down' and not self.downPressed:
                self.downPressed = True
                self.currentLetter = chr(ord(self.currentLetter) - 1)
            if ev == 'left' and not self.leftPressed:
                self.leftPressed = True
                self.currentPos -= 1
                if self.currentPos < 0 :
                    self.currentPos = 0
                name = list(self.name)
                self.currentLetter = name[self.currentPos]

            if ev == 'right' and not self.rightPressed:
                self.rightPressed = True
                if self.currentPos < 10:
                    self.currentPos += 1
                if len(self.name) <= self.currentPos:
                    self.currentLetter = 'A'
                else:
                    name = list(self.name)
                    self.currentLetter = name[self.currentPos]


    def process(self, view, events):

        self.processControl(events)

        if self.currentPos == len(self.name) :
            self.name += ' '
        name = list(self.name)
        name[self.currentPos] = self.currentLetter
        self.name = ''.join(name)

        if self.state == 'ending':
            return 'ending'

        if self.state == 'show':
            self.showResults(view)

        if self.state == 'enter':
            self.enterName(view)

        return 'highScore'


    def showResults(self, view):
        view.draw_text('High Score', (0, 180, 0), 30, (20, 60))
        for x in range(min(self.showCount, len(self.highScore))):
            fh = 32
            view.draw_text(str(x+1) + '. ' + str(self.highScore[x][0]) + ' ' + self.highScore[x][1], (0, 180, 0), 30, (20, 120 + fh*x))

    def enterName(self, view):
        view.draw_text('SCORE: ' + str(int(self.result)), (0, 180, 0), 30, (20, 60))
        view.draw_text('Enter name: ' + self.name, (0, 180, 0), 30, (20, 150))

        fw = 21
        view.draw_text('_', (0, 180, 0), 30, (270 + fw*self.currentPos, 152))


    def wait(self, view):
        """If player finds exit, ask for new game."""

        self.text = self.config.waiting_text
        self.draw_text(view)


    def draw_text(self, view):

        view.draw_text(self.text)


    def quit(self):

        print("Bye")
