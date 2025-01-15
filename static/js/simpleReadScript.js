import { notes, noteContainer, transposeInterval, socket, addEventListeners, transpose, abcInBackButton } from "./utils.js";
const validRandomNotes = notes.slice(24, notes.length - 8);
let randomNote = "";
let detectedNote = "";
let correctCounter = 0;
let lastNotes = ["X", "X"];
let isPaused = false;

addEventListeners();
abcInBackButton();
socket.emit("start_audio_stream");
socket.on("note_detected", (data) => {
    if(!isPaused){
        handleNote(data);
    }
});

randomNote = "C";
const currentNotes = [randomNote];
renderNotes(currentNotes);

function getRandomNote(previousNote) {
    let newNote = "";
    do {
      newNote = validRandomNotes[Math.floor(Math.random() * validRandomNotes.length)];
    } while (newNote === previousNote);
    return newNote;
}

function renderNotes(currentNotes) {
    let abcString = "X:1\nM:4/4\nL:1/1\nK:C\n";
    abcString += "|[";

    currentNotes.forEach((note) => {
        abcString += note;
    });
    abcString += "]|";

    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        scale: 6
    });
}

function handleNote(data) {
    detectedNote = transpose(data.note, transposeInterval);
    if(lastNotes.length > 2) {
        lastNotes.shift();
    }
    lastNotes.push(detectedNote);
    if(isNoteAccurate(detectedNote)) {
        currentNotes[1] = detectedNote;
        console.log(`Detected Note: ${data.note}`);
        if (detectedNote === randomNote){
            correctNoteRoutine();
        } else {
            wrongNoteRoutine();
        }
    }
}

function correctNoteRoutine() {
    correctCounter++;
    document.getElementById("correct-counter").textContent = correctCounter;
    currentNotes[1] = "";
    renderNotes(currentNotes);    
    colorNote(true);
    isPaused = true;
    setTimeout(() => {
        isPaused = false;
        randomNote = getRandomNote(randomNote);
        currentNotes[0] = randomNote;
        currentNotes[1] = "";
        lastNotes = ["X", "X"];
        renderNotes(currentNotes);
    }, 500);
}

function wrongNoteRoutine() {
    renderNotes(currentNotes);    
    colorNote(false);
}

function colorNote(isNoteCorrect) {
    const chord = noteContainer.querySelector(".abcjs-note");
    let color = "red";
    if(isNoteCorrect) {
        color = "green";
    }
    chord.childNodes.forEach((childNode) => {
        if(childNode.dataset.name === detectedNote){
            childNode.style.fill = color;
        }
    });
}

function isNoteAccurate(note) {
    return(lastNotes.every(isDetectedNote));
}

const isDetectedNote = (note) => note === detectedNote;