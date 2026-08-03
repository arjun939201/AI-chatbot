async function sendMessage() {
  const messageInput = document.getElementById('userMessage');
  const message = messageInput.value.trim();
  if (!message) return;

  const response = await fetch('/chatbot/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  messageInput.value = '';
  renderHistory(data.history);
}

async function clearHistory() {
  const response = await fetch('/chatbot/clear', { method: 'POST' });
  const data = await response.json();
  renderHistory(data.history);
}

function renderHistory(history) {
  const container = document.getElementById('chatContainer');
  if (!history || history.length === 0) {
    container.innerHTML = '<p>ఇంకా సందేశాలు లేవు. దిగువన మీ మొదటి సందేశాన్ని పంపండి.</p>';
    return;
  }
  container.innerHTML = history.map(entry => `
    <div class="message ${entry.role}">
      <strong>${entry.role === 'user' ? 'మీరు' : 'TelAI'}:</strong>
      <div>${entry.text}</div>
    </div>
  `).join('');
}
