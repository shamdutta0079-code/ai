// static/script.js
// MIC WORKING VERSION

const chatBox = document.getElementById("chatBox");
const input = document.getElementById("msg");
const typing = document.getElementById("typing");
const micBtn = document.querySelector(".mic");

// time
function getTime() {
    let d = new Date();
    let h = d.getHours();
    let m = d.getMinutes().toString().padStart(2, "0");
    return h + ":" + m;
}

// add msg
function addMessage(text, type, name) {

    let div = document.createElement("div");
    div.className = "msg " + type;

    div.innerHTML = `
<div class="name">${name}</div>
<div class="bubble">${text}</div>
<div class="time">${getTime()}</div>
`;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// typing
function showTyping() {
    typing.style.display = "block";
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    typing.style.display = "none";
}

// send
async function sendMsg() {

    let msg = input.value.trim();

    if (msg == "") return;

    addMessage(msg, "user", "Ayan");
    input.value = "";

    showTyping();

    try {

        let res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ msg: msg })
        });

        let data = await res.json();

        hideTyping();

        addMessage(data.reply, "ai", "Bidwiya");

        // voice
        let audio = new Audio("/voice?text=" + encodeURIComponent(data.reply));
        audio.play();

    } catch {

        hideTyping();
        addMessage("Network problem 😔", "ai", "Bidwiya");

    }
}

// enter
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMsg();
    }
});


// ========================
// MIC SPEECH TO TEXT
// ========================
const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "bn-BD";
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.onclick = () => {

        micBtn.innerText = "🎙️";
        micBtn.style.background = "#00ffaa";

        recognition.start();

    };

    recognition.onresult = function (event) {

        let transcript = event.results[0][0].transcript;

        input.value = transcript;

        micBtn.innerText = "🎤";
        micBtn.style.background = "";

        sendMsg();

    };

    recognition.onerror = function () {

        micBtn.innerText = "🎤";
        micBtn.style.background = "";

    };

    recognition.onend = function () {

        micBtn.innerText = "🎤";
        micBtn.style.background = "";

    };

} else {

    micBtn.onclick = () => {
        alert("Mic not supported in this browser");
    };

}

input.focus();
