$(document).ready ->
        # prepare page
        $('#save-content').hide()
        # setup vars and functions
        ctype = $('#ctype').val()
        fresh_edit = (data, status, xhr) ->
                $('#save-content').hide()
        # init editor
        editor = ace.edit('editor')
        editor.getSession().on('change', () ->
                $('#save-content').show()
                )
        # set editor mode
        if ctype == 'css'
                editor.getSession().setMode('ace/mode/css')
        if ctype == 'js'
                editor.getSession().setMode('ace/mode/javascript')
        # set editor theme
        editor.setTheme('ace/theme/twilight')

        # click save button
        $('#save-content').click ->
                formdata =
                        update: 'submit'
                        content: editor.getValue()
                $(this).hide()
                $.post(window.location, formdata, fresh_edit)
                        
