var blobHostPopupOptions = {
    title: "Upload File",
}

var saveBlobHostData = function() {
    return new FormData(openPopUp.find('.blob-host-form')[0]);
};

// FIXME: update url?
configurePopUp('/core/blob-host', blobHostPopupOptions, saveBlobHostData);