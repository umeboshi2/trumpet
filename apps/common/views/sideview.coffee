define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    template = require 'templates/sideview'
    
    ########################################
    # Side View
    ########################################
    class SideView extends Backbone.View
        el: $ '.sidebar'
            
        initialize: (app) ->
            console.log('Init SideView')
            @current_view = null
            @router = app.router
            
        
        template: template
                        
        render: =>
            sidebar = $ '.sidebar'
            #@$el.html @template()
            sidebar.html @template()
            console.log(@$el)
            return @


        # pull_trigger is to activate views
        # when the route changes
        pull_trigger = trigger: true, replace: true
        listview = $ '.listview-list'
        events:
            'click .home-button': ->
                @router.navigate '', pull_trigger

            'click .users-button': ->
                listview.remove()
                @router.navigate 'dummy', pull_trigger
                @router.navigate 'view/user', pull_trigger

            'click .groups-button': ->
                listview.remove()
                @router.navigate 'dummy', pull_trigger
                @router.navigate 'view/group', pull_trigger
                
            
                                
    module.exports = SideView
    