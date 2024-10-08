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
  if (contentDiv) {
    contentDiv.scroll({
      top: contentDiv.scrollHeight,
      behavior: "smooth",
    });
  }
}

function truncateText(text, maxLength) {
  if (text.length > maxLength) {
    return text.slice(0, maxLength) + "...";
  }
  return text;
}

function appendQuery(query) {
  const md = window.markdownit();

  const messageDiv = document.createElement("div");
  const messageP = document.createElement("p");

  messageP.innerHTML = md.render(query);
  messageP.classList.add("query-message");

  messageDiv.appendChild(messageP);
  messageDiv.classList.add("query-message-container");

  const messagesContainer = document.querySelector(".chat-container");
  messagesContainer.appendChild(messageDiv);
}

function appendReply(message) {
  const md = window.markdownit();

  const messageP = document.querySelector(".temp-cursor");
  messageP.innerHTML = "";
  messageP.classList.remove("temp-cursor");

  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = md.render(message.message);

  appendCitation(message, tempDiv);

  var typing = new Typing({
    source: tempDiv,
    output: messageP,
    delay: 30,
  });
  typing.start();

  tempDiv.remove();
}

function appendCitation(message, tempDiv) {
  if (message.citations.length > 0) {
    const citationDiv = document.createElement("div");
    citationDiv.classList.add("citation-container");

    citationDiv.innerHTML += "References:<br>";
    message.citations.forEach((citation, index) => {
      const referenceNumber = `${index + 1}. `;
      const truncatedQuote = truncateText(citation.quote, 100);

      const sourceURL = `/marinechat/document/${citation.source.id}/`;

      const citationP = document.createElement("p");
      citationP.classList.add("citation-paragraph");

      const citationLink = document.createElement("a");
      citationLink.href = sourceURL;
      citationLink.innerHTML = `${referenceNumber} ${truncatedQuote}`;
      citationLink.classList.add("citation-link");

      citationP.appendChild(citationLink);
      citationDiv.appendChild(citationP);
      citationDiv.style.marginBottom = "1rem";
    });

    tempDiv.appendChild(citationDiv);
  }
}

function createTempCursor() {
  const messageDiv = document.createElement("div");
  const messageP = document.createElement("p");

  const logoDiv = document.createElement("div");
  logoDiv.classList.add("logo-circle");

  const logoImg = document.createElement("img");
  logoImg.src = "/static/marinechat/assets/ship.svg";
  logoImg.alt = "Logo";
  logoImg.classList.add("logo-svg");

  logoDiv.appendChild(logoImg);

  const replyContainer = document.createElement("div");
  replyContainer.classList.add("query-reply-container");

  messageP.classList.add("temp-cursor");
  messageP.classList.add("query-reply");
  messageP.innerHTML = "Thinking";

  replyContainer.appendChild(messageP);

  messageDiv.classList.add("query-reply-section");
  messageDiv.appendChild(logoDiv);
  messageDiv.appendChild(replyContainer);

  const messagesContainer = document.querySelector(".chat-container");
  messagesContainer.appendChild(messageDiv);

  scrollToBottom();
}
// Function to handle form submission
function handleFormSubmission(event) {
  event.preventDefault();
  const query = document.querySelector(".query-input").value;

  appendQuery(query);
  document.querySelector(".query-input").value = "";
  createTempCursor();

  sendQueryToServer(query);
  removeIntro();
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
    const messages = data.messages;
    appendReply(messages[messages.length - 1]);
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

function removeIntro() {
  const intro = document.querySelector(".welcome-message");
  if (intro) {
    intro.remove();
  }
}
