define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    teacup = require 'teacup'

    renderable = teacup.renderable

    div = teacup.div
    # I use "icon" for font-awesome
    icon = teacup.i
    strong = teacup.strong
    span = teacup.span
    label = teacup.label
    input = teacup.input

    text = teacup.text

    # Main Templates must use teacup.
    # The template must be a teacup.renderable, 
    # and accept a layout model as an argument.

    # Tagnames to be used in the template.
    {div, span, link, text, strong, label, input, 
    button, a, nav, form,
    ul, li, b} = teacup
            
    
    ########################################
    # Templates
    ########################################
    _btnclass = '.btn.btn-default.btn-xs.pull-right.show-entry-btn'
        
    entry_template = renderable (atts) ->
        div '.listview-list-entry', ->
            text atts.name
            div _btnclass, ->
                icon '.fa.fa-folder-open'
                                
    user_entry_template = renderable (atts) ->
        div '.listview-list-entry', ->
            text atts.username
            div _btnclass, ->
                icon '.fa.fa-folder-open'

                
                
                    
                                        
                        
    #######################################################
    module.exports =
        entry: entry_template
        user_entry: user_entry_template
        
