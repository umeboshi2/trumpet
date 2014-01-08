define (require, exports, module) ->
    $ = require 'jquery'
    jQuery = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    bootstrap = require 'bootstrap'

    templates = require 'views/templates'
    main_menu = require 'frontdoor/templates/main-menu'
    PageLayoutTemplate = require 'frontdoor/templates/site'
    
    SideView = require 'views/sideview'

    Router = require 'router'
    
    class CurrentUser extends Backbone.Model
        url: '/rest/current/user'

    class CurrentPage extends Backbone.Model
        url: '/rest/webviews/default'
        
    
    class ApplicationView extends Backbone.View
        el: $ 'body'
    
        initialize: () ->
            @current_user = new CurrentUser()
            response = @current_user.fetch()
            response.done =>
                @render()

        template: PageLayoutTemplate
        
        render: ->
            @$el.html PageLayoutTemplate @current_user
            @side_view = new SideView @
            @side_view.render()
            $('.header').text "User Admin"
            $('#main-menu').html main_menu()
            
            
    module.exports = ApplicationView
    
    
