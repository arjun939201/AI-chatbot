document.querySelectorAll(".suggestion").forEach(button => {

    button.addEventListener("click", () => {

        input.value = button.dataset.message;

        input.focus();

    });

});


const mobileNewChat = document.getElementById("mobileNewChat");

if (mobileNewChat) {

    mobileNewChat.addEventListener("click", () => {

        conversation = [];

        chatContainer.innerHTML = `
            <div class="welcome">

                <div class="welcome-icon">
                    T
                </div>

                <h1>How can I help you?</h1>

                <p>
                    Ask questions, write code, learn something new,
                    or just have a conversation.
                </p>

                <div class="suggestions">

                    <button class="suggestion"
                        data-message="Explain Python in simple words">
                        <span>⌘</span>
                        Explain Python simply
                    </button>

                    <button class="suggestion"
                        data-message="Help me learn programming">
                        <span>◇</span>
                        Help me learn programming
                    </button>

                </div>

            </div>
        `;

        input.value = "";

        input.focus();

    });

}
