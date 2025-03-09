$(document).ready(function () {

    eel.init()()

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event

    $("#MicBtn").click(function () {
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });


    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    // send button event handler
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });


    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });




});

document.addEventListener("mousemove", (e) => {
    let trail = document.createElement("div");
    trail.className = "cursor-trail";
    document.body.appendChild(trail);
    trail.style.left = `${e.clientX}px`;
    trail.style.top = `${e.clientY}px`;
    setTimeout(() => trail.remove(), 300);
});

// document.getElementById("send-chat-btn").addEventListener("click", function() {
//     const userInput = document.getElementById("chat-input").value;

//     if (!userInput) return; // Do nothing if input is empty

//     // Append user message to chat log
//     const chatLog = document.getElementById("chat-log");
//     chatLog.innerHTML += `<div class="user-message"><strong>You:</strong> ${userInput}</div>`;

//     // Clear the input field
//     document.getElementById("chat-input").value = "";

//     // Send the prompt to the Python backend using eel
//     eel.allCommands(userInput)(function(response) {
//         // Append chatbot response to chat log
//         chatLog.innerHTML += `<div class="bot-message"><strong>Jarvis:</strong> ${response}</div>`;
//     });
document.getElementById("send-chat-btn").addEventListener("click", function() {
    const userInput = document.getElementById("chat-input").value;
    if (!userInput) return; // Do nothing if input is empty

    // Append user message to chat log
    const chatLog = document.getElementById("chat-log");
    chatLog.innerHTML += `<div class="user-message"><strong>You:</strong> ${userInput}</div>`;

    // Clear the input field
    document.getElementById("chat-input").value = "";

    // Detect "write email" command
    if (userInput.toLowerCase().includes("write email")) {
        const recipientEmail = prompt("Enter recipient's email:");
        if (!recipientEmail) {
            alert("Recipient email is required!");
            return;
        }

        // Send the query and recipient email to the backend
        eel.send_email_command(userInput, recipientEmail)(function(response) {
            chatLog.innerHTML += `<div class="bot-message"><strong>Jarvis:</strong> ${response}</div>`;
        });
    } else {
        // Regular command handling
        eel.allCommands(userInput)(function(response) {
            chatLog.innerHTML += `<div class="bot-message"><strong>Jarvis:</strong> ${response}</div>`;
        });
    }
});

