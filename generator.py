#Copied from Estudio - Martin Karanitsch
from etude import Etude, Period, Key
from phrase_generator import PhraseGenerator
import focus
import utils
import constraint
from random import choice


class Generator:
    def __init__(self, etude: Etude) -> None:
        self.etude = etude
        self.etude.update_parameters()
        etude.clear()
        self.constraints = focus.get_constraints(self.etude.focus)
        self.phrase_generator = PhraseGenerator(self.etude, self.constraints)
    

    def generate_etude(self) -> Etude:
        if "equal_note_length" in self.constraints["attributes"]:
            self.constraints["allowed_note_lengths"] = [choice(self.constraints["allowed_note_lengths"])]

        parts = int(self.etude.length)
        self.etude.form = Generator.generate_form(parts)
        self.etude.harmony = Generator.generate_modulations(self.etude.form, self.etude.key)

        for i in range(parts):
            form = self.etude.form[:i]
            if self.etude.form[i] in form:
                idx = form.index(self.etude.form[i])
                period = self.etude.piece[idx]
            else:
                period = self.create_period(self.etude.harmony[i])
            self.etude.piece.append(period)

        return self.etude
    

    def generate_form(parts: int):
        parts = max(2, min(parts, 4))
        problem = constraint.Problem()
        
        problem.addVariable("a", [0])
        problem.addVariable("b", [1])

        if parts > 2:
            problem.addVariable("c", [0, 2])
        if parts > 3:
            problem.addVariable("d", [0, 2])
            problem.addConstraint(lambda x, y: x != y, ["c", "d"])

        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        elems = ["a", "b", "c", "d"]
        result = []
        for e in elems[:parts]:
            result.append(random_solution[e])

        return result
    

    def generate_modulations(form: list, key: Key):
        problem = constraint.Problem()
        elems = ["a", "b", "c", "d"]
        form_len = len(form)

        for i in range(form_len):
            problem.addVariable(elems[i], ["T", "S", "D", "TP", "SP", "DP"])

        problem.addConstraint(lambda x: x == "T", [elems[0]])
        problem.addConstraint(lambda x, y: x == y, [elems[0], elems[form_len-1]])
        if form_len > 2:
            if form[0] == form[2]:
                problem.addConstraint(lambda x: x != "S" and x != "SP", elems[1])
                problem.addConstraint(lambda x: x == "T", elems[2])
            else:
                problem.addConstraint(lambda x: x != "S" and x != "SP", elems[2])
                problem.addConstraint(lambda x, y: (
                    (x != "S" and x != "SP") or (
                        (x == "S" and y == "D") or
                        (x == "S" and y == "DP") or
                        (x == "SP" and y == "D") or
                        (x == "SP" and y == "DP")
                    )
                ), [elems[1], elems[2]])
        
        solutions = problem.getSolutions()
        random_solution = choice(solutions)
        result = []
        for i in range(form_len):
            result.append(utils.function_to_key(random_solution[elems[i]], key))

        return result
        

    def create_period(self, key: Key):
        period = Period(key)
        elems = ["a", "b", "c", "d", "e", "f", "g", "h"]
        phrase_length = self.etude.beats_per_measure * 2
        elems = elems[:phrase_length]

        phrase_a = self.phrase_generator.create_phrase(period.key, elems, 0)
        period.antecedent.append(phrase_a)
        period.consequent.append(phrase_a)

        phrase_b = self.phrase_generator.create_phrase(period.key, elems, 1, phrase_a)
        period.antecedent.append(phrase_b)

        phrase_c = self.phrase_generator.create_phrase(period.key, elems, 2, phrase_a)
        period.consequent.append(phrase_c)

        return period