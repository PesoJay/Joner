#Copied from Estudio - Martin Karanitsch
from etude import Etude, Note
from random import choice


def convert_to_abc(etude: Etude) -> str:
    abc = "%%MIDI program 73\n"
    abc += "T: " + etude.title + "\n"
    abc += "M: " + etude.metre + "\n"
    abc += "L: 1/16\n"
    abc += "Q: " + '"' + etude.tempo[0] + '" 1/4=' + str(etude.tempo[1]) + "\n"
    abc += "K: " + str(etude.key) + "\n"
    
    figure_count = 0
    previous_key = str(etude.key)
    for j in range(len(etude.piece)):
       phrases = etude.piece[j].antecedent + etude.piece[j].consequent
       if str(etude.piece[j].key) != previous_key:
           abc += " [K:" + str(etude.piece[j].key) + "] "
       previous_key = str(etude.piece[j].key)
       for i in range(len(phrases)):
           for figure in phrases[i].figures:
                for note in figure.notes:
                   if note.length:
                       if note.articulation == "leg_start":
                            abc += "("
                       abc += note_to_abc(note)
                       if note.articulation == "leg_end":
                            abc += ")"
                abc += " "
                figure_count += 1
                if figure_count % etude.beats_per_measure == 0:
                   abc += "|"
       abc = abc + "]" if j == len(etude.piece)-1 else abc + "|"

    return abc


def note_to_abc(note: Note) -> str:
    abc = ""
    if note.articulation == "stacc":
        abc += "."
    abc += note.pitch.upper() if note.octave < 2 else note.pitch
    abc += "'" * max(0, note.octave-2)
    abc += str(note.length)
    return abc