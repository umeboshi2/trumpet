define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    listview_template = require 'templates/listview'
    create_template = require 'templates/create'
    entry_templates = require 'templates/entry'
    
    {UserList, GroupList} = require 'collections'
        
    class BaseMainContentView extends Backbone.View
        el: $ '.right-column-content'
                                        
        remove: () ->
            @undelegateEvents()
            @$el.empty()
            @stopListening()
            return @


    class BaseModelView extends Backbone.View
        template: entry_templates.entry
        
        initialize: ->
            _.bindAll @, 'render'
            @model.bind 'change', @render
            @model.bind 'remove', @unrender

        render: ->
            # FIXME This is a HACK
            # we are using one entry template
            # for both models.  The User db
            # object should really have a 'name'
            # attribute, rather than 'username',
            # but that will be done later.  For
            # now, there needs to be work done
            # on using abstract backbone 'classes'
            # upon different model types.
            if @model.has 'username'
                tmpl = entry_templates.user_entry
            else
                tmpl = entry_templates.entry
    
            #@model.set 'name', @model.get 'username'
            html = tmpl @model.attributes
            #html = @template.render @model.attributes
            this.$el.html html
            return @

        unrender: ->
            $(@el).remove()

        events:
            'click .show-entry-btn': 'showentry'

        showentry: ->
            el = $('.listview-list')
            if @model.get('objtype') == 'user'
                view = new MainUserView main_model: @model
            else
                view = new MainGroupView main_model: @model
            html = view.render @model.attributes
            el.html html
                        
        
        
    ########################################
    # List Views
    ########################################
    class BaseListView extends BaseMainContentView
        render: (data) ->
            tmpl = listview_template
            @$el.html tmpl data
            return @

        modelView: BaseModelView

                
        appendItem: (model) =>
            view = new @modelView model: model
            html = view.render(model).el
            $('.listview-list').append html

        events:
            'click .add-entry-btn': 'new_entry_view'

        new_entry_view: ->
            mclass = @collection.model
            model = new mclass()
            tmpl = create_template
            html = tmpl model.attributes
            $('.listview-list').html html
                        
    class UserListView extends BaseListView
        initialize: ->
            console.log('Init UserListView')
            @collection = new UserList
            @collection.bind 'add', @appendItem
            @collection.fetch()

        appendItem: (model) =>
            view = new @modelView model: model
            # FIXME
            window.mbview = view
            html = view.render(model).el
            $('.listview-list').append html

    class GroupListView extends BaseListView
        initialize: ->
            console.log('Init GroupListView')
            @collection = new GroupList
            @collection.bind 'add', @appendItem
            @collection.fetch()

                
            
                                
    module.exports =
        user: UserListView
        group: GroupListView
        
    