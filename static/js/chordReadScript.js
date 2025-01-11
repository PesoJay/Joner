import { notes, notesFlat, noteContainer, transposeInterval, socket, addEventListeners, transpose, abcInBackButton } from "./utils.js";
const chordTypes = ["major", "minor", "sus2", "sus4", "diminished"];
//const possibleRootNotes = notes.slice(12, notes.length - 24);
//const possibleRootNotesFlat = notesFlat.slice(12, notes.length -24);
const key = document.getElementById("key").textContent;
const mode = document.getElementById("mode").textContent;
const keyChords = {
    major: [["major", "sus2", "sus4"], ["minor", "sus2", "sus4"], ["minor", "sus4"], ["major", "sus2"], ["major", "sus2", "sus4"], ["minor", "sus2", "sus4"], ["diminished"]],
    minor: [["minor", "sus2", "sus4"], ["diminished"], ["major", "sus2", "sus4"], ["minor", "sus2", "sus4"], ["minor", "sus4"], ["major", "sus2"], ["major", "sus2", "sus4"]]
};
let possibleRootNotes = [];
let notesList = notes;
let flatMode = false;

if(mode == "maj"){
    if (key.length == 2 || key == "F"){
        possibleRootNotes = notesFlat.slice(12, notesFlat.length -24);
        notesList = notesFlat;
        flatMode = true;
        console.log("Chosen Flatlist");
    } else {
        possibleRootNotes = notes.slice(12, notes.length - 24);
        console.log("Chosen SharpList");

    }
} else {
    if (key == "D" || key == "G" || key == "C" || key == "F" || key == "Bb") {
        possibleRootNotes = notesFlat.slice(12, notesFlat.length -24);
        notesList = notesFlat;
        flatMode = true;
        console.log("Chosen Flatlist");
    } else {
        possibleRootNotes = notes.slice(12, notes.length - 24);
        console.log("Chosen SharpList");
    }
}

const scaleNotes = getScaleNotes(key, mode);

console.log("Selected Key: " + key + mode);
let randomChord = { root: "", type: "", notes: [] };
let detectedChord = [];
let correctCounter = 0;
let isPaused = false;

addEventListeners();
abcInBackButton();
socket.emit("start_audio_stream");
socket.on("chord_detected", (data) => {
    if (!isPaused) {
        handleChord(data);
    }
});

randomChord = getRandomChord();
renderChord(randomChord);

function getRandomChord() {
    let diatonicChords = keyChords.major;
    if(mode == "min") {
        diatonicChords = keyChords.minor;
    }
    const randomIndex = Math.floor(Math.random() * scaleNotes.length);
    let octaveSelector = "";
    if (Math.random() < 0.5){
        octaveSelector = ",";
    }
    const root = scaleNotes[randomIndex] + octaveSelector;
    const possibleTypes = diatonicChords[randomIndex];
    const type = possibleTypes[Math.floor(Math.random() * possibleTypes.length)];
    const chordNotes = generateChordNotes(root, type);
    return { root, type, notes: chordNotes };
}

function generateChordNotes(root, type) {
    // Generate chord notes based on the type
    const semitoneSteps = {
        major: [0, 4, 7],
        minor: [0, 3, 7],
        sus2: [0, 2, 7],
        sus4: [0, 5, 7],
        diminished: [0, 3, 6]
    };

    const rootIndex = notesList.indexOf(root);
    const steps = semitoneSteps[type];
    const chordNotes = [];
    steps.forEach(step => {
        let note = notesList[rootIndex + step];
        if(note[0] == "^") {
            note = notesList[rootIndex + step - 1];
        } else if (note[0] == "_") {
            note = notesList[rootIndex + step + 1];
        }
        chordNotes.push(note);
    });
    return chordNotes;
}

function renderChord(chord) {
    let abcString = "X:1\nT:" + getChordStandardNotation(chord.root + chord.type) + "\nL:1/1\nK:" + key + mode + "\n";
    console.log("Random Chord: " + getChordStandardNotation(chord.root + chord.type) );
    let trebleNotes = [];
    let bassNotes = [];

    chord.notes.forEach(note => {
        if (notesList.indexOf(note) >= notesList.indexOf("C")) { 
            trebleNotes.push(note);
        } else {
            bassNotes.push(note);
        }
    });

    if (trebleNotes.length > 0) {
        abcString += "V:1 clef=treble\n[";
        trebleNotes.forEach(note => {
            abcString += note;
        });
        abcString += "]|\n";
    } else {
        // Add a whole rest if there are no treble notes
        abcString += "V:1 clef=treble\nz1|\n";
    }

    if (bassNotes.length > 0) {
        abcString += "V:2 clef=bass\n[";
        bassNotes.forEach(note => {
            abcString += note;
        });
        abcString += "]|\n";
    } else {
        // Add a whole rest if there are no bass notes
        abcString += "V:2 clef=bass\nz1|\n";
    }

    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        scale: 4
    });
}

function handleChord(data) {
    let transposedRoot = transpose(data["chord"][0], transposeInterval);
    if(flatMode && transposedRoot[0] == "^") {
        transposedRoot = convertToFlat(transposedRoot);
    }
    detectedChord = transposedRoot + data["chord"][1];
    console.log("Chord detected: " + detectedChord);
    if (isChordAccurate(detectedChord)) {
        correctChordRoutine();
    } else {
        wrongChordRoutine();
    }
}

function correctChordRoutine() {
    correctCounter++;
    document.getElementById("correct-counter").textContent = correctCounter;
    colorChord(true);
    isPaused = true;
    setTimeout(() => {
        isPaused = false;
        randomChord = getRandomChord();
        renderChord(randomChord);
    }, 500);
}

function wrongChordRoutine() {
    colorChord(false);
}

function colorChord(isChordCorrect) {
    const chordElements = noteContainer.querySelectorAll(".abcjs-note");
    let color = "red";
    if(isChordCorrect) {
        color = "green";
    }
    chordElements[0].style.color = color;
    if(chordElements[1]){
        chordElements[1].style.color = color;
    }
}

function getScaleNotes(key, type) {
    const scaleSteps = [0, 2, 4, 5, 7, 9, 11];
    if (type === "min") {
        scaleSteps[2] = 3;
        scaleSteps[5] = 8;
        scaleSteps[6] = 10;
    }

    const rootIndex = possibleRootNotes.indexOf(standardToABCNotation(key));
    let scaleNotes = [];
    scaleSteps.forEach((step) => {
        scaleNotes.push(normalizeNote(notesList[(rootIndex + step) % notesList.length]));
    });
    return scaleNotes;
}

function convertToFlat(note) {
    let index = notes.indexOf(note);
    return notesFlat[index];
}

function normalizeNote(note) {
    note = note.replace(/[,']/g, "");
    note = note.toUpperCase();
    return note;
}

function standardToABCNotation(note) {
    let accidental = "";
    if (note[1] == "#") {
        note = note.slice(0, 1);
        accidental = "^";
    } else if (note[1] == "b") {
        note = note.slice(0, 1);
        accidental = "_";
    }
    return accidental + note;
}

function getChordStandardNotation(chord) {
    chord = chord.replace(/[,']/g, "");
    chord = chord.toLowerCase();
    let accidental = "";
    if (chord[0] == "^") {
        chord = chord.slice(1);
        accidental = "#";
    } else if (chord[0] == "_") {
        chord = chord.slice(1);
        accidental = "b";
    }
    let chordRoot = chord.charAt(0).toUpperCase();
    let chordType = chord.slice(1);
    chord = chordRoot + accidental + chordType;

    return chord;
}

function isChordAccurate(chord) {
    return getChordStandardNotation(chord) === getChordStandardNotation(randomChord.root + randomChord.type);
}
