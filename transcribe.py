import keyboard, json

ONST = "12345qwert"
NCLS = "cvbnm"
CODA = "09876poiuy"

BIT = [{alpha[a]: 10**a for a in range(len(alpha))} for alpha in [ONST, NCLS, CODA]]

with open("symbol.json", 'r', encoding = 'utf-8') as f:
    SYMBOL = json.load(f)

with open("pronunciation.json", 'r') as f:
    CMU = json.load(f)

def findWord(word):

    if word in CMU:
        return CMU[word]
    
    return None

class Transcription:

    def __init__(self):

        self.pressed = set()
        self.english = None
        self.word = []
    
    def addKey(self, key: keyboard.KeyboardEvent):

        self.pressed.add(key.name)
        # print(self.pressed)
    
    def removeKey(self, key: keyboard.KeyboardEvent):

        syll = [sum(part[a] for a in self.pressed if a in part) for part in BIT]
        done = "space" in self.pressed
        self.pressed = set()

        if sum(syll) > 0:
            print(syll)

        for i, n in enumerate(["onset", "nucleus", "coda"]):
            if str(syll[i]) in SYMBOL[n]:
                self.word.append(SYMBOL[n][str(syll[i])])

        if done:
            print(self.word)
            self.english = findWord(' '.join(self.word))
            self.word = []
    
    def getWord(self):

        if self.english:
            toret = self.english
            self.english = None
            return toret
        
        return None
    
    def isDone(self):

        return "esc" in self.pressed

if __name__ == "__main__":

    t = Transcription()

    keyboard.on_press(t.addKey, suppress = True)
    keyboard.on_release(t.removeKey, suppress = True)

    while not t.isDone():
        if w := t.getWord():
            print(w)