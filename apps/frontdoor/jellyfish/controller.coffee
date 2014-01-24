define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'jellyfish/views'
  Collections = require 'collections'

  
  class Controller extends Backbone.Marionette.Controller
    make_sidebar: ->
      MSGBUS.events.trigger 'sidebar:close'
      view = new Views.FeedListView
        collection: feeds
      MSGBUS.events.trigger 'sidebar:show', view
      if feeds.length == 0
        console.log 'fetching feeds for sidebar'
        feeds.fetch()
      
      
    make_main_content: ->
      MSGBUS.events.trigger 'rcontent:close'
      @set_header 'JellyFish'
      @make_sidebar()
      
    start: ->
      console.log 'jellyfish start'
      MSGBUS.events.trigger 'rcontent:close'
      MSGBUS.events.trigger 'sidebar:close'
      @set_header 'JellyFish'
      

    set_header: (title) ->
      header = $ '#header'
      header.text title
      
              
  module.exports = Controller
  
