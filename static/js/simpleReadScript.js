const notes = ['C,', '^C,', 'D,', '^D,', 'E,', 'F,', '^F,', 'G,', '^G,', 'A,', '^A,', 'B,', 'C', '^C', 'D', '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A', 'B'];
let currentNote = '';
let correctCounter = 0;
const noteContainer = document.getElementById("note-container");

const socket = io();
socket.emit('start_audio_stream');

function getRandomNote(previousNote) {
    let newNote = '';
    do {
      newNote = notes[Math.floor(Math.random() * notes.length)];
    } while (newNote === previousNote);
    return newNote;
}

function renderNotes(currentNotes) {
    let abcString = "X:1\nT:Note Practice\nM:4/4\nL:1/1\nK:C\n";
    abcString += "[";

    currentNotes.forEach((note) => {
        abcString += note;
    });
    abcString += "]";

    ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        staffwidth: 500
    });
}

function colorWrongNote() {
    const chord = noteContainer.querySelector('.abcjs-note');
    chord.childNodes.forEach((childNode) => {
        if(childNode.dataset.name === currentNotes[1]){
            childNode.style.fill = "red";
        }
    });
}

currentNote = 'C';
const currentNotes = [currentNote];
renderNotes(currentNotes);

socket.on('note_detected', (data) => {
    const detectedNote = data.note;
    currentNotes[1] = detectedNote;
    console.log(`Detected Note: ${data.note}`);
    renderNotes(currentNotes);
    colorWrongNote();

    if (detectedNote === currentNote) {
        correctCounter++;
        document.getElementById("correct-counter").textContent = correctCounter;
        currentNote = getRandomNote(currentNote);
        currentNotes[0] = currentNote;
        currentNotes[1] = '';
        renderNotes(currentNotes);
    }
});