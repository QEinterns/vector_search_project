
// Function to send message when Enter key is pressed
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Function to send message when Send button is clicked
function sendMessage() {
    console.log("button clicked")
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") {
        return;
    }
    showLoader();
    appendUserMessage(userInput);
    sendUserInputToServer(userInput);
    document.getElementById("user-input").value = "";
}

// Function to append user message to the chat display
function appendUserMessage(message) {
    var chatDisplay = document.getElementById("chat-display");
    var userMessageElement = document.createElement("div");
    userMessageElement.textContent = "You: " + message;
    userMessageElement.classList.add("message", "user-message");
    chatDisplay.appendChild(userMessageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// Function to append bot message to the chat display
function appendBotMessage(message) {
    var chatDisplay = document.getElementById("chat-display");
    var botMessageElement = document.createElement("div");
    botMessageElement.innerHTML = "Bot: " + message.replace(/\n/g, "<br>");
    botMessageElement.classList.add("message", "bot-message");
    chatDisplay.appendChild(botMessageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

// // Function to send user input to the server and receive bot response
// function sendUserInputToServer(userInput) {
//     $.ajax({
//         type: "POST",
//         url: "/chat",
//         data: {"user_input": userInput},
//         success: function(response) {
//             // Handle streaming response
//             response.forEach(function(chunk) {
//                 var botResponse = chunk.message.content;
//                 appendBotMessage(botResponse);
//             });
//             hideLoader();
//         },
//         error: function(error) {
//             console.log("Error:", error);
//             hideLoader();
//         },
//         // dataType: "json",
//         // contentType: "application/json"
//     });
// }

function sendUserInputToServer(userInput) {
    $.ajax({
        type: "POST",
        url: "/chat_a",
        data: {"user_input": userInput},
        success: function(response) {
            var botResponse = response.bot_response;
            appendBotMessage(botResponse);
            hideLoader();
        },
        error: function(error) {
            console.log("Error:", error);
            hideLoader();
        }
    });
}

// Function to show loading spinner
function showLoader() {
    document.getElementById("loader").style.display = "inline-block";
}

// Function to hide loading spinner
function hideLoader() {
    document.getElementById("loader").style.display = "none";
}


function newSession(session_name){
    var oldval = session_name
    console.log("oldval: ",oldval)
    console.log("sessionname:",session_name)
    var ress = "";
    $.ajax({
        type: "POST",
        url: "/newsession_a",
        data: {"session_name": session_name},
        success: function(response) {
            ress = response.new_name;
            
            console.log("newname:",ress)
            console.log("aftersession:",session_name)
            next1(ress,oldval);
        },
        error: function(error) {
            console.log("Error:", error);
            hideLoader();
        }
    });

    
}

function loadSession(session_name){
    $.ajax({
        type: "POST",
        url: "/loadsession_a",
        data: {"session_name": session_name},
        success: function(response) {
            console.log(response)
            // var parsedResponse = JSON.parse(response);
            var parsedData = JSON.parse(response.data);

            var session_con = document.getElementById("chat-container");
            session_con.innerHTML = "";

            // Get a reference to the div with id "chat-container"
            var chatContainer = document.getElementById("chat-container");

            // Create a new div element
            var newDivElement = document.createElement("div");

            // Set the id attribute of the new div element using the session name variable
            newDivElement.id = session_name;

            // Create the chat display div
            var chatDisplayDiv = document.createElement("div");
            chatDisplayDiv.id = "chat-display";

            // Create the user input container div
            var userInputContainerDiv = document.createElement("div");
            userInputContainerDiv.id = "user-input-container";

            // Create the input element
            var inputElement = document.createElement("input");
            inputElement.type = "text";
            inputElement.id = "user-input";
            inputElement.placeholder = "Type your message...";


            var anchor = document.createElement('a');
            anchor.setAttribute('onclick', 'sendMessage()');
            anchor.setAttribute('class', 'icon-button');
            var icon = document.createElement('i');
            icon.setAttribute('class', 'ph-arrow-up-bold');
            anchor.appendChild(icon);
            


            $(document).on("click", "#user-input-container a", function() {
                console.log("Button clicked");
                var userInput = $("#user-input").val().trim();
                if (userInput === "") {
                    return;
                }
                showLoader();
                appendUserMessage(userInput);
                sendUserInputToServer(userInput);
                $("#user-input").val("");
            });
            

            // Append the input and button elements to the user input container div
            userInputContainerDiv.appendChild(inputElement);
            userInputContainerDiv.appendChild(anchor);

            // Append the chat title, chat display, user input container, and loader divs to the new div element
            newDivElement.innerHTML = `
                <div id="chat-title">CB Architect Chat</div>
                ${chatDisplayDiv.outerHTML}
                ${userInputContainerDiv.outerHTML}
                <div id="loader"></div>
            `;

            // Append the new div element to the chat container
            chatContainer.appendChild(newDivElement);

            // // var newButton = document.createElement("button");
            // // newButton.setAttribute("class", "session_item");
            // // newButton.textContent = new_name;
            // // appendable.appendChild(newButton);

            // var text1 = document.createElement("div");
            // text1.setAttribute("id", "chat-title");
            // text1.textContent = "CAP Chatbot";
            // appendable.appendChild(text1);

            // var text2 = document.createElement("div");
            // text2.setAttribute("id", "chat-display");
            // appendable.appendChild(text2);

            // var text3 = document.createElement("div");
            // text3.setAttribute("id", "user-input-container");
            // var inside1 = document.createElement("input");
            // inside1.setAttribute("id", "user-input");
            // inside1.setAttribute("type", "text");
            // inside1.setAttribute("placeholder", "Type your message...");
            // text3.appendChild(inside1);
            // var inside2 = document.createElement("button");
            // inside2.onclick = function(){
            //     sendMessage();
            // }
            // inside2.textContent = "Send";
            // text3.appendChild(inside2);

            // appendable.appendChild(text3);

            // var text4 = document.createElement("div");
            // text4.setAttribute("id", "loader");

            // appendable.appendChild(text4);

            // session_con.appendChild(appendable);

            parsedData.forEach(function(item) {
                // Access the user's text and AI's text for each item
                var userText = item.user;
                var aiText = item.ai;
                
                var chatDisplay = document.getElementById(session_name).querySelector("#chat-display");
                var userMessageElement = document.createElement("div");
                userMessageElement.textContent = "You: " + userText;
                userMessageElement.classList.add("message", "user-message");
                chatDisplay.appendChild(userMessageElement);
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
                

         
                var botMessageElement = document.createElement("div");
                botMessageElement.textContent = "Bot: " + aiText;
                botMessageElement.classList.add("message", "bot-message");
                chatDisplay.appendChild(botMessageElement);
                chatDisplay.scrollTop = chatDisplay.scrollHeight;
            });

            // initializeChatContainer(session_name);
            
            // var ress = response;
            // // console.log(ress)
            // var load_data = JSON.parse('{{ ress | tojson | safe }}');
            // console.log(load_data)
            // load_data.forEach(function(pair){
            //     console.log(pair.ai);
            //     console.log(pair.user);
            // });
        },
        error: function(error) {
            console.log("Error:", error);
            hideLoader();
        }
    });
    console.log(session_name)
}
function next1(new_name, session_name) {
    // Remove existing session and "New session" button
    // console.log("Removing element with id:", session_name);
    console.log("newname : ",new_name)
    console.log("session_name",session_name)
    var parentElement = document.getElementById("newsns");
    parentElement.onclick = function(){
        newSession(new_name)
    };

    // if (parentElement) {
    //     parentElement.remove();
    // } else {
    //     console.error("Parent element not found.");
    // }
    

    // var elementToRemove1 = document.getElementById("newsns");
    // if (elementToRemove1) {
    //     elementToRemove1.remove();
    // } else {
    //     console.error("Element not found.");
    // }
    // var ut1 = document.createElement("div");
    // ut1.setAttribute("id", "sessions");
    // // Create and append "New session" button
    // var newButton1 = document.createElement("button");
    // newButton1.setAttribute("id", "newsns");
    // newButton1.textContent = "New session";
    // newButton1.onclick = function() {
    //     newSession(new_name);
    // };
    // ut1.appendChild(newButton1);

    // Create and append the new session div

    var elementToRemove1 = document.getElementById(session_name);
    if (elementToRemove1) {
        elementToRemove1.remove();
    } else {
        console.error("Element not found.");
    }

    var upper = document.getElementById("senlist")
    var newButton = document.createElement("button");
    newButton.setAttribute("class", "session_item");
    newButton.textContent = new_name;
    newButton.onclick = function(){
        loadSession(new_name)
    }
    upper.appendChild(newButton);


    var session_con = document.getElementById("chat-container");
    var appendable = document.createElement("div");
    appendable.setAttribute("id", new_name);

    // var newButton = document.createElement("button");
    // newButton.setAttribute("class", "session_item");
    // newButton.textContent = new_name;
    // appendable.appendChild(newButton);

    var text1 = document.createElement("div");
    text1.setAttribute("id", "chat-title");
    text1.textContent = "CB Architect chat";
    appendable.appendChild(text1);

    var text2 = document.createElement("div");
    text2.setAttribute("id", "chat-display");
    appendable.appendChild(text2);

    var text3 = document.createElement("div");
    text3.setAttribute("id", "user-input-container");
    var inside1 = document.createElement("input");
    inside1.setAttribute("id", "user-input");
    inside1.setAttribute("type", "text");
    inside1.setAttribute("placeholder", "Type your message...");
    text3.appendChild(inside1);


    var anchor = document.createElement('a');
    anchor.setAttribute('onclick', 'sendMessage()');
    anchor.setAttribute('class', 'icon-button');
    var icon = document.createElement('i');
    icon.setAttribute('class', 'ph-arrow-up-bold');
    anchor.appendChild(icon);
    

    text3.appendChild(anchor);

    appendable.appendChild(text3);

    var text4 = document.createElement("div");
    text4.setAttribute("id", "loader");

    appendable.appendChild(text4);

    session_con.appendChild(appendable);

    $(document).on("click", "#user-input-container a", function() {
        console.log("Button clicked");
        var userInput = $("#user-input").val().trim();
        if (userInput === "") {
            return;
        }
        showLoader();
        appendUserMessage(userInput);
        sendUserInputToServer(userInput);
        $("#user-input").val("");
    });

    // initializeChatContainer(new_name);
}


// Example usage: initialize the chat container with the session name







// this is end of main file


// // Function to send message when Enter key is pressed
// document.getElementById("user-input").addEventListener("keypress", function(event) {
//     if (event.key === "Enter") {
//         sendMessage();
//     }
// });

// // Function to send message when Send button is clicked
// function sendMessage() {
//     var userInput = document.getElementById("user-input").value;
//     if (userInput.trim() === "") {
//         return;
//     }
//     showLoader();
//     appendUserMessage(userInput);
//     sendUserInputToServer(userInput);
//     document.getElementById("user-input").value = "";
// }

// // Function to append user message to the chat display
// function appendUserMessage(message) {
//     var chatDisplay = document.getElementById("chat-display");
//     var userMessageElement = document.createElement("div");
//     userMessageElement.textContent = "You: " + message;
//     userMessageElement.classList.add("message", "user-message");
//     chatDisplay.appendChild(userMessageElement);
//     chatDisplay.scrollTop = chatDisplay.scrollHeight;
// }

// // Function to append bot message to the chat display
// function appendBotMessage(message) {
//     var chatDisplay = document.getElementById("chat-display");
//     var botMessageElement = document.createElement("div");
//     botMessageElement.textContent = "Bot: " + message;
//     botMessageElement.classList.add("message", "bot-message");
//     chatDisplay.appendChild(botMessageElement);
//     chatDisplay.scrollTop = chatDisplay.scrollHeight;
// }

// // Function to send user input to the server and receive bot response
// function sendUserInputToServer(userInput) {
//     $.ajax({
//         type: "POST",
//         url: "/chat",
//         data: {"user_input": userInput},
//         success: function(response) {
//             var botResponse = response.bot_response;
//             appendBotMessage(botResponse);
//             hideLoader();
//         },
//         error: function(error) {
//             console.log("Error:", error);
//             hideLoader();
//         }
//     });
// }

// // Function to show loading spinner
// function showLoader() {
//     document.getElementById("loader").style.display = "inline-block";
// }

// // Function to hide loading spinner
// function hideLoader() {
//     document.getElementById("loader").style.display = "none";
// }

// // Function to clear conversation and reset session variables
// function clearConversation() {
//     localStorage.removeItem('conversation');
//     document.getElementById("chat-display").innerHTML = ""; // Clear chat display
//     // Additional logic to reset session variables as needed
// }

// // Function to load selected session
// function loadSession(sessionId) {
//     if (sessionId) {
//         // Load session data from localStorage and populate chat display
//         var sessionData = JSON.parse(localStorage.getItem(sessionId));
//         if (sessionData) {
//             document.getElementById("chat-display").innerHTML = sessionData.conversation;
//         }
//     }
// }




















// function newSession(session_name){
//     $.ajax({
//         type: "POST",
//         url: "/newsession",
//         data: {"session_name": session_name},
//         success: function(response) {
//             var ress = response.new_name;
//             next1(ress)
//         },
//         error: function(error) {
//             console.log("Error:", error);
//             hideLoader();
//         }
//     });
//     console.log(session_name)
// }

// function next1(new_name){
//     var session_con = document.getElementById("sessions");
//     var btn_text = new_name
//     var newButton = document.createElement("button");
//     newButton.setAttribute("class", "session_item");
//     newButton.textContent = btn_text;
//     session_con.appendChild(newButton)
// }


// // Function to send message when Enter key is pressed
// document.getElementById("user-input").addEventListener("keypress", function(event) {
//     if (event.key === "Enter") {
//         sendMessage();
//     }
// });

// // Function to send message when Send button is clicked
// function sendMessage() {
//     var userInput = document.getElementById("user-input").value;
//     if (userInput.trim() === "") {
//         return;
//     }
//     showLoader();
//     appendUserMessage(userInput);
//     sendUserInputToServer(userInput);
//     document.getElementById("user-input").value = "";
// }

// // Function to append user message to the chat display
// function appendUserMessage(message) {
//     var chatDisplay = document.getElementById("chat-display");
//     var userMessageElement = document.createElement("div");
//     userMessageElement.textContent = "You: " + message;
//     userMessageElement.classList.add("message", "user-message");
//     chatDisplay.appendChild(userMessageElement);
//     chatDisplay.scrollTop = chatDisplay.scrollHeight;
// }

// // Function to append bot message to the chat display
// function appendBotMessage(message) {
//     // console.log("msg: ")
//     // console.log(message)
//     var chatDisplay = document.getElementById("chat-display");
//     var botMessageElement = document.createElement("div");
//     botMessageElement.textContent = "Bot: " + message;
//     botMessageElement.classList.add("message", "bot-message");
//     chatDisplay.appendChild(botMessageElement);
//     chatDisplay.scrollTop = chatDisplay.scrollHeight;
// }

// // Function to send user input to the server and receive bot response
// function sendUserInputToServer(userInput) {
//     $.ajax({
//         type: "POST",
//         url: "/chat",
//         data: {"user_input": userInput},
//         success: function(response) {
//             var botResponse = response.bot_response;
//             appendBotMessage(botResponse);
//             hideLoader();
//         },
//         error: function(error) {
//             console.log("Error:", error);
//             hideLoader();
//         }
//     });
// }

// // Function to show loading spinner
// function showLoader() {
//     document.getElementById("loader").style.display = "inline-block";
// }

// // Function to hide loading spinner
// function hideLoader() {
//     document.getElementById("loader").style.display = "none";
// }




