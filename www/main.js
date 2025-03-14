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


// Initialize Particles.js for Background
particlesJS("particleCanvas", {
    particles: {
        number: { value: 120, density: { enable: true, value_area: 800 } },
        color: { value: "#00B8FF" },
        shape: { type: "circle" },
        opacity: { value: 0.6, random: true },
        size: { value: 3, random: true },
        line_linked: {
            enable: true,
            distance: 100,
            color: "#00B8FF",
            opacity: 0.4,
            width: 1
        },
        move: {
            enable: true,
            speed: 2,
            direction: "none",
            random: true,
            straight: false,
            out_mode: "out"
        }
    }
});

// Cursor Glow Effect
document.addEventListener("mousemove", (e) => {
    let cursor = document.querySelector(".circle");
    cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});

// Orb Hover Animation
const orb = document.querySelector(".glowing-orb");
orb.addEventListener("mouseenter", () => {
    orb.style.boxShadow = "0 0 150px #00B8FF, 0 0 200px #0066FF, 0 0 250px #0033FF";
    orb.style.transform = "scale(1.2)";
});
orb.addEventListener("mouseleave", () => {
    orb.style.boxShadow = "0 0 100px #00B8FF, 0 0 150px #0066FF, 0 0 200px #0033FF";
    orb.style.transform = "scale(1)";
});



// Create multiple circles for the trail effect
const trailSize = 20; // Number of circles
const circles = [];

for (let i = 0; i < trailSize; i++) {
  let div = document.createElement("div");
  div.classList.add("circle");
  document.body.appendChild(div);
  circles.push(div);
}

// Style the circles dynamically
circles.forEach((circle, index) => {
  circle.style.position = "fixed";
  circle.style.width = "12px";
  circle.style.height = "12px";
  circle.style.borderRadius = "50%";
  circle.style.pointerEvents = "none";
  circle.style.backgroundColor = `rgba(0, 184, 255, ${1 - index / trailSize})`; // Fade effect
  circle.style.zIndex = "9999";
});

// Store the previous positions
const coords = { x: 0, y: 0 };
const positions = Array(trailSize).fill({ x: 0, y: 0 });

window.addEventListener("mousemove", (e) => {
  coords.x = e.clientX;
  coords.y = e.clientY;
});

function animateCircles() {
  // Shift all positions back by one
  for (let i = positions.length - 1; i > 0; i--) {
    positions[i] = { ...positions[i - 1] };
  }

  // Set first position to the current cursor
  positions[0] = { x: coords.x, y: coords.y };

  // Update the position of each circle
  circles.forEach((circle, index) => {
    let x = positions[index].x;
    let y = positions[index].y;

    circle.style.transform = `translate(${x - 6}px, ${y - 6}px) scale(${1 - index / trailSize})`;
  });

  requestAnimationFrame(animateCircles);
}

// Start the animation
animateCircles();


  






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
document.getElementById("send-chat-btn").addEventListener("click", function () {
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
        eel.send_email_command(userInput, recipientEmail)(function (response) {
            chatLog.innerHTML += `<div class="bot-message"><strong>Jarvis:</strong> ${response}</div>`;
        });
    } else {
        // Regular command handling
        eel.allCommands(userInput)(function (response) {
            chatLog.innerHTML += `<div class="bot-message"><strong>Jarvis:</strong> ${response}</div>`;
        });
    }





});

