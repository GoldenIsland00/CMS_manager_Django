document.addEventListener("DOMContentLoaded", function () {
  // Product gallery: clicking a thumbnail swaps the main image
  var mainImage = document.getElementById("mainImage");
  var thumbs = document.querySelectorAll(".thumb-btn");

  thumbs.forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!mainImage) return;
      mainImage.src = btn.getAttribute("data-full");
      thumbs.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
    });
  });
});
