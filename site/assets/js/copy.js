// "Copy prompt" buttons for the prompt boxes (layouts/_shortcodes/prompt.html).
// Plain JavaScript, no libraries; inlined into the home page like flip.js.
(function () {
  "use strict";

  var RESET_MS = 2200;

  // Older browsers, or pages not served over HTTPS, have no async clipboard API.
  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-1000px";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  // If copying fails, select the visible prompt so the reader can copy it by hand.
  function selectText(el) {
    var sel = window.getSelection && window.getSelection();
    if (!sel) return;
    var range = document.createRange();
    range.selectNodeContents(el);
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function setup(box) {
    var btn = box.querySelector(".prompt-copy");
    var src = box.querySelector(".prompt-source");
    var body = box.querySelector(".prompt-body");
    var label = box.querySelector(".prompt-copy-text");
    var status = box.querySelector(".prompt-status");
    if (!btn || !src || !label || btn.getAttribute("data-ready")) return;
    btn.setAttribute("data-ready", "1");
    var original = label.textContent;
    var timer;

    function finish(ok) {
      btn.classList.toggle("is-copied", ok);
      label.textContent = ok ? "Copied!" : "Select and copy";
      if (status) status.textContent = ok ? "Prompt copied to clipboard." : "Couldn't copy automatically. The prompt is selected; press Ctrl+C or Cmd+C.";
      if (!ok && body) selectText(body);
      clearTimeout(timer);
      timer = setTimeout(function () {
        btn.classList.remove("is-copied");
        label.textContent = original;
        if (status) status.textContent = "";
      }, RESET_MS);
    }

    btn.addEventListener("click", function () {
      var text = src.value;
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(
          function () { finish(true); },
          function () { finish(legacyCopy(text)); }
        );
      } else {
        finish(legacyCopy(text));
      }
    });
    btn.hidden = false;
  }

  function init() {
    var boxes = document.querySelectorAll(".prompt");
    for (var i = 0; i < boxes.length; i++) setup(boxes[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
