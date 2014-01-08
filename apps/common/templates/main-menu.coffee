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
    main_menu = renderable (user) ->
        ul '.ctx-menu.nav.navbar-nav', ->
            li '.dropdown', ->
                a '.dropdown-toggle', 'data-toggle':'dropdown', ->
                    text "Main"
                    b '.caret'
                ul '.dropdown-menu', ->
                    li ->
                        a href:'/apps/simplerss', 'Simple RSS'
                    li ->
                        a href:'/apps/users2', 'Manage Users'
                    li ->
                        a href:'/apps/jellyfish', 'jellyfish'
            
    module.exports = main_menu
    
    