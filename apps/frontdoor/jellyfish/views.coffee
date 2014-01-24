define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'jellyfish/templates'

  class JellyfishView extends Backbone.Marionette.ItemView
    
      
      
  module.exports =
    JellyfishView: JellyfishView
