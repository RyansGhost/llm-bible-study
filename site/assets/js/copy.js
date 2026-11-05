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
    // .guide-copy boxes fetch their text from data-copy-url, read at click time
    // because the home page's book picker changes it.
    var isGuide = box.classList.contains("guide-copy");
    var pick = box.querySelector(".guide-pick");
    var body = isGuide ? null : box.querySelector(".prompt-body");
    var label = box.querySelector(".prompt-copy-text");
    var status = box.querySelector(".prompt-status");
    if (!btn || !(src || isGuide) || !label || btn.getAttribute("data-ready")) return;
    btn.setAttribute("data-ready", "1");
    var original = label.textContent;
    var timer;

    function finish(ok) {
      btn.classList.toggle("is-copied", ok);
      label.textContent = ok ? "Copied!" : (body ? "Select and copy" : "Couldn't copy");
      var what = box.getAttribute("data-copied") || "Prompt";
      if (status) status.textContent = ok ? what + " copied to clipboard." :
        (body ? "Couldn't copy automatically. The text is selected; press Ctrl+C or Cmd+C."
         : pick ? "Couldn't copy automatically. Open the book's page from the list below and use its Copy Study Guide button."
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
    function copyFromUrl(url) {
      if (!url || btn.getAttribute("aria-busy") === "true") return;
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
      if (isGuide) { copyFromUrl(box.getAttribute("data-copy-url")); return; }
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
    if (pick) setupPicker(box, pick, btn);
    btn.hidden = false;
  }

  // Home page book picker: choosing a book points the box at that book's
  // index-for-copy.md and enables the button. ?book=<slug> preselects a book;
  // otherwise the last choice is remembered in this browser (a convenience only).
  var PICK_KEY = "bible-study:book";
  function setupPicker(box, pick, btn) {
    function choose() {
      var opt = pick.options[pick.selectedIndex];
      var url = pick.value;
      if (url) {
        box.setAttribute("data-copy-url", url);
        box.setAttribute("data-copied", (opt.getAttribute("data-title") || "Study") + " study guide");
        btn.setAttribute("aria-label", "Copy the " + (opt.getAttribute("data-title") || "") + " study guide");
      } else {
        box.removeAttribute("data-copy-url");
      }
      btn.disabled = !url;
      try { if (url) localStorage.setItem(PICK_KEY, opt.getAttribute("data-slug") || ""); } catch (e) {}
    }
    var want = null;
    try { want = new URLSearchParams(location.search).get("book"); } catch (e) {}
    if (!want) { try { want = localStorage.getItem(PICK_KEY); } catch (e) {} }
    if (want) {
      for (var i = 0; i < pick.options.length; i++) {
        if (pick.options[i].getAttribute("data-slug") === want) { pick.selectedIndex = i; break; }
      }
    }
    pick.addEventListener("change", choose);
    choose();
    var row = box.querySelector(".guide-pick-row");
    if (row) row.hidden = false;
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
