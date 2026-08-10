const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const chatContainer = document.getElementById("chatContainer");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");

let conversation = [];


/* ============================= */
/* ADD MESSAGE */
/* ============================= */

function addMessage(role, content) {

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }

    const message = document.createElement("div");

    message.className = `message ${role}`;

    const contentElement = document.createElement("div");

    contentElement.className = "message-content";

    contentElement.textContent = content;

    message.appendChild(contentElement);

    chatContainer.appendChild(message);

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

    return contentElement;
}


/* ============================= */
/* SEND MESSAGE */
/* ============================= */

async function sendMessage() {

    const message = input.value.trim();

    if (!message || sendButton.disabled) {
        return;
    }


    // Show user message
    addMessage("user", message);


    // Clear input
    input.value = "";


    // Disable button
    sendButton.disabled = true;


    // Show thinking
    const thinkingMessage = addMessage(
        "assistant",
        "Thinking..."
    );


    try {

        const response = await fetch(
            "/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message,
                    history: conversation
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );

        }


        const data = await response.json();


        if (!data.reply) {

            throw new Error(
                "No reply received from server"
            );

        }


        // Replace Thinking with AI response
        thinkingMessage.textContent =
            data.reply;


        // Save conversation
        conversation.push({
            role: "user",
            content: message
        });


        conversation.push({
            role: "assistant",
            content: data.reply
        });


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        thinkingMessage.textContent =
            "Sorry, something went wrong. Please try again.";

    } finally {

        sendButton.disabled = false;

        input.focus();

        chatContainer.scrollTop =
            chatContainer.scrollHeight;

    }
}


/* ============================= */
/* FORM SUBMIT */
/* ============================= */

form.addEventListener(
    "submit",
    function (event) {

        event.preventDefault();

        sendMessage();

    }
);


/* ============================= */
/* ENTER TO SEND */
/* ============================= */

input.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* ============================= */
/* NEW CHAT */
/* ============================= */

function startNewChat() {

    conversation = [];

    chatContainer.innerHTML = `
        <div class="welcome">

            <div class="welcome-icon">
                T
            </div>

            <h1>
                How can I help you?
            </h1>

            <p>
                Ask questions, write code, learn something new,
                or just have a conversation.
            </p>

            <div class="suggestions">

                <button
                    class="suggestion"
                    data-message="Explain Python in simple words"
                >
                    <span>⌘</span>
                    Explain Python simply
                </button>

                <button
                    class="suggestion"
                    data-message="Help me learn programming"
                >
                    <span>◇</span>
                    Help me learn programming
                </button>

                <button
                    class="suggestion"
                    data-message="Write a professional resume summary"
                >
                    <span>✦</span>
                    Write something for me
                </button>

                <button
                    class="suggestion"
                    data-message="Tell me something interesting"
                >
                    <span>◈</span>
                    Something interesting
                </button>

            </div>

        </div>
    `;

    attachSuggestionEvents();

    input.value = "";

    input.focus();
}


/* ============================= */
/* NEW CHAT BUTTON */
/* ============================= */

clearButton.addEventListener(
    "click",
    startNewChat
);


const mobileNewChat =
    document.getElementById("mobileNewChat");


if (mobileNewChat) {

    mobileNewChat.addEventListener(
        "click",
        startNewChat
    );

}


/* ============================= */
/* SUGGESTIONS */
/* ============================= */

function attachSuggestionEvents() {

    document
        .querySelectorAll(".suggestion")
        .forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    input.value =
                        this.dataset.message;

                    input.focus();

                }
            );

        });

}


attachSuggestionEvents();


/* ============================= */
/* INITIAL FOCUS */
/* ============================= */

input.focus();
