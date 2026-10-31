// Split-flap ("flip clock") word changer for the home page heading.
// <span class="flip" data-words='["Claude","ChatGPT"]'>Claude</span>
(function () {
  "use strict";

  var INTERVAL_MS = 3000;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function half(cls, word) {
    var outer = document.createElement("span");
    outer.className = "flip-half " + cls;
    var inner = document.createElement("span");
    inner.textContent = word;
    outer.appendChild(inner);
    return outer;
  }

  function setWord(el, word) {
    el.firstChild.textContent = word;
  }

  function init(card) {
    var words;
    try {
      words = JSON.parse(card.getAttribute("data-words") || "[]");
    } catch (e) {
      return;
    }
    if (!words || words.length < 2) return;

    var current = 0;

    // The server-rendered sizer holds invisible copies of every word in one
    // grid cell, so the card already has the widest word's width; keep it and
    // replace the static word with the flip layers.
    var sizer = card.querySelector(".flip-sizer");
    card.textContent = "";
    if (!sizer) {
      sizer = document.createElement("span");
      sizer.className = "flip-sizer";
      words.forEach(function (w) {
        var s = document.createElement("span");
        s.textContent = w;
        sizer.appendChild(s);
      });
    }

    var top = half("flip-top", words[0]);          // new word, top half
    var bottom = half("flip-bottom", words[0]);    // old word, bottom half
    var flapTop = half("flip-top flip-flap flip-flap-top", words[0]);          // old top, folds down
    var flapBottom = half("flip-bottom flip-flap flip-flap-bottom", words[0]); // new bottom, folds down

    [sizer, top, bottom, flapTop, flapBottom].forEach(function (n) { card.appendChild(n); });
    card.classList.add("is-ready");

    flapBottom.addEventListener("animationend", function () {
      setWord(bottom, words[current]);
      card.classList.remove("is-flipping");
    });

    setInterval(function () {
      if (document.hidden) return;
      var oldWord = words[current];
      current = (current + 1) % words.length;
      var newWord = words[current];

      if (reduceMotion) {
        setWord(top, newWord);
        setWord(bottom, newWord);
        return;
      }

      setWord(top, newWord);
      setWord(bottom, oldWord);
      setWord(flapTop, oldWord);
      setWord(flapBottom, newWord);
      card.classList.remove("is-flipping");
      void card.offsetWidth; // restart the animation
      card.classList.add("is-flipping");
    }, INTERVAL_MS);
  }

  document.querySelectorAll(".flip[data-words]").forEach(init);
})();
