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
    list_titles =
        user: 'Users'
        group: 'Groups'
        
    listview_template = renderable (data) ->
        nbtn = '#new-entry-button.pull-right.btn.btn-default.btn-xs.add-entry-btn'
        div '.listview-header', ->
            text list_titles[data.type]
            div nbtn, ->
                icon '.fa.fa-plus-square'
        div '.listview-list'
                
                    
                                        
                        
    #######################################################
    module.exports = listview_template
    
