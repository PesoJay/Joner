import { socket, abcInBackButton } from "./utils.js";
let latencyInMs = 0;
let startTime = 0;
let endTime = 0;
let testRunning = false;

abcInBackButton();
window.addEventListener("beforeunload", () => {
    socket.emit("stop_audio_stream");
});

socket.on("note_detected", (data) => {
    if(testRunning){
        console.log(`Detected Note: ${data.note}`);
        endTime = Date.now()
        testRunning = false;
        latencyInMs = endTime - startTime;
        document.getElementById("latency-counter").textContent = latencyInMs;
        localStorage.setItem("latencyInMs", latencyInMs);
        socket.emit("stop_audio_stream");  
    }
});

document.addEventListener('keydown', event => {
    if (event.code === 'Space') {
        latencyTest();
    }
});

function latencyTest(){
    socket.emit("start_audio_stream");
    console.log("startedTest");
    testRunning = true;
    startTime = Date.now();
}