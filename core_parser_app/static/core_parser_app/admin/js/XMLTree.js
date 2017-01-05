//Expand/Collapse elements from the XML tree on Curate page
showhideCurate = function(event){
	button = event.target
	parent = $(event.target).parent();
	$(parent.children("ul")).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
};