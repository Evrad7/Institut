$(document).ready(function(){
  $(".owl-carousel").owlCarousel({
    items:1,
    //loop:true,
    dots:false,
    //center:true,
    nav:true,
    stagePadding:8,
    merge:true,
    //mergeFit:false,
    autoWidth:true,
    autoplay:true,
    smartSpeed:100,
    autoplayTimeout:3500,
    rewind:true,
    autoplayHoverPause:true,

    responsive:{
      576:{
        items:2,
      },
      720:{
        items:3,
      }
    }
  })


})
