define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  FDViews = require 'frontdoor/views'
  
  
  class Controller extends Backbone.Marionette.Controller
    make_main_content: ->
      MSGBUS.events.trigger 'sidebar:close'
      user = MSGBUS.reqres.request 'current:user'
      $('#header').text user.get 'name'
      view = new FDViews.FrontDoorMainView
      MSGBUS.events.trigger 'rcontent:show', view
          
          
    start: ->
      @make_main_content()
        

  module.exports = Controller
  
