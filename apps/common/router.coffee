define (require, exports, module) ->
    $ = require 'jquery'
    jQuery = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    bootstrap = require 'bootstrap'
    list_views = require 'views/listviews'
        
    class Router extends Backbone.Router
        initialize: (app) ->
            app.router = @
            @app = app
             
        routes:
            '': 'home'
            'view/:listview': 'listview'

        common: ->
            if @app.side_view != undefined
                @app.side_view.render()
                if @app.side_view.current_view != null
                    @app.side_view.current_view.remove()


        home: ->
            @common()

        listview: (lview) ->
            console.log 'Router.listview'
            @common()
            klass = list_views[lview]
            el = $ '.right-column-content'
            view = new klass el:el
            view.render type: lview
            @app.side_view.current_view = view
            $('body').prepend 'hello'
    module.exports = Router
    
    
