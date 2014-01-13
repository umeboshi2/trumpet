#
# Simple RSS app
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'simplerss/controller'
  Collections = require 'collections'
  #Models = require 'models'
  
  
  feeds = MSGBUS.reqres.request 'rss:feedlist'

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'simplerss': 'start'

      
  MSGBUS.commands.setHandler 'simplerss:route', () ->
    console.log "simplerss:route being handled"
    controller = new Controller
      feeds: feeds
    router = new Router
      controller: controller
    