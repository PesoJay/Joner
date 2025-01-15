import { notes, noteContainer, transposeInterval, socket, addEventListeners, transpose, abcInBackButton } from "./utils.js";
document.addEventListener("DOMContentLoaded", () => {
    const highlightBox = document.getElementById("highlightBox");
    const startStopButton = document.getElementById("start-stop-button");
    const beat = new Audio("/static/audio/countdown.wav");
    const latency = parseInt(localStorage.getItem("latencyInMs"), 10) || 100;
    let isPaused = true;
    let isFinished = false;
    let firstEvent = true;
    let eventCounter = 0;
    let startTime = 0;
    let pauseStartTime = 0;
    let totalPauseDuration = 0;
    let abcString = noteContainer.textContent;
    let visualObj = null;

    let practiceStates = [];

    class PracticeState {
        constructor(event) {
            this.event = event;
            this.detectedNotes = new Map();
            this.playedNote = "";
            this.expectedNote = getExpectedNote(event);
            this.eventStartTime = event.milliseconds;
        }
    }

    setUp();

    socket.on("note_detected", (data) => {
        if (!isPaused && !isFinished) {
            console.log("note detected!");
            let eventNoteWasPlayedInIndex = findEventNoteWasPlayedIn();
            let transposedNote = transpose(data.note, transposeInterval);
            addToDetectedNotes(transposedNote, eventNoteWasPlayedInIndex);
        }
    });

    const timingCallbacks = new ABCJS.TimingCallbacks(visualObj[0], {
        extraMeasuresAtBeginning: 1,
        eventCallback: (ev) => {
            if (!firstEvent) {
                console.log(practiceStates[eventCounter]);
                let lastEventIndex = eventCounter;
                gradeNote(lastEventIndex);
                eventCounter++;
            }
            if (ev != null) {
                animateHighlightBox(ev);
                let state = new PracticeState(ev);
                practiceStates[eventCounter] = state;
            } else {
                finishPractice();
            }
            firstEvent = false;
        }
    });

    function findEventNoteWasPlayedIn() {
        for (let i = practiceStates.length-1; i >= 0; i--) {
            if(noteWasPlayedDuringEvent(i)){
                return i;
            }
        }
    }

    function gradeNote(index){
        setTimeout(() => {
            practiceStates[index].playedNote = getPlayedNote(practiceStates[index].detectedNotes);
            let noteIsCorrect = isPlayedNoteCorrect(practiceStates[index]);
            colorNote(practiceStates[index], noteIsCorrect); //for now just colors the note red or green, may be able to extend to show actually played notes as well    
        }, latency);
    }

    function colorNote(state, noteIsCorrect){
        let color = "red";
        if (noteIsCorrect){
            color = "green";
        }
        state.event.elements[0][0].style.color = color;
    }

    function isPlayedNoteCorrect(state) {
        return state.expectedNote === state.playedNote;
    }

    function addToDetectedNotes(note, index){
        let count = 0;
        if(practiceStates[index].detectedNotes.has(note)){
            count = practiceStates[index].detectedNotes.get(note);
        }
        count++;
        practiceStates[index].detectedNotes.set(note, count);
    }

    function noteWasPlayedDuringEvent(index) {
        let now = Date.now();
        let noteTime = timeSinceStart(now);
        return (practiceStates[index].eventStartTime + latency) < noteTime;
    }

    function setUp(){
        console.log("Latency: " + latency);
        addEventListeners();
        document.addEventListener('keydown', event => {
            if (event.code === 'Space') {
                startStopPractice();
            }
        });
        abcInBackButton();
        abcString = cleanGeneratedAbcString(abcString);
        visualObj = ABCJS.renderAbc(noteContainer.id, abcString, {
            add_classes: true,
            staffwidth: 1000,
            wrap: {
                minSpacing: 1.5,
                maxSpacing: 5,
                preferredMeasuresPerLine: 4
            },
            scale: 1.3
        });
        highlightBox.style.display = "block";
        noteContainer.appendChild(highlightBox);
    }

    function cleanGeneratedAbcString(abc) {
        abc = abc.replace(/[()]/g, "");
        return abc;
    }

    function getExpectedNote(ev) {
        const startChar = ev.startChar;
        const endChar = ev.endChar;
        let noteString = abcString.slice(startChar, endChar);
        noteString = noteString.replace(/[0-9\/]/g, "");
        noteString = noteString.trim();
        noteString = shiftExpectedNoteByKey(noteString);
        return noteString;
    }

    function shiftExpectedNoteByKey(note) {
        let noteIndex = notes.indexOf(note);
        const accidentals = visualObj[0].getKeySignature().accidentals;
        accidentals.forEach((accidental) => {
            if(getNoteChar(note) === getNoteChar(accidental.note)) {
                if(accidental.acc == "sharp") {
                    noteIndex++;
                } else {
                    noteIndex--;
                }
            }
        });
        return notes[noteIndex];
    }

    function getNoteChar(note) {
        note = note.replace(/[,']/g, "");
        note = note.toLowerCase();
        return note;
    }

    function getPlayedNote(map) {
        let mostCommonNote = "";
        let mostCommonNoteCount = 0;
        let numberOfSamples = 0;

        for(let [key, value] of map){
            numberOfSamples += value;
            if(value > mostCommonNoteCount){
                mostCommonNote = key;
                mostCommonNoteCount = value;
            }
        }
        if(mostCommonNoteCount < 1){
            return "z"; //Assumes player didn't play during event, so returns a rest
        }
        if(mostCommonNoteCount / numberOfSamples >= 0.5){
            return mostCommonNote;
        }
        return "inaccurate result";
    }

    function animateHighlightBox(ev) {
        highlightBox.style.left = `${ev.left*1.3}px`;
        highlightBox.style.top = `${ev.top*1.3}px`;
        highlightBox.style.width = `${ev.width*1.3}px`;
        highlightBox.style.height = `${ev.height*1.3}px`;
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
        isFinished = false;
        practiceStates.forEach(state => {
            state.event.elements[0][0].style.color = "black";
        });
        practiceStates = [];
        eventCounter = 0;
        firstEvent = true;
        totalPauseDuration = 0;
    }

    function startPractice() {
        if(firstEvent){
            startTime = Date.now();
            beatIndicator();
        } else {
            totalPauseDuration += Date.now() - pauseStartTime;
        }
        socket.emit("start_audio_stream");
        isPaused = false;
        highlightBox.style.display = "block";
        timingCallbacks.start();
        startStopButton.innerHTML = "Stop";
    }

    function pausePractice() {
        pauseStartTime = Date.now();
        timingCallbacks.pause();
        isPaused = true;
        startStopButton.innerHTML = "Resume";
    }

    function finishPractice() {
        setTimeout(() => {
            isPaused = true;
            isFinished = true;
            startStopButton.innerHTML = "Restart";
        }, latency);
    }

    function beatIndicator() {
        const beatsToPlay = visualObj[0].getBeatsPerMeasure()-1;
        const beatLength = visualObj[0].millisecondsPerMeasure() / visualObj[0].getBeatsPerMeasure();
        let currentBeat = 0;

        beat.currentTime = 0;
        beat.play();

        const interval = setInterval(() => {
            if (currentBeat < beatsToPlay) {
                beat.currentTime = 0;
                beat.play();    
                currentBeat++;
            } else {
                clearInterval(interval);
            }
        }, beatLength);
    }

    function timeSinceStart(now) {
        return now - startTime - totalPauseDuration;
    }

    startStopButton.onclick = startStopPractice;
});