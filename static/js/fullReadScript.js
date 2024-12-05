document.addEventListener("DOMContentLoaded", () => {
    const notes = ["C,", "^C,", "D,", "^D,", "E,", "F,", "^F,", "G,", "^G,", "A,", "^A,", "B,", "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B"];
    let currentNote = "";
    const noteContainer = document.getElementById("note-container");
    const highlightBox = document.getElementById("highlightBox");
    const startStopButton = document.getElementById("start-stop-button");
    let isPaused = true;
    let isFinished = false;
    let firstEvent = true;
    let eventCounter = 0;
    let startTime = 0;
    let latency = 450; //set this to the latency test result

    let practiceStates = [];

    class PracticeState {
        constructor(event) {
            this.event = event;
            this.detectedNotes = [];
            this.expectedNote = getExpectedNote(event);
            this.eventStartTime = event.milliseconds;
            this.accuracy = 0;
        }
    }

    let abcString = "X:1\nT:Example\nM:4/4\nL:1/8\nQ:1/4=60\nK:Cmaj\n";
    let randomlyGeneratedMusic = "C2 D2 E2 F2|";

    document.addEventListener('keydown', event => {
        if (event.code === 'Space') {
            startTime = Date.now();
            startStopPractice();
        }
    });

    const socket = io();
    window.addEventListener("beforeunload", () => {
        socket.emit("stop_audio_stream");
    });
    socket.on("note_detected", (data) => {
        if (!isPaused && !isFinished) {
            if(noteWasPlayedDuringCurrentEvent()){
                practiceStates[eventCounter].detectedNotes.push(data.note);
            } else {
                if(eventCounter - 1 >= 0){
                    practiceStates[eventCounter - 1].detectedNotes.push(data.note);
                }
            }
        }
    });

    function noteWasPlayedDuringCurrentEvent() {
        let now = Date.now();
        let noteTime = timeSinceStart(now);
        return (practiceStates[eventCounter].eventStartTime + latency) < noteTime;
    }

    abcString += randomlyGeneratedMusic;
    const visualObj = ABCJS.renderAbc(noteContainer.id, abcString, {
        add_classes: true,
        staffwidth: 500
    });

    highlightBox.style.display = "block";
    noteContainer.appendChild(highlightBox);

    const timingCallbacks = new ABCJS.TimingCallbacks(visualObj[0], {
        eventCallback: (ev) => {
            if (!firstEvent) {
                console.log(practiceStates[eventCounter]);
                eventCounter++;
                //fixate last note
            }
            if (ev != null) {
                animateHighlightBox(ev);
                let state = new PracticeState(ev);
                practiceStates[eventCounter] = state;
            } else {
                isPaused = true;
                isFinished = true;
                startStopButton.innerHTML = "Restart";
            }
            firstEvent = false;
        }
    });

    function getExpectedNote(ev) {
        const startChar = ev.startChar;
        const endChar = ev.endChar;
        let noteString = abcString.slice(startChar, endChar);
        noteString = noteString.replace(/[0-9\/]/g, "");
        noteString = noteString.trim();
        return noteString;
    }

    function animateHighlightBox(ev) {
        highlightBox.style.left = `${ev.left}px`;
        highlightBox.style.top = `${ev.top}px`;
        highlightBox.style.width = `${ev.width}px`;
        highlightBox.style.height = `${ev.height}px`;
    }

    function startStopPractice() {
        if (isFinished) {
            resetPracticeSession();
            startPractice();
        } else {
            if (isPaused) {
                startPractice();
            } else {
                pausePractice();
            }
        }
    }

    function resetPracticeSession() {
        isPaused = false;
        practiceStates = [];
        eventCounter = 0;
        firstEvent = true;
    }

    function startPractice() {
        socket.emit("start_audio_stream");
        isPaused = false;
        highlightBox.style.display = "block";
        timingCallbacks.start();
        startStopButton.innerHTML = "Stop";
    }

    function pausePractice() {
        timingCallbacks.pause();
        isPaused = true;
        startStopButton.innerHTML = "Resume";
    }

    function timeSinceStart(now) {
        return now - startTime;
    }

    startStopButton.onclick = startStopPractice;
});
