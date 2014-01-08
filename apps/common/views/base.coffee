define (require, exports, module) ->
    $ = require 'jquery'
    jQuery = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    templates = require 'templates/entry'
    listview_template = require 'templates/listview'
    create_template = require 'templates/create'
            
    ########################################
    # Views
    ########################################
    class BaseModelView extends Backbone.View
        template: templates.entry
        
        initialize: ->
            _.bindAll @, 'render'
            @model.bind 'change', @render
            @model.bind 'remove', @unrender

        render: ->
            html = @template @model.attributes
            this.$el.html html
            return @

        unrender: ->
            $(@el).remove()

        
    class BaseMainContentView extends Backbone.View
        el: $ '.right-column-content'
                                        
        remove: () ->
            @undelegateEvents()
            @$el.empty()
            @stopListening()
            return @

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

    module.exports =
        BaseModelView: BaseModelView
        BaseMainContentView: BaseMainContentView
        BaseListView: BaseListView
        