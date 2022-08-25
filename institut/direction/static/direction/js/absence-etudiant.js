$(document).ready(function(){
$("tr td.presence").each(function(){
  $(this).on("click", function(e){
    e.preventDefault()
   if ($(this).attr("present")=="1"){
     $(this).attr("present", "0")
     $(this).html("<div class='text-center text-danger'> <i class='bi bi-x fs-2'></i></div>")
   }
   else{
     $(this).attr("present", "1")
     $(this).html("")
   }
  })
})
var form=$("form")
$("#register").on("click", function(e){
  e.preventDefault()
  var presences=$("tr td.presence")
  if(presences.length>0){
    presences.each(function(){

      form.append("<input type='hidden' name='"+$(this).attr("id")+"' value='"+$(this).attr("present")+"'/>")
    })
  }
  form=$("form")

  form.submit()


})

})
