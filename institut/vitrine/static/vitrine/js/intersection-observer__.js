
var haut=0

function createObserver(){
  options={
    root:null,
    rootMargin:"0px",
    threshold:0.5
  }

   var   observer=new IntersectionObserver(callBack, options)
   return observer

}

var callBack=(entries, observer)=>{
    if(haut==1){
      entries.forEach((entry) => {
        if(entry.target.classList.contains("hidden-tml")){
          console.log("TMLLLLLLLLLLLLLLLLll")
            entry.target.classList.replace("hidden-tml", "visible-tml");
            observer.unobserve(entry.target)
        }

              console.log(entry.target)
              console.log(entry.intersectionRatio)
    })
  }
    else{
      haut=1;
    }


  }



var observer=createObserver();
//document.querySelectorAll(".hidden-tml").forEach(elt=> {
  //observer.observe(elt);
//});
var cible=document.querySelector(".hidden-tml");
observer.observe(cible)
