document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");

  // Function to add a message to the chat
  function addMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.textContent = `${sender}: ${message}`;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Handle sending a message
  sendButton.addEventListener("click", async () => {
    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    // Add user message to chat
    addMessage("You", userMessage);

    // Clear input field
    userInput.value = "";

    // Call the API to get the bot's response
    try {
      const botResponse = await fetchBotResponse(userMessage);
      addMessage("Bot", botResponse);
    } catch (error) {
      addMessage("Bot", "Sorry, I encountered an error. Please try again.");
    }
  });

  // Fetch bot response from API
  async function fetchBotResponse(message) {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch bot response");
    }

    const data = await response.json();
    return data.response;
  }
});
