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
  rss_feed_entry = renderable (feed) ->
    div '.listview-list-entry', ->
      a href:'#showfeed/' + feed.id, feed.name

  rss_feed_entry_empty = renderable (feed) ->
    div '.listview-list-entry', ->
      text 'EmptyView'

  rss_feed_list = renderable (header) ->
    div '.listview-header', "RSS Feeds"
    div '.rss-feedlist.listview-list'

  sidebar = renderable () ->
    div '.listview-header', ->
      div ->
        a href:'#', 'RSS List'
        
  sbutton = renderable (model) ->
    btnclass = '.btn.btn-default.' + model.bclass
    div btnclass, ->
      text model.name

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
            
  ##################################################################
  # ##########################
  ##################################################################    
          
  module.exports =
    rss_feed_entry: rss_feed_entry
    rss_feed_list: rss_feed_list
    sidebar: sidebar
    viewfeed: viewfeed
    
    
