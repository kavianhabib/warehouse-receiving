
   window.onload = function () {
     window.document.body.addEventListener('keydown', function(event){
        if( event.keyCode == 13 || event.keyCode == 16 ||  event.keyCode == 17 ) {
                event.preventDefault();
                    return;
                }

                if(event.ctrlKey) {
                    event.preventDefault()
                    document.getElementById("myForm").submit();
                    return;
                }
    });
}


    // When the user clicks on <div>, open the popup
function myFunction() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

function loadScreen(){
  let load_screen = document.getElementById("load_screen");
  load_screen.classList.remove("modal");
  load_screen.classList.add("modal-view");
  document.getElementById("bulk_add_form").submit();
}

function loadPO(){
  let load_screen = document.getElementById("load_screen");
  // load_screen.classList.remove("modal");
  // load_screen.classList.add("modal-view");
  document.getElementById("po_upload").submit();
}

