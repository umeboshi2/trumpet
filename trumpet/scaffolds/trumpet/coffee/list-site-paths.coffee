$(document).ready ->
        $('.delete-confirm').hide()
        $('.delete-button').click ->
                btnid = $(this).attr['id']
                $('header > h2').text(btnid)

        $('#save-content').click ->
                #$('#editor').toggle()
                $('header > h2').text(window.location)
                formdata =
                        update: "submit"
                        content: editor.getValue()
                post_to_url(window.location, formdata, 'post')
                $('header > h2').text("Posted")
                
