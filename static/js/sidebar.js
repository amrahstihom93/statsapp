$("#navbarDropdown").click(function(e) {
  e.preventDefault();
  $("#sidebar").toggleClass("active");
  var clsname=document.getElementById("cntnt");
  var dd = clsname.getAttribute("class");
  console.log(clsname);
  console.log(dd);
  if(dd=="full-cntnt"){
    dd="full-cntnt1";
    $("#cntnt").toggleClass("content").toggleClass("full-cntnt1");
    console.log(dd);
  }
  else{
      dd="content full-cntnt";
      $("#cntnt").toggleClass("content").toggleClass("full-cntnt");
      console.log(dd);
  }
});
