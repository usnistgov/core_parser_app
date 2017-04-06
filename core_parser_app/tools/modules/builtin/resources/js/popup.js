var openModule = null;
var openPopUp = null;
var popUpOptions = [];

closePopUp = function() {
    openPopUp.removeClass('active_dialog');
    openPopUp.dialog("destroy");

    openModule = null;
    openPopUp = null;
};

var defaultPopUpOptions = {
    modal: true,
    buttons: {
        Cancel: closePopUp
    },
    close: function(event, ui) {
        closePopUp();
    }
};

configurePopUp = function(moduleURL, options, getDataFunction) {
    var modulePopUpOptions = $.extend({}, defaultPopUpOptions, options);

    var saveButton = {
        Save: function() {
            data = getDataFunction();            
            saveModuleData(openModule, data);
            
            closePopUp();
        }
    };
    modulePopUpOptions["buttons"] = $.extend({}, saveButton, modulePopUpOptions["buttons"]);

    popUpOptions[moduleURL] = modulePopUpOptions;
};

$('body').on('click', '.mod_popup .open-popup', function(event) {
    event.preventDefault();
    openModule = $(this).parent().parent().parent();

    openModule.find('.mod_dialog').addClass('active_dialog');

    openPopUp = $('.active_dialog');
    openPopUp.dialog(popUpOptions[openModule.find('.moduleURL').text()]);
});