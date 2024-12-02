const notes = ['C,', '^C,', 'D,', '^D,', 'E,', 'F,', '^F,', 'G,', '^G,', 'A,', '^A,', 'B,', 'C', '^C', 'D', '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A', 'B'];
let currentNote = '';
const noteContainer = document.getElementById("note-container");


const abcString = "X:1\nT:Cooley's\nM:4/4\nL:1/8\nK:Emin\nD2|EBBA B2 EB|";

ABCJS.renderAbc(noteContainer.id, abcString, {
    add_classes: true,
    staffwidth: 500
});