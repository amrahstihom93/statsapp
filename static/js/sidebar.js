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
      x.style.display = "none";
      y.style.display = "inline-block";
  }
  else{
      clsname.classList.remove("full-cntnt1");
      clsname.classList.add("full-cntnt");
      x.style.display = "inline-block";
      y.style.display = "none";
  }
});


$('.dropdown-submenu a.test').on("click", function(e){
    $(this).next('div').toggle();
    e.stopPropagation();
    e.preventDefault();
});
