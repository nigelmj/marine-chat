document.addEventListener("DOMContentLoaded", function () {
  const md = window.markdownit();

  document.querySelectorAll(".query").forEach(function (element) {
    const plainText = element.textContent;
    if (plainText) {
      const markdownText = md.render(plainText);
      element.innerHTML = markdownText;
    }
  });
  scrollToBottom();

  const form = document.querySelector(".query-form");
  if (form) {
    form.addEventListener("submit", handleFormSubmission);
  }
});

// Function to scroll to the bottom of the chat container
function scrollToBottom() {
  const contentDiv = document.querySelector(".content");
  contentDiv.scroll({
    top: contentDiv.scrollHeight,
    behavior: "smooth",
  });
}

// Function to render messages
function appendMessage(message) {
  const md = window.markdownit();

  const messageDiv = document.createElement("div");
  const messageP = document.createElement("p");

  messageP.innerHTML = md.render(message.fields.message);

  if (message.fields.sender === "user") {
    messageDiv.classList.add("query-message-container");
    messageP.classList.add("query-message");

    messageDiv.appendChild(messageP);
  } else {
    const logoDiv = document.createElement("div");
    logoDiv.classList.add("logo-circle");

    const logoImg = document.createElement("img");
    logoImg.src = "/static/marinechat/assets/ship.svg";
    logoImg.alt = "Logo";
    logoImg.classList.add("logo-svg");

    logoDiv.appendChild(logoImg);

    const replyContainer = document.createElement("div");
    replyContainer.classList.add("query-reply-container");

    replyContainer.appendChild(messageP);

    messageDiv.classList.add("query-reply-section");
    messageDiv.appendChild(logoDiv);
    messageDiv.appendChild(replyContainer);
  }

  const messagesContainer = document.querySelector(".chat-container");
  messagesContainer.appendChild(messageDiv);

  scrollToBottom();
}

// Function to handle form submission
function handleFormSubmission(event) {
  event.preventDefault();
  const query = document.querySelector(".query-input").value;
  sendQueryToServer(query);
}

// Function to send the query to the server
function sendQueryToServer(query) {
  fetch("/marinechat/query/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      query: query,
    }),
  })
    .then((response) => response.json())
    .then((data) => handleServerResponse(data))
    .catch((error) => console.error("Error:", error));
}

// Function to handle the server response
function handleServerResponse(data) {
  if (data.error) {
    console.error(data.error);
  } else {
    const messages = JSON.parse(data.messages);

    appendMessage(messages[messages.length - 2]);
    appendMessage(messages[messages.length - 1]);
    document.querySelector(".query-input").value = "";
  }
}

// Function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
