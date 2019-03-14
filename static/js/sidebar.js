$("#navbarDropdown").click(function(e) {
  e.preventDefault();
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
