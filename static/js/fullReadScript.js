const notes = ['C,', '^C,', 'D,', '^D,', 'E,', 'F,', '^F,', 'G,', '^G,', 'A,', '^A,', 'B,', 'C', '^C', 'D', '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A', 'B'];
let currentNote = '';
const noteContainer = document.getElementById("note-container");
const highlightBox = document.getElementById("highlightBox");

let abcString = "X:1\nT:Example\nM:4/4\nL:1/8\nQ:1/4=60\nK:Emin\n";
let randomlyGeneratedMusic = "C2 D2 E2 F2| G2 A2 B2 c2|";
const socket = io();
socket.emit('start_audio_stream');

abcString += randomlyGeneratedMusic;
const visualObj = ABCJS.renderAbc(noteContainer.id, abcString, {
    add_classes: true,
    staffwidth: 500
});

highlightBox.style.display = 'block';
noteContainer.appendChild(highlightBox);

const timingCallbacks = new ABCJS.TimingCallbacks(visualObj[0], {
    eventCallback: (ev) => {
        if (ev.elements && ev.elements.length > 0) {
           
            highlightBox.style.left = `${ev.left}px`;
            highlightBox.style.top = `${ev.top}px`;
            highlightBox.style.width = `${ev.width}px`;
            highlightBox.style.height = `${ev.height}px`;
            
            const startChar = ev.startCharArray[0];
            const endChar = ev.endCharArray[0];
            console.log(ev);
            console.log(abcString.slice(startChar, endChar));
        }
    }
});


function startPractice(){
    highlightBox.style.display = 'block';
    timingCallbacks.start();
}