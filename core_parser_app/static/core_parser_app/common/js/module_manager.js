/**
 * Insert a module in the XML tree
 * @param event
 */
var insertModule = function(event){
	// change the sequence style
	parent = $(target).parent();

	insertButton = event.target;
	moduleURL = $(insertButton).parent().siblings(':first').attr('data-module-url-value')
	moduleID = $(insertButton).parent().siblings(':first').attr('data-id');
    templateID = $("#templateid").html();

	xpath = getXPath();

	$( "#dialog-modules" ).dialog("close");

	insert_module(moduleID, templateID, xpath, parent);
};


/**
 * AJAX call, inserts a module
 */
var insert_module = function(moduleID, templateID, xpath, parent){
    $("#add-module-modal").modal("hide");
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
};


/**
 * Remove a module
 * @param event
 */
var deleteModule = function(event){
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
var delete_module = function(xpath, templateID, parent){
    $("#add-module-modal").modal("hide");
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
	$("#add-module-modal").modal("show");
};		

/**
 * Hides modules for generation of automatic keys
 */
var hideAutoKeys = function(){
    $("#modules-table").find("tr:not(:first)").each(function(){
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
	$("#add-module-modal").modal("show");
};

/**
 * Shows only modules for generation of automatic keys
 */
var showAutoKeys = function(){
    $("#modules-table").find("tr:not(:first)").each(function(){
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
var getXPath = function(){
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


$(document).on('click', '.insert', insertModule);
$(document).on('click', '.delete', deleteModule);
