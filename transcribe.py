import keyboard, json

ONST = "12345qwert"
NCLS = "cvbnm"
CODA = "09876poiuy"

BIT = [{alpha[a]: 10**a for a in range(len(alpha))} for alpha in [ONST, NCLS, CODA]]

with open("symbol.json", 'r', encoding = 'utf-8') as f:
    SYMBOL = json.load(f)

print(SYMBOL)

class Transcription:

    def __init__(self):

        self.pressed = set()
    
    def addKey(self, key: keyboard.KeyboardEvent):

        self.pressed.add(key.name)
        # print(self.pressed)
    
    def removeKey(self, key: keyboard.KeyboardEvent):

        syll = [sum(part[a] for a in self.pressed if a in part) for part in BIT]
        self.pressed = set()

        if sum(syll) > 0:
            print(syll)

        toret = ""

        for i, n in enumerate(["onset", "nucleus", "coda"]):
            if str(syll[i]) in SYMBOL[n]:
                toret += SYMBOL[n][str(syll[i])]
        
        if len(toret):
            print(toret)
    
    def isDone(self):

        return "esc" in self.pressed

if __name__ == "__main__":

    t = Transcription()

    keyboard.on_press(t.addKey, suppress = True)
    keyboard.on_release(t.removeKey, suppress = True)

    while not t.isDone():
        pass