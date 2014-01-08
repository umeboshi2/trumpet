define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    templates = require 'views/templates'
    
    ########################################
    # Preferences View
    ########################################
    class PreferencesView extends Backbone.View
        el: $ '.right-column-content'
            
        initialize: (app) ->
            console.log('Init PreferencesView')
            @current_view = null
            @router = app.router
            
        
        template:
            templates.side_view
                        
        render: =>
            container = $ '.right-column-content'
            #@$el.html @template()
            container.html @template()
            console.log(@$el)
            return @


        # pull_trigger is to activate views
        # when the route changes
        pull_trigger = trigger: true, replace: true
        events:
            'click .home-button': ->
                @router.navigate '', pull_trigger
                                
    module.exports = PreferencesView
    
    
