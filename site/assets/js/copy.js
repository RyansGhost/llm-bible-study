// Copy buttons: the home page's prompt boxes (layouts/_shortcodes/prompt.html)
// and each book page's "Copy … Study Guide Markdown" button (layouts/page.html).
// A box holds the button, a hidden .prompt-source textarea with the exact text,
// and an optional .prompt-body to select if copying fails. data-copied names
// what was copied for screen readers. Plain JavaScript, no libraries; inlined.
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
    var url = box.getAttribute("data-copy-url");
    var body = box.querySelector(".prompt-body");
    var label = box.querySelector(".prompt-copy-text");
    var status = box.querySelector(".prompt-status");
    if (!btn || !(src || url) || !label || btn.getAttribute("data-ready")) return;
    btn.setAttribute("data-ready", "1");
    var original = label.textContent;
    var what = box.getAttribute("data-copied") || "Prompt";
    var timer;

    function finish(ok) {
      btn.classList.toggle("is-copied", ok);
      label.textContent = ok ? "Copied!" : (body ? "Select and copy" : "Couldn't copy");
      if (status) status.textContent = ok ? what + " copied to clipboard." :
        (body ? "Couldn't copy automatically. The text is selected; press Ctrl+C or Cmd+C."
              : "Couldn't copy automatically. Use View as markdown and copy the page.");
      if (!ok && body) selectText(body);
      clearTimeout(timer);
      timer = setTimeout(function () {
        btn.classList.remove("is-copied");
        label.textContent = original;
        if (status) status.textContent = "";
      }, RESET_MS);
    }

    // Book pages: fetch the text (books/<book>/index-for-copy.md) on click, so it
    // never sits in the page's HTML. Passing a promise to ClipboardItem keeps the
    // click's permission in Safari while the request runs; browsers without
    // ClipboardItem (older Firefox) wait for the text and then use writeText.
    function copyFromUrl() {
      if (btn.getAttribute("aria-busy") === "true") return;
      btn.setAttribute("aria-busy", "true");
      var done = function (ok) { btn.removeAttribute("aria-busy"); finish(ok); };
      var text = fetch(url, { credentials: "same-origin" }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      });
      if (!navigator.clipboard || !window.isSecureContext) {
        text.then(function (t) { done(legacyCopy(t)); }, function () { done(false); });
        return;
      }
      if (window.ClipboardItem && navigator.clipboard.write) {
        var item = new ClipboardItem({
          "text/plain": text.then(function (t) { return new Blob([t], { type: "text/plain" }); })
        });
        navigator.clipboard.write([item]).then(
          function () { done(true); },
          function () { text.then(function (t) { return navigator.clipboard.writeText(t); }).then(function () { done(true); }, function () { done(false); }); }
        );
      } else {
        text.then(function (t) { return navigator.clipboard.writeText(t); }).then(function () { done(true); }, function () { done(false); });
      }
    }

    btn.addEventListener("click", function () {
      if (url) { copyFromUrl(); return; }
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
    var boxes = document.querySelectorAll(".prompt, .guide-copy");
    for (var i = 0; i < boxes.length; i++) setup(boxes[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
