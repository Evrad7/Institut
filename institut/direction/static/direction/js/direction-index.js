document.addEventListener("DOMContentLoaded", function(){
 var il=document.querySelectorAll(".vertical-bar ul li");

 il.forEach((item) => {
   item.addEventListener("click", verticalBar)
 });

 var menus=document.querySelectorAll(".main .top .menu i, .menu-2");
 var main=document.querySelector(".main")
 verticalBar=document.querySelector(".vertical-bar")
 menus.forEach(item => {
   item.addEventListener("click", function(e){
     main.classList.toggle("active")
     verticalBar.classList.toggle("active")
   })
 });

 tr=document.querySelectorAll("#table-list tr.item")
 console.log(tr)
 tr.forEach(item=>{
  item.addEventListener("click", function(e){
    e.stopPropagation()
    document.location.replace(this.getAttribute("url"))
  }, false)
 })



 
})


var verticalBar=function(){
  var il=document.querySelectorAll(".vertical-bar ul li");
  il.forEach(item => {
    item.classList.remove("active")
    this.classList.add("active")

  });
}

