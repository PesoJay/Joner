document.addEventListener("DOMContentLoaded", () => {
    
    ABCJS.renderAbc("simple-read-music", "X:1\nK:C\nC8| A8| D8]", { scale: 2});
    ABCJS.renderAbc("chord-read-music", "X:1\nK:C\n[C E G]8| [A c e]8| [F A c]|]", {  scale: 2 });
    ABCJS.renderAbc("full-read-music", "X:1\nL:1/16K:C\nDDd2 A2 z ^G z =G z (F F)DFG", {  scale: 2 });
    ABCJS.renderAbc("latency-test-music", "X:1\nL:1/16K:C\nz8| z8| z8|]", {  scale: 2 });
});

function showTutorial(mode) {
    const tutorialDisplay = document.getElementById("tutorial-display");
    const formContainer = document.getElementById("form-container");
    formContainer.innerHTML = "";

    let tutorialText = "";
    switch (mode) {
        case "simpleReadPractice":
            tutorialText = "Practice single notes by sightreading one at a time.";
            break;
        case "chordReadPractice":
            tutorialText = "Practice identifying and playing chords by sight.";
            break;
        case "fullReadPractice":
            tutorialText = "Generate full sheet music to sightread. Adjust tempo and key below.";
            formContainer.innerHTML = `
                <form method="POST" action="/startFullReadPractice">
                    <label for="tempo">Tempo (BPM):</label>
                    <input type="number" id="tempo" name="tempo" min="40" max="240" placeholder="60">
                    
                    <label for="mode">Mode:</label>
                    <select id="mode" name="mode" onchange="updateKeyOptions()">
                        <option value="random">Random</option>  
                        <option value="maj">Major</option>
                        <option value="min">Minor</option>
                    </select>

                    <label for="key">Key:</label>
                    <select id="key" name="key">
                    </select>

                    <button type="submit">Start Practice</button>
                </form>
            `;

            updateKeyOptions();
            break;
        case "latencyTest":
            tutorialText = "Measure input latency to ensure accurate practice results.";
            break;
        default:
            tutorialText = "Hover over a button to see the tutorial.";
            break;
    }

    tutorialDisplay.querySelector("h2").innerText = tutorialText;
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