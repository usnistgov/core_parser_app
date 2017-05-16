var advancedBlobHostPopupOptions = {
    title: "Select a file",
}

var saveAdvancedBlobHostData = function() {
    return new FormData(openPopUp.find('.advanced-blob-host-form')[0]);
};

// FIXME: update url?
configurePopUp('/core/advanced-blob-host', advancedBlobHostPopupOptions, saveAdvancedBlobHostData);