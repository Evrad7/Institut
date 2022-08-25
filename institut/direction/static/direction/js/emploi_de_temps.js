var menuMatiere=false
var pk_professeur=""
var pk_matiere=null
var pk_specialite=null
var noms_professeur=""
document.addEventListener("DOMContentLoaded", function(){

	cases=document.querySelectorAll(".case")

	cases.forEach(item=>{
		item.addEventListener("mouseover", function(e){
			e.target.classList.add("border-tml")

		})
		item.addEventListener("mouseleave", function(e){
			e.target.classList.remove("border-tml")
		})

	})

	$(".owl-carousel").owlCarousel({
		items:6,
		autoWidth:true,
		nav:true,
		dots:false,
		navClass:["nav-prev-tml", "nav-next-tml"],


	})


	var cases=$("table tr td.case")
	cases.each(function(){
		matiere=$(this).attr("matiere")
		var clone=$("."+matiere+":first").clone()
		clone.addClass("owl-click")
		$(this).html(clone)
		id=$(this).attr("id")
		input=$("input#id_field_"+id+"[name='field_"+id+"']")
		input.val(matiere)


	})
	matiere=false

	var owls=$(".owl-carousel .owl-item .item")



	owls.each(function(){

		$(this).on("click", function(e){
			if($(this).hasClass("owl-click")){
			owls.each(function(){
				$(this).removeClass("owl-click")
				matiere=false
			})
		     }
		     else{
		     	owls.each(function(){
				$(this).removeClass("owl-click")
			   })
		     	$(this).addClass("owl-click")
		     	matiere=$(this).attr("matiere")

		     }
		})
	})
	cases.each(function(){
		$(this).on("click", function(e){
			if(matiere!==false){
				if($(this).attr("matiere")=="-"){
					
					

					matiere_=matiere.split("-")
					if(matiere_[1]!=""){
						selectionProfesseur1Ajax($(this).attr("id"), matiere_[1], $(this))
					}
					else{
						$(this).html($("."+matiere+":first").clone())
						petitMenuMatiere()
					    prepareAjax()
					    detailsMatiere()
						$(this).attr("matiere", matiere)
						id=$(this).attr("id")
						input=$("input#id_field_"+id+"[name='field_"+id+"']")
						input.val(matiere)
						$(this).removeClass("error-select-prof")

					}
					


				}
				else{

					$(this).attr("matiere", "-")
					$(this).empty()
					//petitMenuMatiere()
					//prepareAjax()
					id=$(this).attr("id")
					input=$("input#id_field_"+id+"[name='field_"+id+"']")
					input.val("-")


				}
			}
		})

	})
 $("form button").on("click", function(e){
	 e.preventDefault()
	 enregistrementAjax()
 })
	petitMenuMatiere()
	prepareAjax()
	detailsMatiere()
	$("button#search-matiere").on("click", function(){
		ajax(pk_matiere)
	})
	$("#chevron-left").on("click", function(){
		$(this).addClass("d-none")
		$(".menu-professeurs").removeClass("d-none")
	})
	$("#chevron-right").on("click", function(){
		$(".menu-professeurs").addClass("d-none")
		$("#chevron-left").removeClass("d-none")
	})

  detailsProfesseur()
	detailsMatiere()

			//$("#modalDetailsProfesseur modal modal-dialog modal-content modal-body").html()


})

var detailsProfesseur=function(){

	console.log($(".professeurs div p a"))
  $(".professeurs div p a").each(function(){
		$(this).on("click", function(e){
			e.preventDefault()
			e.stopPropagation()
			$("#modalDetailsProfesseur").modal("show")
			detailsProfesseurAjax($(this).attr("pk-professeur"))
		})
	})

}

var detailsMatiere=function(){
	$(".item div div ul li:nth-child(2) a").each(function(){
		$(this).on("click", function(e){
			e.preventDefault()
			var menu=$(" .item  div i.active")
			menu.removeClass("active")
			menu.next().addClass("d-none")
			$("#modalDetailsMatiere").modal("show")
			detailsMatiereAjax($(this).attr("matiere"))
		})
	})
}

var petitMenuMatiere=function(){
	var menus_matiere=$(" .item  div i.bi-three-dots-vertical")

	menus_matiere.each(function(){
		$(this).off("click")
		$(this).on("click", function(){
			if(!$(this).hasClass("active")){
				menus_matiere.each(function(){
					$(this).removeClass("active")
					$(this).next().addClass("d-none")
				})
				$(this).addClass("active")
				$(this).next().removeClass("d-none")

			}
				else{
					$(this).removeClass("active")
					$(this).next().addClass("d-none")

				}


		})
	})

}

var prepareAjax=function(){
	lis=$(".item div ul li:nth-child(1) a")
	lis.each(function(){
		$(this).on("click", function(e){
			e.preventDefault()
			pk_matiere=$(this).attr("matiere")
			pk_professeur=$(this).attr("professeur")
				var menu=$(" .item  div i.active")
				$("#chevron-left").addClass("d-none")
				$(".menu-professeurs").removeClass("d-none")
				menu.removeClass("active")
				menu.next().addClass("d-none")
				ajax(pk_matiere)
		})
	})

}
var selectProfesseur=function(){
	var professeurs=$("div.professeurs div p  ")
	professeurs.each(function(){
		$(this).on("click", function(){

			if(!$(this).hasClass("violet")){
				professeurs.removeClass("violet")
					$(this).addClass("violet")

					matieres=$("."+pk_matiere+"-"+pk_professeur)
					matieres.parent("td").removeClass("error-select-prof")

					
						matieres.parent("td").removeClass("error-select-prof")

					var cases=matieres.parent("td")
					parametre=""
					if(cases.length>0){

					cases.each(function(i){
						parametre+=$(this).attr("class").split(" ")[1]+"/"
						

					})
					parametre=parametre.substring(0, parametre.length-1)
					noms_professeur=$(this).children("span").first().html()
					inputs=$("[value="+pk_matiere+"-"+pk_professeur+"]")
					new_pk_professeur=$(this).attr("pk-professeur")
					selectionProfesseurAjax(parametre, new_pk_professeur, matieres, inputs, noms_professeur, $(this))
					}
					else{


					noms_professeur=$(this).children("span").first().html()
					matieres.removeClass(pk_matiere+"-"+pk_professeur)

					inputs=$("[value="+pk_matiere+"-"+pk_professeur+"]")
					pk_professeur=$(this).attr("pk-professeur")
			        matieres.addClass(pk_matiere+"-"+pk_professeur)
					matieres.attr("matiere", pk_matiere+"-"+pk_professeur)
					matieres.parent("td.case").attr("matiere", pk_matiere+"-"+pk_professeur)
					inputs.each(function(){
							$(this).val(pk_matiere+"-"+pk_professeur)
					})

					matieres.find("ul li a").attr("professeur", pk_professeur)


					matieres.find("span.professeur").each(function(){
						$(this).html(noms_professeur)
					})

					}
					
					
				
					
					
					
			}
			else{
				professeurs.each(function(){
					$(this).removeClass("violet")
				})
				$(this).removeClass("violet")
				 matieres.removeClass(pk_matiere+"-"+pk_professeur)
				 matieres.parent("td").removeClass("error-select-prof")
				 inputs=$("[value="+pk_matiere+"-"+pk_professeur+"]")
				pk_professeur=""
				matieres.addClass(+pk_matiere+"-"+pk_professeur)
				matieres.attr("matiere", pk_matiere+"-"+pk_professeur)
					matieres.parent("td.case").attr("matiere", pk_matiere+"-"+pk_professeur)
				inputs.each(function(){
						$(this).val(pk_matiere+"-"+pk_professeur)
				})
				noms_professeur=""
				matieres.find("ul li a").attr("professeur", pk_professeur)
				matieres.find("span.professeur").each(function(){
					$(this).html(noms_professeur)
				})
			}
		})
	})
}

var ajax=function(pk){
	if (pk===null){
		 pk=0
	}

	search=$("#search-nom-professeur").val()
var	request=$.ajax({
		url:"/direction/emploi_de_temps/edition/modification_professeur/"+pk+"/?search="+search,
		type:"GET",
		asynch:true,
		beforeSend:function(){
			$("div.professeurs").html("")
			$("div.professeurs").append("<div class='d-flex justify-content-center align-items-center'>\
			               <div class='spinner-border text-primary' ></div><span>chargement</span></div>")
		}


	})
	request.done(function(response){
		if (response.error){
			$("div.professeurs").html("<p class='text-danger'>"+response.error+"</p>")
			

		}
		else{
			var domaines=""
		 $.each(response.domaines, function(i, object){
			 domaines+=object.nom+", "
		 })
			$("h4 span.domaine").html(domaines)

			var professeurs=""
			var div_professeurs=$("div.professeurs")
			div_professeurs.html("")
			$.each(response.professeurs, function(i, object){
				div_professeurs.append("<div > <p  pk-professeur='"+object.pk+"' > <span class='fw-bold' style='cursor:pointer'>"+object.noms+" "+object.prenoms+",  </span>  <a href=# pk-professeur='"+object.pk+"'  class='link-primary' >détails</a></p></div>")
			})
			span_matiere=$("div.matiere p span")
			span_matiere.html(response.nom_matiere)
			span_matiere.attr("pk-matiere", response.pk_matiere)
			selectProfesseur()
			detailsProfesseur()
		}

	});
	request.fail(function(response){
	   var div_professeurs=$("div.professeurs")
		 div_professeurs.html("<p class='text-danger'>Erreur de chargement </p>")

	})
}

var enregistrementAjax=function(){
	var myForm=$("form")[0]
	inputs=$("form input")
	data=new FormData(myForm)
		//inputs.each(function(){
			//$(this).attr("name"):$(this).val(),
		//})




	var request1=$.ajax({
		url:$(location).attr("pathname"),
		type:"POST",
		processData:false,
		contentType:false,
		cache:false,
		data:data,
		asynch:true,
		beforeSend:function(){
			button=$("form button")
		 button.text("Enregistrement...")
		},


	})

	request1.done(function(response){
		button=$("form button")
			button.text("Enregistrer")
			button.show()

     var status=$(".status")

		 status.html("<span class='text-success fw-bold'>Enregistrement réussi </span>")
		setTimeout(()=>{
			status.html("<span>emploi de temps</span>")
		}, 2000)

})

	request1.fail(function(response){
		var status=$(".status")
		status.html("<span class='text-danger fw-bold'>Enregistrement échoué</span>")
	 setTimeout(()=>{
		 status.html("<span>emploi de temps</span>")
	 }, 2000)
	})
}
var detailsProfesseurAjax=function(pk_professeur){
 	var request2=$.ajax({
		url:"/direction/emploi_de_temps/edition/details_professeur/"+pk_professeur+"/",
		type:"GET",
		processData:false,
		contentType:false,
		cache:false,
		asynch:true,
		beforeSend: function(){
			var modalBody=$("#modalDetailsProfesseur  .modal-dialog .modal-content .modal-body")
			modalBody.html("")
		  modalBody.append("<div class=' fs-6 d-flex justify-content-center align-items-center'>\
			               <div class='spinner-border text-primary' ></div><span>chargement</span></div>")

		}



	})

 request2.done(function(response){
		
		var modalBody=$("#modalDetailsProfesseur  .modal-dialog .modal-content .modal-body")
		modalBody.html("")
		$.each(response.professeur, function(i, object){
			modalBody.append(" <p> <img src='"+object.photo+"' alt='"+object.noms+" "+object.prenoms+"'></p>\
			                     <p class='mt-1'>Matricule: <span class='fw-bold'>"+object.matricule+"</span> </p>\
			                                         <p class='mt-1'>Emploi de temps professeur: <a  href='/direction/emploi_de_temps/affichage/"+pk_professeur+"/' class='fw-bold link-dark' target='_blank' >cliquez ici</a> </p>\
													 <p class='mt-1'>Noms: <span class='fw-bold'>"+object.noms+"</span> </p>\
													 <p class='mt-1'>Prenoms: <span class='fw-bold'>"+object.prenoms+"</span> </p>\
													 <p class='mt-1'>Date de naissance: <span class='fw-bold'>"+object.date_naissance+"</span> </p>\
													 <p class='mt-1'>Lieu de naissance: <span class='fw-bold'>"+object.lieu_de_naissance+"</span> </p>\
													 <p class='mt-1'>Email: <span class='fw-bold'>"+object.email+"</span> </p>\
													 <p class='mt-1'>Numéro de téléphone: <span class='fw-bold'>"+object.numero_telephone+"</span> </p>\
													 <p class='mt-1'>Nationalité: <span class='fw-bold'>"+object.nationalite+"</span> </p>\
													 <p class='mt-1'>Numéro de CNI: <span class='fw-bold'>"+object.numero_CNI+"</span> </p>\
			")
		})
		modalBody.append("<p class='mt-1'>Nom du diplome: <span class='fw-bold'>"+response.cv.nom_diplomes+"</span> </p>\
		<p class='mt-1'>Année d'optension du diplome: <span class='fw-bold'>"+response.cv.annee_obtension_diplome+"</span> </p>\
		<p class='mt-1'>Ecole d'optension du diplome: <span class='fw-bold'>"+response.cv.ecole_obtension_diplome+"</span> </p>\
	")
	$.each(response.domaines, function(i, object){
		modalBody.append("<p class='mt-1'> Domaine "+(i+1)+": <span class='fw-bold'>"+object.nom+"</span> </p>")


	})


	})


	request2.fail(function(response){
 		var modalBody=$("#modalDetailsProfesseur  .modal-dialog .modal-content .modal-body")
		modalBody.html("")
		modalBody.append("<p class='text-danger'> Erreur lors de l'affichage des details </p>")

 	})
}

var detailsMatiereAjax=function(pk_matiere){
	var request3=$.ajax({
		url:"/direction/emploi_de_temps/edition/details_matiere/"+pk_matiere+"/",
		type:"GET",
		processData:false,
		contentType:false,
		cache:false,
		asynch:true,
		beforeSend: function(){
			var modalBody=$("#modalDetailsMatiere .modal-dialog .modal-content .modal-body")
			modalBody.html("")
		  modalBody.append("<div class=' fs-6 d-flex justify-content-center align-items-center'>\
			               <div class='spinner-border text-primary' ></div><span>chargement</span></div>")

		}
	})
	request3.done(function(response){
		
		var modalBody=$("#modalDetailsMatiere .modal-dialog .modal-content .modal-body")
		modalBody.html("")
		$.each(response.matiere, function(i, object){
			modalBody.append("<p class='mt-1'>Nom: <span class='fw-bold'>"+object.nom+"</span> </p>\
			 <p class='mt-1'>Credit: <span class='fw-bold'>"+object.credit+"</span> </p>\
			 <p class='mt-1'>Semestre: <span class='fw-bold'>"+object.semestre+"</span> </p>\
			  <p class='mt-1'>Programme: <span class='fw-bold'>"+object.programme+"</span> </p>")
		})
		modalBody.append("<p class='mt-1'>Nom de la specialité: <span class='fw-bold'>"+response.specialite.nom+"</span> </p>\
		<p class='mt-1'>Nom de la filière: <span class='fw-bold'>"+response.specialite.nom_filiere+"</span> </p>\
		<p class='mt-1'>Nom du cycle: <span class='fw-bold'>"+response.specialite.nom_cycle+"</span> </p>\
	")
	$.each(response.domaines, function(i, object){
		modalBody.append("<p class='mt-1'> Domaine "+(i+1)+": <span class='fw-bold'>"+object.nom+"</span> </p>")


	})
	})
	request3.fail(function(response){
		var modalBody=$("#modalDetailsMatiere  .modal-dialog .modal-content .modal-body")
		modalBody.html("")
		modalBody.append("<p class='text-danger'> Erreur lors de l'affichage des details </p>")
	})




}

var selectionProfesseurAjax=function(param, new_pk_professeur, matieres, inputs, noms_professeur, this_){
	var request=$.ajax({
		url:"/direction/emploi_de_temps/edition/selection_professeur/?p="+param+"&prof="+new_pk_professeur,
		type:"GET",
		processData:false,
		contentType:false,
		cache:false,
		asynch:true,
		beforeSend:function(){
			this_.append("<span id='spinner-professeur' style='width:20px; height:20px;' class='d-inline-block ml-2 spinner-border  spinner-border-sm text-primary'> </span>")
			

		},
	})

	request.done(function(response){
		$("#spinner-professeur").remove()

		error=false
		$.each(response, function(i, object){
			if (object.length!=0){
				error=true
			}
			})

		if (!error){
			matieres.removeClass(pk_matiere+"-"+pk_professeur)
			matieres.addClass(pk_matiere+"-"+new_pk_professeur)
					matieres.attr("matiere", pk_matiere+"-"+new_pk_professeur)
					matieres.parent("td.case").attr("matiere", pk_matiere+"-"+new_pk_professeur)
					inputs.each(function(){
							$(this).val(pk_matiere+"-"+new_pk_professeur)
					})

					matieres.find("ul li a").attr("professeur", new_pk_professeur)


					matieres.find("span.professeur").each(function(){
						$(this).html(noms_professeur)
					})
					pk_professeur=new_pk_professeur
		}


		else{
			classes=[]
			//$("#modalSelectionProfesseur").modal("show")
			$.each(response, function(i, object){
				$.each(object, function(i_1, object_1){
					classes.push(i+object_1)
				})
			})
			 var status=$(".status")
			 status.html("<span class='text-danger fw-bold'>Les professeur est déja occupé dans \
			 dans les périodes encadrées en rouge. Veillez le changer</span>")
		setTimeout(()=>{
			status.html("<span>emploi de temps</span>")
		}, 5000)
			classes.forEach(item=>{
				$("#"+item).addClass("error-select-prof")
			})
			

		}

		 } )
	
	request.fail(function(response){
		$("#spinner-professeur").remove()
		return false
	})
}


var selectionProfesseur1Ajax=function(param, pk_professeur, this_){
	var request=$.ajax({
		url:"/direction/emploi_de_temps/edition/selection_professeur1/?p="+param+"&prof="+pk_professeur,
		type:"GET",
		processData:false,
		contentType:false,
		cache:false,
		asynch:true,
		beforeSend:function(){
			this_.html("<div class='d-flex justify-content-center align-items-center\
				 '> <div class='spinner-grow spinner-grow-sm text-primary'></div></div>")
			

		},
	})
	request.done(function(response){
		
		this_.html("")
		if (response.error==false){
			this_.html($("."+matiere+":first").clone())
			petitMenuMatiere()
			prepareAjax()
			detailsMatiere()
			this_.attr("matiere", matiere)
		   id=this_.attr("id")
		    input=$("input#id_field_"+id+"[name='field_"+id+"']")
		    input.val(matiere)
		    this_.removeClass("error-select-prof")
		}
		else{
			this_.addClass("error-select-prof")
			 var status=$(".status")
			 status.html("<span class='text-danger fw-bold'>Le professeur est déja occupé dans \
			 dans la période encadrée en rouge. Veillez le changer</span>")
		setTimeout(()=>{
			status.html("<span>emploi de temps</span>")
		}, 5000)
		}
		
	})
	request.fail(function(response){
		this_.html("")
		var status=$(".status")
			 status.html("<span class='text-danger fw-bold'>Error </span>")
		setTimeout(()=>{
			status.html("<span>emploi de temps</span>")
		}, 5000)
		
		
	})

	
}