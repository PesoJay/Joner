document.addEventListener("DOMContentLoaded", () => {
    ABCJS.renderAbc("simple-read-music", "X:1\nK:C\nC8| A8| D8]", { scale: 2});
    ABCJS.renderAbc("chord-read-music", "X:1\nK:C\n[C E G]8| [A c e]8| [F A c]|]", {  scale: 2 });
    ABCJS.renderAbc("full-read-music", "X:1\nL:1/16K:C\nDDd2 A2 z ^G z =G z (F F)DFG", {  scale: 2 });
    ABCJS.renderAbc("latency-test-music", "X:1\nL:1/16K:C\nz8| z8| z8|]", {  scale: 2 });
});