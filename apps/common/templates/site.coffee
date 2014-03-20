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
  user_menu = renderable (user) ->
    name = user.username
    ul '#user-menu.ctx-menu.nav.navbar-nav', ->
      li '.dropdown', ->
        a '.dropdown-toggle', 'data-toggle':'dropdown', ->
          if name == undefined
            text "Guest"
          else
            text name
          b '.caret'
        ul '.dropdown-menu', ->
          if name == undefined
            li ->
              a href:'/login', 'login'
          else
            li ->
              a href:'/app/user', 'User Page'
            # we need a "get user info" from server
            # to populate this menu with 'admin' link
            admin = false
            unless name == undefined
              groups = user.groups
              if groups != undefined
                for g in groups
                  if g.name == 'admin'
                    admin = true
            if admin
              li ->
                a href:'/admin', 'Administer Site'
            li ->
              a href:'/logout', 'Logout'

  ########################################
  main_bar = renderable () ->
    div '.navbar-header', ->
      button '.navbar-toggle', type:'button', 'data-toggle':'collapse',
      'data-target':'#mainbar-collapse', ->
        span '.sr-only', 'Toggle navigations'
        span 'badge', 'expand'
    div '#mainbar-collapse.collapse.navbar-collapse', ->
      div '#main-menu.nav.navbar-nav.navbar-left.main-menu'
      div '#user-menu.navbar.navbar-nav.navbar-right.main-menu'

  ########################################
  PageLayoutTemplate = renderable (user) ->
    div '.page', ->
      nav '#mainbar', 'data-spy':'affix', 'data-offset-top':'10'
      div '#main-content', ->
        div '#header'
        div '#subheader'
        div '#content', ->
          div '.two-col', ->
            div '.sidebar'
            div '.right-column-content'
        div '#footer'
            
  module.exports =
    PageLayoutTemplate: PageLayoutTemplate
    main_bar: main_bar
    user_menu: user_menu
    
      
