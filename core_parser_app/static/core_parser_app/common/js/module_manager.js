/**
 * Load controllers for module management
 */
$(document).ready(function() {
    $('.insert').on('click', insertModule);
    $('.delete').on('click', deleteModule);
});

/**
 * Insert a module in the XML tree
 * @param event
 */
insertModule = function(event){
	// change the sequence style
	parent = $(target).parent();

	insertButton = event.target;
	moduleURL = $(insertButton).parent().siblings(':nth-of-type(2)').text();
	moduleID = $(insertButton).parent().siblings(':first').attr('moduleID');
    templateID = $("#templateid").html();

	xpath = getXPath();

	$( "#dialog-modules" ).dialog("close");

	insert_module(moduleID, templateID, xpath, parent);
};


/**
 * AJAX call, inserts a module
 */
insert_module = function(moduleID, templateID, xpath, parent){
    $.ajax({
        url : templateModuleInsertUrl,
        type : "POST",
        dataType: "json",
        data:{
        	moduleID: moduleID,
        	templateID: templateID,
        	xpath: xpath
        },
        success: function(data){
            // add the module attribute
            if ($(parent).parent().find('.module').length == 1 ){
                $(parent).parent().find(".module").html(moduleURL);
            }else{
                $(parent).after("<span class='module'>"+
                                moduleURL +
                                "</span>");
            }
        }
    });
}


/**
 * Remove a module
 * @param event
 */
deleteModule = function(event){
	parent = $(target).parent();

	insertButton = event.target;

	xpath = getXPath();
	templateID = $("#templateid").html();

	$( "#dialog-modules" ).dialog("close");

	delete_module(xpath, templateID, parent);
};


/**
 * AJAX call, deletes a module
 */
delete_module = function(xpath, templateID, parent){
    $.ajax({
        url : templateModuleDeleteUrl,
        type : "POST",
        dataType: "json",
        data:{
        	xpath: xpath,
        	templateID: templateID
        },
        success: function(data){
            // remove the module from the HTML
	        $(parent).parent().find('.module').remove()
        }
    });
};


var target;

/**
 * Opens dialog with available modules
 */
var showModuleManager = function(event){
	target = event.target;
	hideAutoKeys();
	$( "#dialog-modules" ).dialog({
      modal: true,
      width: 600,
      height: 400,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
};		

/**
 * Hides modules for generation of automatic keys
 */
hideAutoKeys = function(){
    $("#dialog-modules").find("table").find("tr:not(:first)").each(function(){
      $(this).show();
      if ($($(this).children("td")[1]).html().indexOf('auto-key') > 0){
        $(this).hide();
      }
    });
};

/**
 * Opens dialog with available auto keys modules
 */
var showAutoKeyManager=function(event){
	target = event.target;
	showAutoKeys();
	$( "#dialog-modules" ).dialog({
      modal: true,
      width: 600,
      height: 400,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
};

/**
 * Shows only modules for generation of automatic keys
 */
showAutoKeys = function(){
    $("#dialog-modules").find("table").find("tr:not(:first)").each(function(){
      $(this).show();
      if ($($(this).children("td")[1]).html().indexOf('auto-key') < 0){
        $(this).hide();
      }
    });
};


/**
 * Build xpath of selected element
 * @returns
 */
getXPath = function(){
	current = $(target).parent().siblings('.path');
	xpath = $(current).text();	
	current = $(current).parent().parent().parent().siblings('.path');
	while(current != null){
		current_path = $(current).text() ;
		if (current_path.indexOf("schema") != -1){
			current = null;
		}else{			
			xpath = current_path + "/" + xpath;	
			current = $(current).parent().parent().parent().siblings('.path');
		}		
	}
	return xpath;
};


/**
 * Get the namespace with the correct index
 */
manageXPath = function(){	
	namespace = $(target).text().split(":")[0];
	i = 1;
	$(target).closest("ul").children().each(function(){
	  if(!($(this).find(".path").html() == $(target).closest("li").find(".path").html() )){
		  $(this).find(".path").html(namespace + ":element["+i+"]");
		  i += 1;
	  }	  
	})
};
