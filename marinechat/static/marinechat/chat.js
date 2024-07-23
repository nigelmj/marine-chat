document.addEventListener("DOMContentLoaded", function () {
  const md = window.markdownit();

  document.querySelectorAll("[data-markdown]").forEach(function (element) {
    const markdownText = element.getAttribute("data-markdown");
    if (markdownText) {
      element.innerHTML = md.render(markdownText);
    }
  });
  scrollToBottom();
});

// Function to scroll to the bottom of the chat container
function scrollToBottom() {
  const contentDiv = document.querySelector(".content");
  contentDiv.scroll({
    top: contentDiv.scrollHeight,
    behavior: "smooth",
  });
}
