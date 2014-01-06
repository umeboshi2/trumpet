$(document).ready ->
        $('.betgame-window').hide()

        $('#attach-css-button').click ->
                url = $(this).attr('href')
                window.location = url
                $(this).hide()

        $('#attach-js-button').click ->
                url = $(this).attr('href')
                window.location = url
                $(this).hide()

        $('.detach-button').click ->
                btnid = $(this).attr('id')
                url = $(this).attr('href')
                elist = btnid.split('-')
                ctype = elist[1]
                #path_id = new Number(elist[2])
                #obj_id = new Number(elist[3])
                detach_id = elist[2] + '-' + elist[3]
                $('header > h2').text(ctype + '-' + detach_id)
                window.location = url