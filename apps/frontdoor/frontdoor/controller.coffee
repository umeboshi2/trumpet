define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'views/mainviews'

  FDViews = require 'frontdoor/views'
  
  main_menu_data =
    tagclass: 'main-menu'
    label: 'Main'
    entries: [
      {
        name: 'Simple RSS'
        url: '/apps/simplerss'
      }
      {
        name: 'Jellyfish'
        url: '/apps/jellyfish'
      }
      ]

  MainMenuModel = new Backbone.Model main_menu_data
  
    
  
  class Controller extends Backbone.Marionette.Controller
    start: ->
      console.log 'called controller.start()'
      layout = new Views.MainPageLayout
      layout.on 'show', =>
        view = new Views.MainPageView
          el: 'body'
        mainbar = new Views.MainBarView
          el: '#mainbar'
        mainbar.render()
        mainmenu = new Views.MenuView
          el: '#main-menu'
          model: MainMenuModel
        mainmenu.render()
        
        user = MSGBUS.reqres.request 'current:user'
        
        usermenu = new Views.UserMenuView
          el: '#user-menu'
          model: user
        usermenu.render()

        
        # FIXME
        show_login_form = false
        if ! user.has('username')
          view = new FDViews.LoginView
            el: '.right-column-content'
          show_login_form = true
          view.render()
          
      MSGBUS.events.trigger 'mainpage:show', layout
      
      #if ! user.has('username')
      #  view = new FDViews.LoginView
      #    el: '.right-column-content'
      #  MSGBUS.events.trigger 'rcontent:show', layout      

      

  module.exports = Controller
  
