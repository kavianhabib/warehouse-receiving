// Get the modal
function showModelPopup(){
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}

window.onclick = function(event) {
    var modal = document.getElementById("myModal");
    if (event.target == modal) {
      closeModelPopup();
    }
  }

function closeModelPopup(){
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

