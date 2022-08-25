$(document).ready(function(){

  $(" .search-1 .dropdown-menu .dropdown-item").each(function(index){

  $(this).on("click", function(){
      $(".search-1  button input").attr("value",$(this).text());
        $(".search-1  button input").attr("pk_cycle", $(this).attr("pk_cycle"));
  })
  }
  )

  $(" .search-2 .dropdown-menu .dropdown-item").each(function(index){

    $(this).on("click", function(){
      $(".search-2  button input").attr("value",$(this).text());
      $(".search-2  button input").attr("pk_filiere", $(this).attr("pk_filiere"));
      })
    }
    )

    $("#form").on("click", function(e){
      rechercheAjax()
    })
})

var rechercheAjax=function(){
  var search=$(".search input").val()
  var cycle=$(".search-1 input").attr("pk_cycle")
  var filiere=$(".search-2 input").attr("pk_filiere")

  var request=$.ajax({
    url:"/vitrine/inscription/?search="+search+"&cycle="+cycle+"&filiere="+filiere,
    type:"GET",
    processData:false,
		contentType:false,
		cache:false,
		asynch:true,
    beforeSend: function(){
      $("#form").append(" <span  id='spinner-search' class=' spinner-border spinner-border-sm text-light'></span>")
    },
  })
  request.done(function(response){
    $("#spinner-search").remove()

    $("#specialites").html("")
    if (response.specialites.length==0){
      $("#specialites").html("Aucune spécialité trouvée")
    }
    else{
      $.each(response.specialites, function(i, specialite){
        $("#specialites").append("\
          <div class='col-12 col-sm-6 col-md-4 col-lg-3  my-2'>\
            <div class='filieres text-center'> <i class='bi bi-dash text-danger'></i> <a href='#' class='text-decoration-none link-dark'>\
            "+specialite.nom_cycle+"/"+specialite.nom_filiere+"/<span class='fw-bold'>"+specialite.nom+" "+specialite.niveau+"</span></a> </div>\
          </div>")
      })

    }

  })
  request.fail(function(response){
    $("#spinner-search").remove()
    $("#specialites").html("error système")
  }

)
}
