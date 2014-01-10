define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  SiteTemplates = require 'common/templates/site'
  
  class MainPageLayout extends Backbone.Marionette.Layout
    el: 'body'
    template: SiteTemplates.PageLayoutTemplate

  module.exports =
    Layout: MainPageLayout
    

    
