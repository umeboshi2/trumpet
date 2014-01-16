#
# Simple RSS app
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'simplerss/controller'
  #Models = require 'models'
  
  
  feeds = MSGBUS.reqres.request 'rss:feedlist'

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'simplerss': 'start'
      'simplerss/showfeed/:id': 'show_feed'
      'simplerss/addfeed': 'show_new_feed_form'
      
      
  MSGBUS.commands.setHandler 'simplerss:route', () ->
    console.log "simplerss:route being handled"
    window.feeds = feeds
    controller = new Controller
      feeds: feeds
    router = new Router
      controller: controller
    