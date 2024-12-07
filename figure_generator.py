#Copied from Estudio - Martin Karanitsch
from etude import Note, Figure
from random import choice
import utils
import constraint


class FigureGenerator:
    def __init__(self, constraints: list, ambitus: list) -> None:
        self.constraints = constraints
        self.ambitus = ambitus


    def create_figure(self, start_note: Note, beat_duration: int, direction: int):
        figure = Figure()
        figure_length = 2 if beat_duration == 8 else 4 if beat_duration == 4 else 8
        rhythm = self.generate_rhythm(self.constraints["allowed_note_lengths"], figure_length)
        figure.rhythm = [x for x in rhythm if x != 0]
        if "equal_articulation" in self.constraints["attributes"]:
            articulation_type = choice(self.constraints["allowed_articulation"])
            articulation = []
            for i in range(len(figure.rhythm)):
                articulation.append(articulation_type)
        else:
            articulation = self.generate_articulation(self.constraints["allowed_articulation"], len(figure.rhythm))

        had_jump = False
        for i in range(len(figure.rhythm)):
            jump = True if i == len(figure.rhythm)-1 and not had_jump else choice([True, False]) 
            if i == 0:
                pitch = utils.absolute_pitch(start_note)
            else:
                intervals = self.constraints["figure_allowed_intervals"]
                if "large_jumps" in self.constraints["attributes"] and jump and not had_jump:
                    had_jump = True
                    intervals = [-8, -7, -6, 6, 7, 8]
                pitch = self.generate_pitch(figure.notes[i-1], intervals, direction)

            note = utils.note_with_pitch(pitch)
            note.length = figure.rhythm[i]
            note.articulation = articulation[i]
            figure.notes.append(note)

        return figure


    def generate_rhythm(self, allowed_note_lengths: list, figure_length: int):
        problem = constraint.Problem()
        elems = ["a", "b", "c", "d", "e", "f", "g", "h"]
        elems = elems[:figure_length]

        lengths = [0] + allowed_note_lengths
        problem.addVariables(elems, lengths)

        problem.addConstraint(constraint.ExactSumConstraint(figure_length))
        problem.addConstraint(lambda a: a != 0, [elems[0]])
        for i in range(figure_length):
            if i % 2 != 0:
                problem.addConstraint(lambda a: a != 2, [elems[i]]) 
                problem.addConstraint(lambda a, b: (
                    (a + b == 2) or 
                    (a + b == 0) or 
                    (a > 2 and b == 0)
                ), [elems[i-1], elems[i]])
            if figure_length >= 4 and i % 4 != 0:
                problem.addConstraint(lambda a: a != 4, [elems[i]])
            if figure_length >= 8 and i % 8 != 0:
                problem.addConstraint(lambda a: a != 8, [elems[i]])
        
        def minLengthThreeConstraint(*args):
            vals = []
            for a in args:
                if a != 0:
                    vals.append(a)
            if len(vals) > 2:
                return True
            return False
        
        if "min_figure_length_three" in self.constraints["attributes"]:
            problem.addConstraint(minLengthThreeConstraint, elems)

        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        result = []
        for i in range(figure_length):
            result.append(random_solution[elems[i]])

        return result
    

    def generate_articulation(self, allowed_articulation: list, figure_length: int):
        problem = constraint.Problem()
        elems = ["a", "b", "c", "d", "e", "f", "g", "h"]
        elems = elems[:figure_length]
        problem.addVariables(elems, allowed_articulation)

        if figure_length == 1:
            problem.addConstraint(lambda a: a != "leg", [elems[0]])
        if figure_length == 2:
            problem.addConstraint(lambda a, b: a == b, [elems[0], elems[1]])
        if figure_length > 2:
            problem.addConstraint(lambda a, b: a == "stacc" or a == b, [elems[0], elems[1]])
            problem.addConstraint(lambda a, b: b == "stacc" or b == a, [elems[figure_length-2], elems[figure_length-1]])
            for i in range(figure_length-2):
                problem.addConstraint(lambda a, b, c: (
                    (b != "leg") or
                    (a == "leg" and b == "leg") or
                    (b == "leg" and c == "leg")
                ), [elems[i], elems[i+1], elems[i+2]])
        
        def notAllEqualConstraint(*args):
            vals = []
            for a in args:
                if not a in vals:
                    vals.append(a)
            if len(vals) > 1:
                return True
            return False

        if "articulation_change" in self.constraints["attributes"]:
            problem.addConstraint(notAllEqualConstraint, elems)

        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        result = []
        for i in range(figure_length):
            result.append(random_solution[elems[i]])

        return result
    

    def generate_pitch(self, previous_note: Note, allowed_intervals: list, direction: int = 0, next_note: Note = None) -> int:
        problem = constraint.Problem()
        previous_abs = utils.absolute_pitch(previous_note)

        problem.addVariable("a", [previous_abs])
        problem.addVariable("b", range(self.ambitus[0], self.ambitus[1]))

        def sign(x: int) -> int:
            return 0 if abs(x) == 0 else x/abs(x)

        problem.addConstraint(lambda a, b: b - a in allowed_intervals, ["a", "b"])
        if direction != 0:
            problem.addConstraint(lambda a, b: sign(b - a) == direction, ["a", "b"])

        if next_note:
            next_abs = utils.absolute_pitch(next_note)
            problem.addVariable("c", [next_abs])
            problem.addConstraint(lambda a, b: b - a in allowed_intervals, ["b", "c"])

        solutions = problem.getSolutions()
        random_solution = choice(solutions)

        return random_solution["b"]
    

    def translate_figure(self, figure: Figure, beat: Note, inversion: bool = False):
        new_figure = Figure()
        direction = -1 if inversion else 1

        for i in range(len(figure.notes)):
            if i == 0:
                new_pitch = utils.absolute_pitch(beat)
            else:
                interval = utils.distance(figure.notes[i-1], figure.notes[i])
                new_pitch = utils.absolute_pitch(new_figure.notes[i-1]) + (interval * direction)
                if not new_pitch in range(self.ambitus[0], self.ambitus[1]):
                    new_pitch = utils.absolute_pitch(beat) - (interval * direction)

            new_note = utils.note_with_pitch(new_pitch)
            new_note.articulation = figure.notes[i].articulation
            if new_note.articulation == "leg_start" or new_note.articulation == "leg_end":
                new_note.articulation = "leg"
            new_note.length = figure.notes[i].length
            new_figure.notes.append(new_note)
        
        return new_figure


    def create_variation(self, figure: Figure, beat: Note, direction: int = 0):
        new_figure = Figure()
        new_figure.rhythm = figure.rhythm

        had_jump = False
        for i in range(len(new_figure.rhythm)):
            jump = True if i == len(new_figure.rhythm)-1 and not had_jump else choice([True, False]) 
            if i == 0:
                pitch = utils.absolute_pitch(beat)
            else:
                intervals = self.constraints["figure_allowed_intervals"]
                if "large_jumps" in self.constraints["attributes"] and jump and not had_jump:
                    had_jump = True
                    intervals = [-8, -7, -6, 6, 7, 8]
                pitch = self.generate_pitch(new_figure.notes[i-1], intervals, direction)

            note = utils.note_with_pitch(pitch)
            note.length = figure.rhythm[i]
            note.articulation = figure.notes[i].articulation
            if note.articulation == "leg_start" or note.articulation == "leg_end":
                note.articulation = "leg"
                
            new_figure.notes.append(note)

        return new_figure