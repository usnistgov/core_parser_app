// FIXME: update urls
var loadedModules = [];

var loadModuleResources = function(moduleURLList) {    
    var neededURLList = [];

    for(var modIndex=0; modIndex<moduleURLList.length; modIndex++) {
        var moduleURL = moduleURLList[modIndex];

        if(loadedModules.indexOf(moduleURL) === -1) {
            neededURLList.push(moduleURL);
        }
    }

    $.ajax({
        url: modulesResourcesUrl,
        type: "GET",
        dataType: "json",
        data: {
            'urlsToLoad': JSON.stringify(neededURLList),
            'urlsLoaded': JSON.stringify(loadedModules)
        },
        success: function(data){
            $('head').append(data.styles);
            $('body').append(data.scripts);

            for(var modIndex=0; modIndex<neededURLList.length; modIndex++) {
                loadedModules.push(neededURLList[modIndex]);
            }
        },
        error: function() {
            // Raise error
            console.error('An error occured when loading the modules');
        }
    });
};

var saveModuleData = function($module, modData, asyncOpt) {
    if(typeof asyncOpt === 'undefined') {
        asyncOpt = true;
    }

    //TODO: test if id always class element (could it be choice or sequence?)
    //var moduleId = $module.parents('.element').attr('id');
    var moduleId = $module.attr('id');
    var moduleURL = $module.find('.moduleURL').text();

    if(moduleURL === '') {
        console.error('moduleURL is not defined');
        return;
    }

    if ( modData instanceof FormData ) {
        modData.append("module_id", moduleId);
    } else {
        modData['module_id'] = moduleId;
    }

    var ajaxOptions = {
        url : '/' + moduleURL,
        type : "POST",
        dataType: "json",
        data: modData,
        async: false,
        success: function(data){
            if(!'html' in data) {
                console.error('No data sent back by the server');
                return;
            }

            var moduleDisplay = $(data.html).find('.moduleDisplay').html();
            var moduleResult = $(data.html).find('.moduleResult').html();

            $module.find('.moduleDisplay').html(moduleDisplay);
            $module.find('.moduleResult').html(moduleResult);     
            
            /* look at extra data received from the server */
            /*if ('xpath_accessor' in data){
            	xpath_accessor(data.xpath_accessor);
            }*/
        },
        error: function() {
            console.error("An error occurred when saving module data");
        }
    };

    if(modData instanceof FormData) {
        ajaxOptions.processData = false;
        ajaxOptions.contentType = false;
    }

    $.ajax(ajaxOptions);   
};

// Modules initialisation
var initModules = function() {
    var moduleList = $('.module');
    var moduleURLList = [];

    $.each(moduleList, function(index, value) {
        var moduleURL = $(value).find('.moduleURL').text();
        if(moduleURL !== "" && moduleURLList.indexOf(moduleURL) === -1) {
            moduleURLList.push(moduleURL);
        }
    });

    loadModuleResources(moduleURLList);
};
