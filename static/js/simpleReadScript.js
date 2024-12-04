const notes = ["F,", "^F,", "G,", "^G,", "A,", "^A,", "B,", "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B", "c", "^c", "d", "^d", "e", "f", "^f", "g", "^g", "a", "^a", "b", "c'"];
let randomNote = "";
let detectedNote = "";
let correctCounter = 0;
let lastNotes = ["X", "X"];
let isPaused = false;
const noteContainer = document.getElementById("note-container");

const socket = io();
socket.emit("start_audio_stream");


function getRandomNote(previousNote) {
    let newNote = "";
    do {
      newNote = notes[Math.floor(Math.random() * notes.length)];
    } while (newNote === previousNote);
    return newNote;
}

function renderNotes(currentNotes) {
    let abcString = "X:1\nT:Note Practice\nM:4/4\nL:1/1\nK:C\n";
    abcString += "|[";

    currentNotes.forEach((note) => {
        abcString += note;
    });
    abcString += "]|";

    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        staffwidth: 500
    });
}



randomNote = "C";
const currentNotes = [randomNote];
renderNotes(currentNotes);

socket.on("note_detected", (data) => {
    if(!isPaused){
        handleNote(data);
    }
});

function handleNote(data) {
    detectedNote = data.note;
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