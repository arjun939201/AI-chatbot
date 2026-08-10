const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");


let conversation = [];


function addMessage(role, content) {

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }

    const message = document.createElement("div");

    message.className = `message ${role}`;

    const messageContent = document.createElement("div");

    messageContent.className = "message-content";

    messageContent.textContent = content;

    message.appendChild(messageContent);

    chatContainer.appendChild(message);

    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageContent;
}


async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    conversation.push({
        role: "user",
        content: message
    });

    input.value = "";

    sendButton.disabled = true;

    const thinkingMessage = addMessage(
        "assistant",
        "Thinking..."
    );

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                history: conversation.slice(0, -1)
            })

        });


        if (!response.ok) {
            throw new Error("Request failed");
        }


        const data = await response.json();

        thinkingMessage.textContent = data.reply;


        conversation.push({
            role: "assistant",
            content: data.reply
        });


    } catch (error) {

        console.error(error);

        thinkingMessage.textContent =
            "Sorry, something went wrong. Please try again.";

    } finally {

        sendButton.disabled = false;

        input.focus();

        chatContainer.scrollTop =
            chatContainer.scrollHeight;
    }
}


form.addEventListener("submit", function(event) {

    event.preventDefault();

    sendMessage();

});


input.addEventListener("keydown", function(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();
    }

});


clearButton.addEventListener("click", function() {

    conversation = [];

    chatContainer.innerHTML = `
        <div class="welcome">
            <h1>How can I help you?</h1>
            <p>Ask me anything.</p>
        </div>
    `;

    input.focus();

});
