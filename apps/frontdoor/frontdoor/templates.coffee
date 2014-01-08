# modular template loading
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
  img = teacup.img
  # Main Templates must use teacup.
  # The template must be a teacup.renderable, 
  # and accept a layout model as an argument.

  # Tagnames to be used in the template.
  {div, span, link, text, strong, label, input, 
  button, a, nav, form, p,
  ul, li, b,
  h1, h2, h3,
  subtitle, section
  } = teacup
            
    
  ########################################
  # Templates
  ########################################
  layout = renderable () ->
    div '.page', ->
      nav '#mainbar',\
      'data-spy':'affix', 'data-offset-top':'10', ->
        div '.navbar-header', ->
          # the id for the data-target came from a tutorial
          # and it should be renamed
          button '.navbar-toggle', type:'button', 'data-toggle':'collapse',\
          'data-target':'#ctx-menu-collapse-1', ->
            span '.sr-only', 'Toggle navigations'
            span 'badge', 'expand'
          a '.navbar-brand', href:"/", 'brand'
        div '#ctx-menu-collapse-1.collapse.navbar-collapse', ->
          div '#user-menu.navbar.navbar-nav.navbar-right'
          div '#main-menu.nav.navbar-nav.navbar-left'
      div '.main-content', ->
        div '#header'
        div '#subheader'
        div '#content', ->
          div '.two-col', ->
            div '.sidebar'
            div '.right-column-content'
        div '#footer'
    

  ##################################################################
  # ##########################
  ##################################################################    
  viewfeed = renderable (data) ->
    div '.listview-header', data.feed.name
    div '.listview-list', ->
      for entry in data.entries
        div '.listview-list-entry', ->
          p ->
            a '.rssviewer-viewfeed-entry-link',
            href:entry.link, entry.title
          div ->
            teacup.raw entry.summary
            
  layout = renderable () ->
    div '.something-very-special'
    
          
  module.exports =
    layout: layout
    
