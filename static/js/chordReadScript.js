import { notes, noteContainer, transposeInterval, socket, addEventListeners, transpose, abcInBackButton } from "./utils.js";
const chordTypes = ["major", "minor", "sus2", "sus4", "diminished", "augmented"];
const validRootNotes = notes.slice(12, notes.length - 20);
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

function getRandomChord() {
    const root = validRootNotes[Math.floor(Math.random() * validRootNotes.length)];
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
    let abcString = "X:1\nM:4/4\nL:1/1\nK:C\n";

    // Separate notes into treble and bass voices
    let trebleNotes = [];
    let bassNotes = [];

    chord.notes.forEach(note => {
        // Determine whether the note is above or below middle C
        console.log("indes of note: " + notes.indexOf(note))
        console.log("index of C4: " + notes.indexOf("C"));
        if (notes.indexOf(note) >= notes.indexOf("C")) { 
            trebleNotes.push(note);
        } else {
            bassNotes.push(note);
        }
    });

    // Handle the treble voice
    if (trebleNotes.length > 0) {
        abcString += "V:1 clef=treble\n|[";
        trebleNotes.forEach(note => {
            abcString += note;
        });
        abcString += "]|\n";
    } else {
        // Add a whole rest if there are no treble notes
        abcString += "V:1 clef=treble\n|z1|\n";
    }

    // Handle the bass voice
    if (bassNotes.length > 0) {
        abcString += "V:2 clef=bass\n|[";
        bassNotes.forEach(note => {
            abcString += note;
        });
        abcString += "]|\n";
    } else {
        // Add a whole rest if there are no bass notes
        abcString += "V:2 clef=bass\n|z1|\n";
    }

    // Render the ABC string
    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        scale: 4
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
    if(chordElements[1]){
        chordElements[1].style.color = color;
    }
}

function isChordAccurate(chord) {
    return chord === randomChord.root + randomChord.type;
}
