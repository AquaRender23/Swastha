function sendMessage(){
  const text = userInput.value.trim();
  if(!text) return;
  addMessage("user", text);
  userInput.value = "";

  // Add loading message
  addMessage("sia", "💜 SIA: Thinking...");

  fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: text})
  })
  .then(res => res.json())
  .then(data => {
    // Remove loading message
    messages.removeChild(messages.lastChild);
    addMessage("sia", "💜 SIA: " + data.answer);
  })
  .catch(err => {
    messages.removeChild(messages.lastChild);
    addMessage("sia", "💜 SIA: Sorry, network error.");
  });
}
