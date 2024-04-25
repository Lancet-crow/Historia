$(function() {
    var editor = new FroalaEditor('#edit', {
        placeholderText: 'Напишите что-нибудь...',
        imageUploadURL: '/upload_image',
        imageManagerLoadURL: '/load_images',
        imageManagerDeleteURL: '/delete_image',
        imageUploadParams: {id: 'edit'},
        useClasses: false,
        htmlRemoveTags: ['script', 'base'],
    })
    /*$(document).ready(function(){
        editor.events['image.removed'] = function (e, editor, $img) {
            // Set the image source to the image delete params.
            editor.options.imageDeleteParams = {src: $img.attr('src')};
            console.log("SOME SORT OF SH");
            // Make the delete request.
            editor.deleteImage($img);
        }
    });*/
});