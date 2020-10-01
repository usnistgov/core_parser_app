/**
 * Popup module script
 */
let moduleElement = null;
let moduleOptions = [];

let configurePopUp = (key, popupOptions)=>{
    moduleOptions[key] = popupOptions;
}

/**
 * Open modal button listener
 */
$('body').on('click', '.mod_popup .open-popup', function(event) {
    event.preventDefault();
    moduleElement = $(this).parent().parent().parent();
    popupOption = moduleOptions[moduleElement.find('.moduleURL').text()];
    let jqBootstrapModalId = $("#modal-" + moduleElement[0].id);

    let modDialogElement = moduleElement.find('.mod_dialog')
    modDialogElement.addClass('active_dialog');

    // the new bootstrap modal have an id as follow : id-<module-id>
    if(jqBootstrapModalId.length > 0){
        const getFormDataFunction = popupOption.getData;
        jqBootstrapModalId.modal("show"); // show the modal
        $(".save-module-form").unbind(); // unbind the previous listeners

        // listen the click event on the save button
        $(".save-module-form").on("click", ()=>{
            let data = getFormDataFunction();
            saveModuleData(moduleElement, data);
            jqBootstrapModalId.modal('hide');
        });
        // listen the hide event on the modal
        jqBootstrapModalId.unbind('hidden.bs.modal');
        jqBootstrapModalId.on('hidden.bs.modal', function (e) {
            moduleElement = null;
        })
    }
});