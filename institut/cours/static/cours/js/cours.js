$(document).ready(function(){
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


    $(".form-ajax").on("click", function(e){
      var search=$(this).parents("form").find("input").val()
      var searchBy=$(this).parents("form").find("select").val()
      formAjax(search, searchBy)
    })
})

var formAjax=function(search, searchBy){
  var request=$.ajax({
    url: "/cours/?search="+search+"&search-by="+searchBy,
    type:"GET",
    processData:false,
		contentType:false,
		cache:false,
		asynch:true,
    beforeSend: function(){

    },

  })
  request.done(function(response){
    $("table tr.cours").remove()
    $.each(response.cours, function(i, object){
      $("table").append("<tr  class='cours' data-cours='/cours/lire_cours/"+object.pk+"/'>\
          <td>"+object.titre+"</td>\
          <td>"+object.discipline+"</td>\
          <td>"+object.auteur+"</td>\
          <td>"+object.description+"</td>\
          <td>"+object.support+"</td>\
          <th>"+object.duree+"h</th>\
        </tr>")

    })

  })
  request.fail(function(response){
//console.log(response)
  })
}
