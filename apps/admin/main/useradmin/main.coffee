#
# User Administration
# 
define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'

  Controller = require 'useradmin/controller'
  

  class Router extends Backbone.Marionette.AppRouter
    appRoutes:
      'useradmin': 'start'
      'useradmin/listusers': 'list_users'
      'useradmin/adduser': 'add_user'
      'useradmin/listgroups': 'list_groups'
      'useradmin/addgroup': 'add_group'
      
      

      
  MSGBUS.commands.setHandler 'useradmin:route', () ->
    console.log "useradmin:route being handled"
    controller = new Controller
    router = new Router
      controller: controller
      
