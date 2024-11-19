const { Renderer, Stave, StaveNote, Voice, Formatter } = Vex.Flow;
const notes = ['c/4', 'd/4', 'e/4', 'f/4', 'g/4', 'a/4', 'b/4'];
let currentNote = '';

function renderRandomNote() {
  const div = document.getElementById("note-container");
  div.innerHTML = '';

  const renderer = new Renderer(div, Renderer.Backends.SVG);

  renderer.resize(500, 500);
  const context = renderer.getContext();

  const stave = new Stave(10, 40, 400);
  stave.addClef("treble").addTimeSignature("4/4");
  stave.setContext(context).draw();

  currentNote = notes[Math.floor(Math.random() * notes.length)];
  const staveNote = new StaveNote({ keys: [currentNote], duration: "w"});

  const voice = new Voice({ num_beats: 4, beat_value: 4 });
  voice.addTickables([staveNote]);

  new Formatter().joinVoices([voice]).format([voice], 350);

  voice.draw(context, stave);
}

renderRandomNote();