$("#navbarDropdown").click(function(e) {
  e.preventDefault();
  var x = document.getElementById("sidebar");
  var y = document.getElementById("sidebar2");
  $("#sidebar").toggleClass("active");
  var clsname=document.getElementById("cntnt");
  var dd = clsname.getAttribute("class");
  console.log(clsname);
  console.log(dd);

  if(dd == "content full-cntnt"){
      clsname.classList.remove("full-cntnt");
      clsname.classList.add("full-cntnt1");
  }
  else{
      clsname.classList.remove("full-cntnt1");
      clsname.classList.add("full-cntnt");
  }
});


$('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('div').toggle();
    e.stopPropagation();
    e.preventDefault();
});


/*$(document).ready(function() {
    var timer;
    var delay = 100;
    $(".y").mouseover(function () {
        console.log("mouseover");
        var x = document.getElementById("sidebar");
        var y = document.getElementById("sidebar2");
        x.style.display = "inline-block";
        y.style.display = "none"
    }),
    $(".x").mouseout(function () {

            console.log("mouseout");
            'mouseover': function () {
        timer = setTimeout(function () {
            var x = document.getElementById("sidebar");
            var y = document.getElementById("sidebar2");
                x.style.display = "none";
                y.style.display = "inline-block"
        }, 1000);
    },
    'mouseout' : function () {
        clearTimeout(timer);
    }

    });
});*/
