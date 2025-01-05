import { notes, noteContainer, transposeInterval, socket, addEventListeners, transpose } from "./utils.js";
const chordTypes = ["major", "minor", "sus2", "sus4", "diminished", "augmented"];
let randomChord = { root: "", type: "", notes: [] };
let detectedChord = [];
let correctCounter = 0;
let isPaused = false;

addEventListeners();
socket.emit("start_audio_stream");
socket.on("chord_detected", (data) => {
    if (!isPaused) {
        handleChord(data);
    }
});

function getRandomChord() {
    const root = notes[Math.floor(Math.random() * 12)];
    const type = chordTypes[Math.floor(Math.random() * chordTypes.length)];
    const chordNotes = generateChordNotes(root, type);
    console.log(root + type);
    return { root, type, notes: chordNotes };
}

function generateChordNotes(root, type) {
    // Generate chord notes based on the type
    const semitoneSteps = {
        major: [0, 4, 7],
        minor: [0, 3, 7],
        sus2: [0, 2, 7],
        sus4: [0, 5, 7],
        diminished: [0, 3, 6],
        augmented: [0, 4, 8]
    };

    const rootIndex = notes.indexOf(root);
    const steps = semitoneSteps[type];
    const chordNotes = [];
    steps.forEach(step => {
        chordNotes.push(notes[rootIndex + step])
    });
    return chordNotes;
}

function renderChord(chord) {
    let abcString = "X:1\nT:Chord Practice\nM:4/4\nL:1/1\nK:C\n";
    abcString += "|[";

    chord.notes.forEach(note => {
        abcString += note;
    });
    abcString += "]|";

    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        staffwidth: 500
    });
}

randomChord = getRandomChord();
renderChord(randomChord);

function handleChord(data) {
    let transposedRoot = transpose(data["chord"][0], transposeInterval);
    detectedChord = transposedRoot + data["chord"][1];
    console.log(detectedChord);
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
    console.log(chordElements);
    let color = "red";
    if(isChordCorrect) {
        color = "green";
    }
    chordElements[0].style.color = color;
}

function isChordAccurate(chord) {
    return chord === randomChord.root + randomChord.type;
}
