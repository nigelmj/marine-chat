document.addEventListener("DOMContentLoaded", function () {
  const md = window.markdownit();

  document.querySelectorAll("[data-markdown]").forEach(function (element) {
    const markdownText = element.getAttribute("data-markdown");
    if (markdownText) {
      element.innerHTML = md.renderInline(markdownText);
    }
  });
});
