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
        name: 'Home'
        url: '#'
      }
      {
        name: 'Simple RSS'
        url: '#simplerss'
      }
      {
        name: 'Jellyfish'
        url: '#jellyfish'
      }
      ]

  MainMenuModel = new Backbone.Model main_menu_data
  
    
  
  class Controller extends Backbone.Marionette.Controller
    initialize_page: ->
      #console.log 'called controller.start()'
      layout = new Views.MainPageLayout
      layout.on 'show', =>
        view = new Views.MainPageView
          el: 'body'
        mainbar = new Views.MainBarView
          el: '#mainbar'
        MSGBUS.events.trigger 'mainbar:show', mainbar
        
        user = MSGBUS.reqres.request 'current:user'
        
        
        # FIXME
        show_login_form = false
        if ! user.has('username')
          view = new FDViews.LoginView
            el: '.right-column-content'
          show_login_form = true
          view.render()
          
      MSGBUS.events.trigger 'mainpage:show', layout

    make_main_content: ->
        $('#header').text 'Front Door'
        
    start: ->
      if document.getElementById 'main-content'
        @make_main_content()
      else
        @initialize_page()
        @make_main_content()
        
    mainbar_displayed: (view) ->
      window.fooview = view
      #console.log 'mainbar_displayed called'
      mainmenu = new Views.MenuView
        el: '#main-menu'
        model: MainMenuModel
      MSGBUS.events.trigger 'main-menu:show', mainmenu

      #console.log 'build user menu'
      user = MSGBUS.reqres.request 'current:user'
  
      usermenu = new Views.UserMenuView
        el: '#user-menu'
        model: user
      MSGBUS.events.trigger 'user-menu:show', usermenu
      
      

      
  MSGBUS.events.on 'mainbar:displayed', (view) ->
    controller = new Controller
    controller.mainbar_displayed view
    #console.log 'handle mainbar:displayed'
          

  module.exports = Controller
  
