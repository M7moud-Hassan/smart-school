(function () {
    'use strict'

    /* dropzone */
    let myDropzone = new Dropzone(".dropzone");
        myDropzone.on("addedfile", file => {
    });

    /* filepond */
    FilePond.registerPlugin(
        FilePondPluginImagePreview,
        FilePondPluginImageExifOrientation,
        FilePondPluginFileValidateSize,
        FilePondPluginFileEncode,
        FilePondPluginImageEdit,
        FilePondPluginFileValidateType,
        FilePondPluginImageCrop,
        FilePondPluginImageResize,
        FilePondPluginImageTransform
    );

    /* multiple upload */
    
    
    /* single upload */
    

})();