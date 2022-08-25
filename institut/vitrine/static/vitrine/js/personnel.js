
//$(document).ready(function(){
  //$(".owl-carousel").owlCarousel({
    //items:2,

    //dots:true
  //})
//})
 active=false;
$(document).ready(function(){
  $(".owl-carousel").owlCarousel({
    items:1,

    center: false,
     dotClass:"point",

  });

  $(" .search-1 .dropdown-menu .dropdown-item").each(function(index){

  $(this).on("click", function(){
      $(".search-1  button input").attr("value",$(this).text());
  })
  }
  )

  $(" .search-2 .dropdown-menu .dropdown-item").each(function(index){

    $(this).on("click", function(){
      $(".search-2  button input").attr("value",$(this).text());
      })
    }
    )

    $(".form-tml input").on("focusin", function(){
    //  console.log("TMLLLL");

      //$(".form-tml input:focus ~ label").css("display", "block");
    //  $(".form-tml input:focus ~ label").css("animation", "translater-haut .5s 0s forwards 1")
    })


    console.log($(".menu-cours  div > button").offset());
    //pos=$(".menu-cours div > button").offset();
    //$(".offcanvas-end").offset({top:pos.top, left:pos.left});

  $(".menu-cours ul li").each(function(index){
    $(this).on("click", function(){
     $(".menu-cours ul li.active").removeClass("active");
     $(this).addClass("active");


     $(".menu-cours  div  button.canvas-tml").text($(this).text());
     var canvas=$(".offcanvas");
    // canvas=new bootstrap.Offcanvas(canvas);
     //console.log(canvas);

    // console.log(s)
    $("table tr.cours").on("click", function(){
      console.log(this);
    })



    })
  })
  $("table tr.cours").on("click", function(){
    console.log(this);
    document.location.replace($(this).attr("data-cours"));
  });
  mode_jour=false;
  $(".menu-cours div  div.toggle").on("click", function(){
    if (mode_jour){
      $(".menu-cours div > div span").html("Mode <br/> sombre");
      $(".menu-cours div > div i").removeClass("bi bi-toggle-on").addClass("bi bi-toggle-off");
      $("table").removeClass("table-dark text-light").addClass("table-light text-dark");
      mode_jour=false;

    }
    else {
      $(".menu-cours div > div span").html("Mode <br/> clair");
      $(".menu-cours div > div i").removeClass("bi bi-toggle-off").addClass("bi bi-toggle-on");
      $("table").removeClass("table-light text-dark").addClass("table-dark text-light");
      mode_jour=true;
    }
    })

}
);


var mot1="Réalisez vos rêves";
var mot2="Devenez compétant";

let textAnimation=function(mot1, mot2){
  var texteur="|";
  var tab1=mot1.split("")
  var tab2=mot2.split("");

}
