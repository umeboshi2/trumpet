$(document).ready ->
        $('.delete-confirm').hide()
        main_id = $('#main_id').val()
        ctype = $('#ctype').val()

        destroy_entry = (data, status, xhr) ->
                f = $.parseJSON(data)
                entry_id = 'entry-' + f.ctype + '-' + f.id
                if f.update == 'deleted'
                        $('#'+ entry_id).empty()
                        $('#'+ entry_id).remove()
                else
                        $('#'+ entry_id).empty()
                        msg = "There are pages using this resource."
                        $('#'+ entry_id).text(msg)

        delete_resource = (ctype, id) ->
                entry_id = 'entry-' + ctype + '-' + id
                #$('#'+ entry_id).hide()
                formdata =
                        update: 'delete'
                        ctype: ctype
                        id: id
                $.post(window.location, formdata, destroy_entry)
                
                
                

        $('.delete-button').click ->
                $(this).hide()
                btnid = $(this).attr('id').split('-')[2]
                div_id = 'div-confirm-' + ctype + '-' + btnid
                $('#'+ div_id).show()
                #$(this).children('.delete-confirm').show()
                #$('$this > .delete-confirm').show()

                       
        $('.cancel-button').click ->
                btnid = $(this).attr('id').split('-')[2]
                div_id = 'div-confirm-' + ctype + '-' + btnid
                $('#'+ div_id).hide()
                del_id = 'delete-' + ctype + '-' + btnid
                $('#'+ del_id).show()
                
                
        $('.confirm-button').click ->
                btnid = $(this).attr('id').split('-')[2]
                #div_id = 'div-confirm-' + ctype + '-' + btnid
                #$('#'+ div_id).hide()
                #del_id = 'delete-' + ctype + '-' + btnid
                #$('#'+ del_id).show()
                delete_resource(ctype, btnid)
                
        $('#save-content').click ->
                #$('#editor').toggle()
                $('header > h2').text(window.location)
                formdata =
                        update: "submit"
                        content: editor.getValue()
                post_to_url(window.location, formdata, 'post')
                $('header > h2').text("Posted")
                
