define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'jellyfish/views'
  Collections = require 'jellyfish/collections'

  
  class Controller extends Backbone.Marionette.Controller
    make_sidebar: ->
      pages = MSGBUS.reqres.request 'wiki:pagelist'
      
      MSGBUS.events.trigger 'sidebar:close'
      view = new Views.PageListView
        collection: pages
      MSGBUS.events.trigger 'sidebar:show', view
      if pages.length == 0
        console.log 'fetching pages for sidebar'
        pages.fetch()
      
      
    set_header: (title) ->
      header = $ '#header'
      header.text title
      
    start: ->
      console.log 'jellyfish start'
      MSGBUS.events.trigger 'rcontent:close'
      MSGBUS.events.trigger 'sidebar:close'
      @set_header 'JellyFish'
      @make_sidebar()
      

      
              
  module.exports = Controller
  
