define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'
  Views = require 'views/mainviews'

  FDViews = require 'frontdoor/views'

  FDController = require 'frontdoor/controller'
  
  
  main_menu_data =
    tagclass: 'main-menu'
    label: 'Main'
    entries: [
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
    make_main_content: ->
        $('#header').text 'simplerss'
              
    start: ->
      if document.getElementById('main-content')
        @make_main_content()
      else
        c = new FDController
        c.initialize_page()
        @make_main_content()
        
  module.exports = Controller
  
