const { Renderer, Stave, StaveNote, Voice, Formatter } = Vex.Flow;
const notes = ['c/4', 'd/4', 'e/4', 'f/4', 'g/4', 'a/4', 'b/4'];
let currentNote = '';
let correctCounter = 0;
const noteContainer = document.getElementById("note-container");

function getRandomNote(previousNote) {
  newNote = '';
  do {
    newNote = notes[Math.floor(Math.random() * notes.length)];
  } while (newNote == previousNote)
  return newNote;
}

function getContext() {
  const renderer = new Renderer(noteContainer, Renderer.Backends.SVG);
  renderer.resize(500, 500);
  return renderer.getContext();
}

function getStave(context) {
  const stave = new Stave(10, 40, 400);
  stave.addClef("treble").addTimeSignature("4/4");
  stave.setContext(context).draw();
  return stave;
}

function renderNotes(currentNotes) {
  noteContainer.innerHTML = '';
  const context = getContext();
  const stave = getStave(context);

  for (let i = 0; i < currentNotes.length; i++) {
    if(currentNotes[i]){
      staveNote = new StaveNote({ keys: [currentNotes[i]], duration: "w"});
      if(i > 0){
        staveNote.setStyle({fillStyle: "red", strokeStyle: "red"});
      }
      const voice = new Voice({ num_beats: 4, beat_value: 4 });
      voice.addTickables([staveNote]);
      new Formatter().joinVoices([voice]).format([voice], 350);
      voice.draw(context, stave);
    }
  }
}

currentNote = getRandomNote();
currentNotes = [currentNote];

renderNotes(currentNotes);

const eventSource = new EventSource('/stream_notes');
eventSource.onmessage = function(event) {
  const detectedNote = event.data;
  playedNote = detectedNote;
  currentNotes[1] = playedNote;
  console.log(`Detected Note: ${detectedNote}`);
  renderNotes(currentNotes);
  if (detectedNote === currentNote) {
    correctCounter++;
    document.getElementById("correct-counter").textContent = correctCounter;
    currentNote = getRandomNote(currentNote);
    currentNotes[0] = currentNote;
    currentNotes[1] = '';
    renderNotes(currentNotes);
  }
};