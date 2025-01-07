document.addEventListener("DOMContentLoaded", () => {
    
    ABCJS.renderAbc("simple-read-music", "X:1\nK:C\nC8| A8| D8]", { scale: 2});
    ABCJS.renderAbc("chord-read-music", "X:1\nK:C\n[C E G]8| [A c e]8| [F A c]|]", {  scale: 2 });
    ABCJS.renderAbc("full-read-music", "X:1\nL:1/16K:C\nDDd2 A2 z ^G z =G z (F F)DFG", {  scale: 2 });
    ABCJS.renderAbc("latency-test-music", "X:1\nL:1/16K:C\nz8| z8| z8|]", {  scale: 2 });
});

function showTutorial(mode) {
    const tutorialDisplay = document.getElementById("tutorial-display");
    const formContainer = document.getElementById("form-container");
    console.log("bing");
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
                    <input type="number" id="tempo" name="tempo" min="40" max="240" placeholder="120">
                    
                    <button type="submit">Start Practice</button>
                </form>
            `;
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
