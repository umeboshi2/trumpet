define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'views/templates'

  FDTemplates = require 'frontdoor/templates'
  
  class FrontDoorMainView extends Backbone.Marionette.ItemView
    template: FDTemplates.frontdoor_main
  
  module.exports =
    FrontDoorMainView: FrontDoorMainView
    