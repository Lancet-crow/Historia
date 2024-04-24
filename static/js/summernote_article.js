 $('#summernote').summernote({
        tabsize: 2,
        width: 1300,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript', 'clear']],
            ['fontsize', ['fontsize']],
            ['forecolor', ['forecolor']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'hr']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']],
        ],
      });

var edit = function() {
    $('.click2edit').summernote({focus: true});
};

var save = function() {
  var markup = $('.click2edit').summernote('code');
  $('.click2edit').summernote('destroy');
};

$(document).ready(function() {
    $('#summernote').summernote({
        height: 200,
        callbacks: {
            onImageUpload: function(files, editor, welEditable) {
                for(var i = files.length - 1; i >= 0; i--) {
                    sendFile(files[i], editor, welEditable);
                }
            }
        }
    });

    function sendFile(file, editor, welEditable) {
        data = new FormData();
        data.append("file", file);
        $.ajax({
            data: data,
            type: "POST",
            url: "../editor-upload.php",
            cache: false,
            contentType: false,
            processData: false,
            success: function(url) {
                editor.insertImage(welEditable, url);
            }
        });
    }
    });