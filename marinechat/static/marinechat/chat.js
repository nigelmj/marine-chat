document.addEventListener("DOMContentLoaded", function () {
  const md = window.markdownit();

  document.querySelectorAll(".query").forEach(function (element) {
    const plainText = element.innerHTML;
    if (plainText) {
      const markdownText = md.render(plainText);
      element.innerHTML = markdownText;
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
