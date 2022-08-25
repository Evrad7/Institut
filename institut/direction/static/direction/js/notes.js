$(document).ready(function(){
  var error_reseau=$(".status").attr("error")

  if(error_reseau==0){
    $(".status").html("<p class='text-success'> enregistrement réussi</p>")
    setTimeout(function(){
      $(".status").html("")
    }, 5000)
  }
  else if(error_reseau==1){
    $(".status").html("<p class='text-danger'> Enregistrement échoué</p>")
    setTimeout(function(){
      $(".status").html("")
    }, 5000)
  }
  else{
    $(".status").html("<p class='text-danger'>"+error_reseau+"</p>")
    setTimeout(function(){
      $(".status").html("")
    }, 5000)
  }
  var id_error=$(".status").attr("id-error")
    if (id_error!=""){
  id_error=id_error.substring(0, id_error.length-1)
  id_error=id_error.split("/")
    id_error.forEach(function(item, i){
      $("#"+item).css("box-shadow", "0px 0px 0px 0.25rem red  ")
    })
  }


  var error=false
  var regex=new RegExp("^([0-9]{1,2}?(,[0-9]{1,2})?)?$")
  var notes=$("input.notes")
  notes.each(function(i){
    $(this).on("keyup", function(e){

      if(!regex.test($(this).val())){
        $(this).addClass("text-danger")
        error=true
      }
      else{
        $(this).removeClass("text-danger")
        error=false
      }

    })
  })
  $("#form").on("click", function(e){
    if(error){
      $(".status").html("<p class='text-danger'> Le format des notes est incorrect</p>")
      setTimeout(function(){
        $(".status").html("")
      }, 5000)
    }
    else{
      $("form").submit()
    }
  })
})
