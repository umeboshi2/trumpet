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
    create_template = renderable () ->
        _nameinput = '#nameinput.form-inline.form-control.pull-right'
        div '.create-form', ->
            div '#create-content.action-button', ->
                text 'Save'
            span '.form-inline', style:'white-space:nowrap', ->
                label '.form-inline', for: 'nameinput', ->
                    text 'Name'
                input  _nameinput, style: 'width:80%', name: 'name'
                                
                                        
                                        
                        
    #######################################################
    module.exports = create_template
    
