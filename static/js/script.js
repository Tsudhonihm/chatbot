document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");

  // Favicon elements
  const faviconLink = document.querySelector("link[rel*='icon']") || document.createElement('link');
  faviconLink.type = 'image/x-icon';
  faviconLink.rel = 'shortcut icon';
  document.head.appendChild(faviconLink);

  // Check if elements exist
  if (!messagesContainer || !userInput || !sendButton) {
    console.error("Error: Required DOM elements not found!");
    return;
  }

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

    // Animate favicon while waiting for bot response
    animateFavicon();

    // Call the Flask backend to get the bot's response
    try {
      const botResponse = await fetchBotResponse(userMessage);
      addMessage("Bot", botResponse);
    } catch (error) {
      console.error("Error fetching bot response:", error);
      addMessage("Bot", "Sorry, I encountered an error. Please try again.");
    } finally {
      // Restore the default favicon after the response
      restoreDefaultFavicon();
    }
  });

  // Fetch bot response from Flask backend
  async function fetchBotResponse(message) {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) {
      throw new Error("Failed to fetch bot response");
    }
    const data = await response.json();
    return data.response;
  }

  // Favicon Animation Logic
  const defaultFavicon = "/static/favicons/favicon.gif"; // Default animated favicon
  const activeFavicon = "/static/favicons/active-favicon.gif"; // Favicon for active state

  function animateFavicon() {
    faviconLink.href = activeFavicon; // Change to active favicon
  }

  function restoreDefaultFavicon() {
    faviconLink.href = defaultFavicon; // Restore default favicon
  }
});
