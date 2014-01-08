define (require, exports, module) ->
    $ = require 'jquery'
    
    template = require 'common/templates/site'
    main_menu = require 'common/templates/main-menu'
    


    render_page = (user, pagemodel) ->
        body = $ 'body'
        body.html template.PageLayoutTemplate user
        $('#main-menu').html main_menu()
        header = $ '#header'
        header.text(pagemodel.header ? 'header')
            
            
    module.exports =
        render: render_page
        
    
