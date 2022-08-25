
var haut=true

const ratio=.2;
document.addEventListener("DOMContentLoaded", function(){

 var observer=createObserver();
 document.querySelectorAll(".hidden-tml").forEach(elt=> {
   observer.observe(elt);
 });


})


function createObserver(){
  options={
    root:null,
    rootMargin:"0px",
    threshold:ratio
  }

   var   observer=new IntersectionObserver(callBack, options)
   return observer

}

var callBack=(entries, observer)=>{
    entries.forEach((entry) => {

      if(entry.boundingClientRect.y<0){
        entry.target.classList.replace("hidden-tml", "visible-tml")
        observer.unobserve(entry.target)
      }
      if(entry.isIntersecting){


          entry.target.classList.replace("hidden-tml", "visible-tml");
          observer.unobserve(entry.target)
      }

      //console.log(entry.target)
      //console.log(entry.intersectionRatio)

  })
}
