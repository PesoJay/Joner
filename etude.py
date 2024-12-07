#Copied from Estudio - Martin Karanitsch
from random import choice, randint


class Key:
    def __init__(self, pitch: str = "", symbol: str = "", mode: str = "") -> None:
        self.pitch = pitch
        self.symbol = symbol
        self.mode = mode


    def __repr__(self) -> str:
        return self.pitch.upper() + self.symbol + self.mode
    

class Etude:
    def __init__(self) -> None:
        self.title: str = None
        self.metre: str = None
        self.key: Key = None
        self.beats_per_measure = None
        self.beat_duration = None
        self.tempo = None
        self.focus: str = None
        self.length: int = None
        self.ambitus = None
        self.form = []
        self.harmony = []
        self.piece = []


    def __repr__(self) -> str:
        period_str = ""
        for period in self.piece:
            period_str += str(period)
        return period_str
    

    def set_tempo(self, tempo: str) -> None:
        if tempo == "random":
            tempo = choice(["very_slow", "slow", "moderate", "fast", "very_fast"])
        match(tempo):
            case "very_slow":
                self.tempo = ["Largo", randint(50, 69)]
            case "slow":
                self.tempo = ["Andante", randint(70, 89)]
            case "moderate":
                self.tempo = ["Moderato", randint(90, 109)]
            case "fast":
                self.tempo = ["Allegro", randint(110, 129)]
            case "very_fast":
                self.tempo = ["Presto", randint(130, 150)]
    

    def set_key(self, key: str, mode: str) -> None:
        if mode == "random":
            mode = choice(["maj", "min"])
        if key == "random" and mode == "maj":
            key = choice(["C", "G", "F", "D", "Bb", "A", "Eb", "E", "Ab", "B", "Db"])
        elif key == "random" and mode == "min":
            key = choice(["A", "E", "D", "B", "G", "F#", "C", "F", "C#", "Bb", "G#"])
        
        pitch = key[:1]
        symbol = key[1:] if key[1:] else ""
        self.key = Key(pitch, symbol, mode)


    def update_parameters(self) -> None:
        if self.metre == "random":
            self.metre = choice(["2/4", "3/4", "4/4"])
        self.beats_per_measure = int(self.metre[0])
        self.beat_duration = int(self.metre[2])
        if self.length == "random":
            self.length = choice([2, 3, 4])
        if self.title == "":
            self.title = "Study in " + self.key.pitch + self.key.symbol
            self.title += " major" if self.key.mode == "maj" else " minor"
        if self.focus == "random":
            self.focus = choice(["tonguing", "air_column", "articulation", "register_change", "technique"])
    

    def apply_difficulty(self, difficulty: str) -> None:
        mode = choice(["maj", "min"])
        if difficulty == "random":
            difficulty = choice(["beginner", "advanced", "expert"])
        match(difficulty):
            case "beginner":
                self.ambitus = [0, 16]
                self.metre = "4/4"
                self.tempo = choice(["very_slow", "slow"])
                key = choice(["C", "G", "F"]) if mode == "maj" else choice(["A", "E", "D"])
            case "advanced":
                self.ambitus = [0, 19]
                self.metre = choice(["2/4", "3/4", "4/4"])
                self.tempo = choice(["slow", "moderate", "fast"])
                key = choice(["D", "A", "Bb", "Eb"]) if mode == "maj" else choice(["B", "G", "F#", "C"])
            case "expert":
                self.ambitus = [0, 22]
                self.metre = choice(["2/4", "3/4", "4/4"])
                self.tempo = choice(["fast", "very_fast"])
                key = choice(["E", "Ab", "B", "Db"]) if mode == "maj" else choice(["F", "C#", "Bb", "G#"])
        pitch = key[:1]
        symbol = key[1:] if key[1:] else ""
        self.key = Key(pitch, symbol, mode)
        self.set_tempo(self.tempo)


    def clear(self) -> None:
        self.form = []
        self.harmony = []
        self.piece = []


class Period:
    def __init__(self, key: Key) -> None:
        self.key = key
        self.antecedent = []
        self.consequent = []
    

    def __repr__(self) -> str:
        phrase_str = "{"
        for phrase in self.antecedent:
            phrase_str += str(phrase)
        phrase_str += ","
        for phrase in self.consequent:
            phrase_str += str(phrase)
        phrase_str += "}"
        return phrase_str
    

    def get_phrases(self):
        return self.antecedent + self.consequent


class Phrase:
    def __init__(self, key: Key) -> None:
        self.key = key
        self.functions = None
        self.degrees = None
        self.contour = None
        self.beats = None
        self.figures = []
        self.motif: Figure = None


    def __repr__(self) -> str:
        figure_str = "["
        for figure in self.figures:
            figure_str += str(figure) + " "
        figure_str += "]"
        return figure_str

 
class Figure:
    def __init__(self) -> None:
        self.rhythm = None
        self.notes = []
    

    def __repr__(self) -> str:
        note_str = ""
        for note in self.notes:
            note_str += str(note) + "-"
        return note_str


class Note:
    def __init__(self, pitch: str = "c", 
                 octave: int = 2, 
                 length: int = 4, 
                 articulation: str = None) -> None:
        self.pitch = pitch.lower()
        self.octave = octave
        self.length = length
        self.articulation = articulation
    

    def __repr__(self) -> str:
        note_str = ""
        if self.articulation == "stacc":
            note_str += "°"
        elif self.articulation == "leg_start":
            note_str += "("
        elif self.articulation == "leg":
            note_str += "~"
        note_str += self.pitch.upper() + str(self.octave)
        if self.articulation == "leg_end":
            note_str += ")"
        return note_str