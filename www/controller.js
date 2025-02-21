// $(document).ready(function () {



//     // Display Speak Message
//     eel.expose(DisplayMessage)
//     function DisplayMessage(message) {

//         $(".siri-message li:first").text(message);
//         $('.siri-message').textillate('start');

//     }

//     // Display hood
//     eel.expose(ShowHood)
//     function ShowHood() {
//         console.log("ShowHood called");
//         $("#Oval").attr("hidden", false);
//         $("#SiriWave").attr("hidden", true);
//     }

//     eel.expose(senderText)
//     function senderText(message) {
//         var chatBox = document.getElementById("chat-canvas-body");
//         if (message.trim() !== "") {
//             chatBox.innerHTML += `<div class="row justify-content-end mb-4">
//             <div class = "width-size">
//             <div class="sender_message">${message}</div>
//         </div>`; 
    
//             // Scroll to the bottom of the chat box
//             chatBox.scrollTop = chatBox.scrollHeight;
//         }
//     }

//     eel.expose(receiverText)
//     function receiverText(message) {

//         var chatBox = document.getElementById("chat-canvas-body");
//         if (message.trim() !== "") {
//             chatBox.innerHTML += `<div class="row justify-content-start mb-4">
//             <div class = "width-size">
//             <div class="receiver_message">${message}</div>
//             </div>
//         </div>`; 
    
//             // Scroll to the bottom of the chat box
//             chatBox.scrollTop = chatBox.scrollHeight;
//         }
        
//     }

    
//     // Hide Loader and display Face Auth animation
//     eel.expose(hideLoader)
//     function hideLoader() {

//         $("#Loader").attr("hidden", true);
//         $("#FaceAuth").attr("hidden", false);

//     }
//     // Hide Face auth and display Face Auth success animation
//     eel.expose(hideFaceAuth)
//     function hideFaceAuth() {

//         $("#FaceAuth").attr("hidden", true);
//         $("#FaceAuthSuccess").attr("hidden", false);

//     }
//     // Hide success and display 
//     eel.expose(hideFaceAuthSuccess)
//     function hideFaceAuthSuccess() {

//         $("#FaceAuthSuccess").attr("hidden", true);
//         $("#HelloGreet").attr("hidden", false);

//     }


//     // Hide Start Page and display blob
//     eel.expose(hideStart)
//     function hideStart() {

//         $("#Start").attr("hidden", true);

//         setTimeout(function () {
//             $("#Oval").addClass("animate__animated animate__zoomIn");

//         }, 1000)
//         setTimeout(function () {
//             $("#Oval").attr("hidden", false);
//         }, 1000)
//     }

//     // Expose getFrontendInput function to Python
//     eel.expose(getFrontendInput);
//     function getFrontendInput() {
//         return new Promise((resolve) => {
//             const message = $("#chatbox").val();  // Get text input from the chatbox
//             resolve(message);  // Resolve the promise with the input value
//         });
//     }

//     // Example usage in Python
//     eel.getFrontendInput()().then((input) => {
//         console.log("Frontend input received:", input);
//     });


// });



$(document).ready(function () {

    // Display Speak Message
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // Display hood
    eel.expose(ShowHood);
    function ShowHood() {
        console.log("ShowHood called");
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    // Expose senderText to update sender messages in the chat
    eel.expose(senderText);
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class="width-size">
            <div class="sender_message">${message}</div>
        </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Expose receiverText to update received messages in the chat
    eel.expose(receiverText);
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class="width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Hide loader and display face authentication
    eel.expose(hideLoader);
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }

    eel.expose(hideFaceAuth);
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }

    eel.expose(hideFaceAuthSuccess);
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }

    eel.expose(hideStart);
    function hideStart() {
        $("#Start").attr("hidden", true);
        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");
        }, 1000);
        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000);
    }

    // Expose getFrontendInput to Python
    eel.expose(getFrontendInput);
    function getFrontendInput() {
        return new Promise((resolve) => {
            const message = $("#chatbox").val();  // Get text input from the chatbox
            $("#chatbox").val("");  // Clear the input field after getting input
            console.log("Captured input:", message);  // Debug log
            resolve(message);  // Resolve the promise with the input value
        });
    }

    // Example usage in Python (kept for testing purposes)
    eel.getFrontendInput()().then((input) => {
        console.log("Frontend input received:", input);
    });

    // Mic button click event
    $("#MicBtn").click(function () {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    // Send button event handler
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        if (!message) return;  // Do nothing if input is empty
        PlayAssistant(message);
    });

    // Enter key event handler on chatbox
    $("#chatbox").keypress(function (e) {
        if (e.which == 13) {  // Check if Enter key is pressed
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    // Function to send user input to the backend
    function PlayAssistant(message) {
        if (message) {
            eel.allCommands(message);  // Send the command to the backend
            $("#chatbox").val("");  // Clear the input field
        }
    }
});
