define (require, exports, module) ->
  $ = require 'jquery'
  jQuery = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  bootstrap = require 'bootstrap'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  common_models = require 'common/models'

  require 'mainpage'
  
  require 'frontdoor/main'
  require 'useradmin/main'
  require 'jellyfish/main'
  

  prepare_app = (app) ->
    app.addRegions
      mainview: 'body'
      
      mainbar: '#mainbar'
      content: '#content'
      header: '#header'
      subheader: '#subheader'
      footer: '#footer'
      
      main_menu: '#main-menu'
      user_menu: '#user-menu'
      
      
      sidebar: '.sidebar'
      rcontent: '.right-column-content'
      
    app.on 'initialize:after', ->
      Backbone.history.start() unless Backbone.history.started
      
    app.msgbus = MSGBUS

    app.addInitializer ->
      # execute code to generate basic page
      # layout
      MSGBUS.commands.execute 'mainpage:init'

      # then setup the routes
      MSGBUS.commands.execute 'frontdoor:route'
      MSGBUS.commands.execute 'useradmin:route'
      MSGBUS.commands.execute 'simplerss:route'
      MSGBUS.commands.execute 'jellyfish:route'
      
      
    # connect events
    MSGBUS.events.on 'mainpage:show', (view) =>
      #console.log 'mainpage:show called'
      app.mainview.show view

    MSGBUS.events.on 'mainbar:show', (view) =>
      #console.log 'mainbar:show called'
      app.mainbar.show view
      MSGBUS.events.trigger 'mainbar:displayed', view
      
    MSGBUS.events.on 'main-menu:show', (view) =>
      #console.log 'main-menu:show called'
      app.main_menu.show view
      
    MSGBUS.events.on 'user-menu:show', (view) =>
      #console.log 'user-menu:show called'
      app.user_menu.show view


    MSGBUS.events.on 'sidebar:show', (view) =>
      console.log 'sidebar:show called'
      app.sidebar.show view

    MSGBUS.events.on 'sidebar:close', () =>
      console.log 'sidebar:close called'
      app.sidebar.close()

      
    MSGBUS.events.on 'rcontent:show', (view) =>
      console.log 'rcontent:show called'
      app.rcontent.show view
      
    MSGBUS.events.on 'rcontent:close', () =>
      app.rcontent.close()
      
            
      
  app = new Marionette.Application()
  app.current_user = new common_models.CurrentUser
  response = app.current_user.fetch()

  MSGBUS.reqres.setHandler 'current:user', ->
    app.current_user
    
  # we prepare the app after we fetch
  # the current user, then we assign
  # app.ready to true (I should use msgbus
  # for this).
  app.ready = false

  response.done ->
    prepare_app app
    app.ready = true
    
    
                        
  module.exports = app
  
    
