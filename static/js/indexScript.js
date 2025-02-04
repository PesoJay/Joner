document.addEventListener("DOMContentLoaded", () => {
    ABCJS.renderAbc("simple-read-music", "X:1\nK:C\nC8| A8| D8]", { scale: 2 });
    ABCJS.renderAbc("chord-read-music", "X:1\nK:C\n[C E G]8| [A c e]8| [F A c]|]", { scale: 2 });
    ABCJS.renderAbc("full-read-music", "X:1\nL:1/16K:C\nDDd2 A2 z ^G z =G z (F F)DFG", { scale: 2 });
    ABCJS.renderAbc("latency-test-music", "X:1\nL:1/16K:C\nz8| z8| z8|]", { scale: 2 });

    const chordReadDiv = document.querySelector(".chord-read");
    const fullReadDiv = document.querySelector(".full-read");

    chordReadDiv.addEventListener("click", () => {
        const form = document.querySelector("form[action='/startChordPractice']");
        if (form) {
            form.submit();
        }
    });

    fullReadDiv.addEventListener("click", () => {
        const form = document.querySelector("form[action='/startFullReadPractice']");
        if (form) {
            form.submit();
        }
    });
});
let lastMode = "";

function showTutorial(mode) {
    if(lastMode != mode){

        const tutorialDisplay = document.getElementById("tutorial-display");
        const formContainer = document.getElementById("form-container");
        const tutorialTextContainer = document.getElementById("tutorial-text-container");
        formContainer.innerHTML = "";

        let tutorialHeading = "";
        let tutorialText = "";
        switch (mode) {
            case "simpleReadPractice":
                tutorialHeading = "Practice identifying and playing single notes by sight.";
                tutorialText = `In this Practice mode you will be shown a single note at a time.
                Try to play that note, if you fail your played note will show up in red, if you succeed the note will light up green and your score will increase.
                You can use the transposition tool to transpose your instrument if it's not in C.
                `;
                break;
            case "chordReadPractice":
                tutorialHeading = "Practice identifying and playing chords by sight.";
                tutorialText = `In this Practice mode you will be shown one chord at a time.
                Try to play that chord, if you fail the chord will show up in red, if you succeed the chord will light up green and your score will increase.
                It doesn't matter in which octave you play the chord, as long as its the same chord displayed it will be counted as correct.
                You can use the transposition tool to transpose your instrument if it's not in C.
                You can select a Key in which you want to practice below. All chords will be diatonic to that key.
                `;
                formContainer.innerHTML = `
                    <form method="POST" action="/startChordPractice">                  
                        <label for="mode">Mode:</label>
                        <select id="mode" name="mode" onchange="updateKeyOptions()">
                            <option value="random">Random</option>  
                            <option value="maj">Major</option>
                            <option value="min">Minor</option>
                        </select>

                        <label for="key">Key:</label>
                        <select id="key" name="key">
                        </select>
                    </form>
                `;

                updateKeyOptions();
                break;
            case "fullReadPractice":
                tutorialHeading = "Practice playing a full piece.";
                tutorialText = `In this Practice mode you will be shown a randomly generated etude.
                Once you press Start (or the spacebar) you will be counted into the piece and after the 4-beat count in the piece will start.
                Try to play the Piece, if you do well the notes will light up green, indicating that you are playing correctly, if they are red, then you played those notes wrong.
                Start with slower tempos and easier keys, then work your way up.
                If you get only red notes you might need to retake the latency test, or your instrument is not in tune.
                You can use the transposition tool to transpose your instrument if it's not in C.
                Note Range (inclusive): C4 - C6             
                `;
                formContainer.innerHTML = `
                    <form method="POST" action="/startFullReadPractice">
                        <label for="tempo">Tempo (BPM):</label>
                        <input type="number" id="tempo" name="tempo" min="40" max="100" value="60">
                        
                        <label for="mode">Mode:</label>
                        <select id="mode" name="mode" onchange="updateKeyOptions()">
                            <option value="random">Random</option>  
                            <option value="maj">Major</option>
                            <option value="min">Minor</option>
                        </select>

                        <label for="key">Key:</label>
                        <select id="key" name="key">
                        </select>
                    </form>
                `;

                updateKeyOptions();
                break;
            case "latencyTest":
                tutorialHeading = "Measure input latency to ensure accurate practice results.";
                tutorialText = `Perform this test to determine the latency of your system.
                A score of <200ms is good, scores above that could cause some problems, but should still be usable.
                The instructions for the test can be found on the test site itself.
                `
                break;
            default:
                tutorialHeading = "Hover over a button to see the tutorial.";
                break;
        }

        tutorialDisplay.querySelector("h2").innerText = tutorialHeading;
        tutorialTextContainer.innerHTML = tutorialText;
    }

    lastMode = mode;
}

function updateKeyOptions() {
    const mode = document.getElementById("mode").value;
    const keyDropdown = document.getElementById("key");

    const majorKeys = ["C", "G", "D", "A", "E", "B", "F", "Bb", "Eb", "Ab", "Db"];
    const minorKeys = ["A", "E", "B", "F#", "C#", "G#", "D", "G", "C", "F", "Bb"];
    const randomKeys = ["random"];

    keyDropdown.innerHTML = "";

    let keys = [];
    if(mode === "maj") {
        keys = majorKeys;
    } else if (mode === "min") {
        keys = minorKeys;
    } else {
        keys = randomKeys;
    }
    keys.forEach((key) => {
        const option = document.createElement("option");
        option.value = key;
        option.textContent = key;
        keyDropdown.appendChild(option);
    });
}