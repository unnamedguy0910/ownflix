const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

chatSend.addEventListener('click', () => {
    if (chatInput.value.trim() === '') return;
    chatSocket.send(JSON.stringify({message: chatInput.value}));
    chatInput.value = '';
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        chatSend.click();
    }
});

// Function to display messages (called inside chatSocket.onmessage)
function displayMessage(username, message, timestamp) {
    const msgDiv = document.createElement('div');
    msgDiv.textContent = `[${new Date(timestamp).toLocaleTimeString()}] ${username}: ${message}`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Emoji reactions example
function showReaction(emoji) {
    const reaction = document.createElement('div');
    reaction.classList.add('reaction');
    reaction.textContent = emoji;
    reaction.style.left = Math.random() * window.innerWidth + 'px';
    reaction.style.top = window.innerHeight + 'px';
    document.body.appendChild(reaction);
    setTimeout(() => reaction.remove(), 3000);
}
