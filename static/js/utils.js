export const notes = [
    "C,,", "^C,,", "D,,", "^D,,", "E,,", "F,,", "^F,,", "G,,", "^G,,", "A,,", "^A,,", "B,,",
    "C,", "^C,", "D,", "^D,", "E,", "F,", "^F,", "G,", "^G,", "A,", "^A,", "B,",
    "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B",
    "c", "^c", "d", "^d", "e", "f", "^f", "g", "^g", "a", "^a", "b",
    "c'", "^c'", "d'", "^d'", "e'", "f'", "^f'", "g'", "^g'", "a'", "^a'", "b'",
];
export const noteContainer = document.getElementById("note-container");
export const transposeSelect = document.getElementById("transpose-select");
export const socket = io();
export let transposeInterval = 0;

export function addEventListeners() {
    transposeSelect.addEventListener("change", (e) => {
        transposeInterval = parseInt(e.target.value);
        console.log(transposeInterval);
    });
    
    window.addEventListener("beforeunload", () => {
        socket.emit("stop_audio_stream");
    });
}

export function transpose(note, interval) {
    let noteIndex = notes.indexOf(note);
    return notes[noteIndex+interval];
}

export function abcInBackButton() {
    console.log("bingo");
    let backButtonAbcContainer = document.getElementById("back-button-music");
    ABCJS.renderAbc(backButtonAbcContainer, "X:1\nK:C\nz4 !D.C.!|]", { scale: 2});
}