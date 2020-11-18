import keyboard, json

ONST = "12345qwert"
NCLS = "cvbnm"
CODA = "09876poiuy"

BIT = [{alpha[a]: 10**a for a in range(len(alpha))} for alpha in [ONST, NCLS, CODA]]

with open("symbol.json", 'r', encoding = 'utf-8') as f:
    SYMBOL = json.load(f)

with open("cmu.json", 'r') as f:
    CMU = json.load(f)

def findWord(word):

    if word in CMU:
        return CMU[word]
    
    return {f"[{word.replace(' ', '')}]": 0}

class Transcription:

    def __init__(self):

        self.pressed = set()
        self.english = None
        self.word = []
        self.history = []
        self.last = []
        self.newword = True
    
    def addKey(self, key: keyboard.KeyboardEvent):

        if key.name == "backspace":
            if len(self.history):
                self.deleteLast()
                self.last = []
            return
        
        if key.name == "`":
            keyboard.press(' ')
            return
        
        if key.name in "[]":
            if len(self.last) > 1:
                self.shiftLast(key.name == '[')

        self.pressed.add(key.name)
        # print(self.pressed)
    
    def removeKey(self, key: keyboard.KeyboardEvent):

        syll = [sum(part[a] for a in self.pressed if a in part) for part in BIT]
        done = "space" in self.pressed
        self.pressed = set()

        if not sum(syll) and done and not len(self.word):
            keyboard.press("backspace")
            keyboard.write(".  ")
            self.history.append(2)
            return

        if sum(syll) > 0:
            print(syll)

        for i, n in enumerate(["onset", "nucleus", "coda"]):
            if str(syll[i]) in SYMBOL[n]:
                self.word.append(SYMBOL[n][str(syll[i])])

        if done:
            print(self.word)
            print(' '.join(self.word))
            
            results = findWord(' '.join(self.word))
            print(results)

            if results == {' '.join(self.word): 0}:
                if self.word[-1] == 'S':
                    results = findWord(' '.join(self.word[:-1]) + ' Z')
                if self.word[-1] == 'L':
                    results = findWord(' '.join(self.word[:-1]) + ' AH L')
            
            self.last = sorted(results, key = lambda x : results[x], reverse = True)

            print(self.last)
            self.english = len(self.last) > 0
            self.word = []
    
    def writeWord(self):

        if self.english:
            keyboard.write(self.last[0].lower() + " ")
            print(len(self.last[0]))
            self.history.append(len(self.last[0]) + 1)
            self.english = None
    
    def isDone(self):

        return "esc" in self.pressed
    
    def deleteLast(self):

        for i in range(self.history[-1]):
            keyboard.press("backspace")
        del self.history[-1]
    
    def shiftLast(self, moreLikely = True):

        if len(self.last):

            self.deleteLast()

            if moreLikely:
                self.last.insert(0, self.last[-1])
                del self.last[-1]
            
            else:
                self.last.append(self.last[0])
                del self.last[0]
            
            self.english = True

if __name__ == "__main__":

    t = Transcription()

    keyboard.on_press(t.addKey, suppress = True)
    keyboard.on_release(t.removeKey, suppress = True)

    while not t.isDone():
        t.writeWord()