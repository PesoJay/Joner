import { socket, abcInBackButton } from "./utils.js";
let latencyInMs = 0;
let startTime = 0;
let endTime = 0;
let testRunning = false;

abcInBackButton();
socket.emit("start_audio_stream");
socket.emit("close_stream");
window.addEventListener("beforeunload", () => {
    socket.emit("stop_audio_stream");
});

socket.on("note_detected", (data) => {
    if(testRunning){
        console.log(`Detected Note: ${data.note}`);
        endTime = Date.now()
        testRunning = false;
        socket.emit("close_stream")        
        latencyInMs = endTime - startTime;
        document.getElementById("latency-counter").textContent = latencyInMs + "ms";
        localStorage.setItem("latencyInMs", latencyInMs);
    }
});

socket.on("stream_event", (data) => {
    console.log(data.status);
})

document.addEventListener('keydown', event => {
    if (event.code === 'Space') {
        latencyTest();
    }
});

function latencyTest(){
    console.log("startedTest");
    socket.emit("open_stream");
    testRunning = true;
    startTime = Date.now();
}