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
                    
                                        
    side_view_template = renderable () ->
        div '.main-content-manager-view.btn-group-vertical', ->
            div '.btn.btn-default.home-button', 'Main'
            div '.btn.btn-default.users-button', 'Users'
            div '.btn.btn-default.groups-button', 'Groups'
            div '.btn.btn-default.preferences-button', 'Preferences'
                        
    #######################################################
    module.exports = side_view_template
