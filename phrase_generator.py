#Copied from Estudio - Martin Karanitsch

from etude import Etude, Phrase, Note, Key
from figure_generator import FigureGenerator
import utils
import constraint
from random import choice
from math import ceil


class PhraseGenerator:
    def __init__(self, etude: Etude, constraints: list) -> None:
        self.etude = etude
        self.constraints = constraints
        self.figure_generator = FigureGenerator(self.constraints, self.etude.ambitus)
    

    def create_phrase(self, key: Key, elems: list, cadence: int, original_phrase: Phrase = None):
        phrase = Phrase(key)
        last_function = original_phrase.functions[len(original_phrase.functions)-1] if original_phrase else None
        phrase.functions = self.generate_functions(elems, cadence, last_function)
        phrase.degrees = self.generate_scale_degrees(phrase.functions, cadence, key.mode)

        phrase.contour = self.generate_contour(elems[:len(elems)-1])
        phrase.beats = self.generate_melody(phrase, self.constraints["phrase_allowed_intervals"], cadence)

        motif_direction = phrase.contour[0] if "long_lines" in self.constraints["attributes"] else 0
        phrase.motif = self.figure_generator.create_variation(original_phrase.motif, phrase.beats[0], motif_direction) if original_phrase else (
            self.figure_generator.create_figure(phrase.beats[0], self.etude.beat_duration, motif_direction)
        )
        phrase.figures.append(phrase.motif)
        phrase_len = len(phrase.beats)
        for i in range(1, phrase_len):
            direction = phrase.contour[i] if i < phrase_len-1 else phrase.contour[i-1]
            if motif_direction != 0 and direction != motif_direction:
                figure = self.figure_generator.translate_figure(phrase.motif, phrase.beats[i], inversion=True)
            else:
                figure = self.figure_generator.translate_figure(phrase.motif, phrase.beats[i])
            phrase.figures.append(figure)

        if cadence == 2:
            idx = phrase_len - 1
            figure = phrase.figures[idx]
            note = Note()
            note.articulation = phrase.beats[idx].articulation
            note.octave = phrase.beats[idx].octave
            note.pitch = phrase.beats[idx].pitch
            note.length = 2 if self.etude.beat_duration == 8 else 4 if self.etude.beat_duration == 4 else 8
            figure.rhythm = [note.length]
            figure.notes = [note]
        
        figure_count = len(phrase.figures)
        if "equal_articulation" in self.constraints["attributes"]:
            first_note = phrase.figures[0].notes[0]
            if first_note.articulation == "leg":
                first_note.articulation = "leg_start"
                last_figure = phrase.figures[figure_count-1]
                last_note = last_figure.notes[len(last_figure.notes)-1]
                last_note.articulation = "leg_end"
        else:
            for figure in phrase.figures:
                len_notes = len(figure.notes)
                last_articulation = ""
                for i in range(len_notes):
                    if figure.notes[i].articulation == "leg":
                        if last_articulation != "leg_start" and last_articulation != "leg":
                            figure.notes[i].articulation = "leg_start"
                        else:
                            if i == len_notes-1 or figure.notes[i+1].articulation != "leg":
                                figure.notes[i].articulation = "leg_end"
                    last_articulation = figure.notes[i].articulation                               

        return phrase


    def generate_functions(self, elems: list, cadence: int, previous_function: int = None):
        problem = constraint.Problem()
        e_len = len(elems)

        problem.addVariables(elems, [1, 4, 5])

        def successionConstraint(a, b) -> bool:
            result = (
                a == b or
                a == 1 or
                (a == 4 and b == 5) or
                (a == 5 and b == 1)
            )
            return result
        
        def previousFunctionConstraint(a) -> bool:
            if not previous_function:
                return False
            return successionConstraint(previous_function, a)
        
        match cadence:
            case 1:
                problem.addConstraint(lambda a: a == 5, [elems[e_len-1]])
                problem.addConstraint(previousFunctionConstraint, [elems[0]])
            case 2:
                problem.addConstraint(lambda a, b: a == 5 and b == 1, [elems[e_len-2], elems[e_len-1]])
                problem.addConstraint(previousFunctionConstraint, [elems[0]])
            case _:
                problem.addConstraint(lambda a: a == 1, [elems[0]])

        for i in range(e_len-1):
            problem.addConstraint(successionConstraint, [elems[i], elems[i+1]])

        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        result = []
        for i in range(e_len):
            result.append(random_solution[elems[i]])

        return result
    

    def generate_scale_degrees(self, functionalHarmony: list, cadence: int, mode: str):
        scaleDegrees = {
            "T": [1, 6],
            "S": [2, 4],
            "D": [3, 5]
        } if mode == "maj" else {
            "T": [1, 3],
            "S": [4, 6],
            "D": [5, 7]
        }
        result = []
        f_len = len(functionalHarmony)
        for i in range(f_len-cadence):
            if i == 0:
                result.append(1)
            else:
                match(functionalHarmony[i]):
                    case 1:
                        result.append(choice(scaleDegrees["T"]))
                    case 4:
                        result.append(choice(scaleDegrees["S"]))
                    case 5:
                        result.append(choice(scaleDegrees["D"]))

        if cadence >= 2:
            result.append(functionalHarmony[f_len-2])
        if cadence >= 1:
            result.append(functionalHarmony[f_len-1])

        return result


    def generate_melody(self, phrase: Phrase, intervals: list, cadence: int):
        notes =  []
        first_note = Note(utils.scale_degree_root(phrase.key, phrase.degrees[0]))
        notes.append(first_note)
        
        cutoff = 1 if cadence == 2 else 0
        for i in range(len(phrase.contour)-cutoff):
            directional_intervals = [x*(phrase.contour[i]) for x in intervals]
            pitch = self.generate_pitch(notes[i], phrase.degrees[i+1], directional_intervals)
            if pitch == None:
                directional_intervals = [x*(-1) for x in directional_intervals]
                pitch = self.generate_pitch(notes[i], phrase.degrees[i+1], directional_intervals)
            notes.append(utils.note_with_pitch(pitch))
        
        if cadence == 2:
            last_note = Note(utils.scale_degree_root(phrase.key, phrase.degrees[len(phrase.degrees)-1]))
            last_note = utils.closest_octave(last_note, notes[len(notes)-1])
            notes.append(last_note)

        last_pitch = None
        repeats = 0
        for i in range(len(notes)):
            pitch = utils.absolute_pitch(notes[i])
            if last_pitch == pitch:
                repeats += 1
                if repeats > 1:
                    pitch = choice([pitch+1, pitch-1])
                    replacement_note = utils.note_with_pitch(pitch)
                    notes[i].pitch = replacement_note.pitch
                    notes[i].octave = replacement_note.octave
                    repeats = 0
            else:
                repeats = 0
            last_pitch = pitch
        return notes


    def generate_contour(self, elems: list):
        problem = constraint.Problem()
        e_len = len(elems)

        problem.addVariables(elems, [-1, 1])

        if "long_lines" in self.constraints["attributes"]:
            middle = ceil(e_len/2)
            problem.addConstraint(lambda x, y: x != y, [elems[middle-1], elems[middle]])
            for i in range(middle-1):
                problem.addConstraint(lambda x, y: x == y, [elems[i], elems[i+1]])
            for i in range(middle, e_len-1):
                problem.addConstraint(lambda x, y: x == y, [elems[i], elems[i+1]])

        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        result = []
        for i in range(e_len):
            result.append(random_solution[elems[i]])

        return result
    
    
    def generate_pitch(self, previous_note: Note, degree: int, allowed_intervals: list):
        problem = constraint.Problem()
        previous_abs = utils.absolute_pitch(previous_note)
        valid_pitches = utils.all_pitches_of_degree(degree, self.etude.ambitus)

        problem.addVariable("a", [previous_abs])
        problem.addVariable("b", valid_pitches)

        problem.addConstraint(lambda a, b: b - a in allowed_intervals, ["a", "b"])

        solutions = problem.getSolutions()
        if len(solutions) == 0:
            return None
        random_solution = choice(solutions)

        return random_solution["b"]