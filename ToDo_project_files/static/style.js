str = document.getElementById('do')
mark = document.querySelector(".strike")

document.getElementById("heading").addEventListener("mouseover", mouseOver);
document.getElementById("heading").addEventListener("mouseout", mouseOut);

mark.addEventListener("click", strikechange);

function strikechange() {
    str.classList.toggle("strikes");
}

function mouseOver() {
  document.getElementById("heading").style.color = "darkcyan";
}

function mouseOut() {
  document.getElementById("heading").style.color = "black";
}