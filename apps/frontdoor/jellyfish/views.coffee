define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'jellyfish/templates'

  class JellyfishView extends Backbone.Marionette.ItemView

  class PageListEntryView extends Backbone.Marionette.ItemView
    template: Templates.page_list_entry
    
  class PageListView extends Backbone.Marionette.CollectionView
    template: Templates.page_list
    itemView: PageListEntryView
    
      
      
  module.exports =
    JellyfishView: JellyfishView
    PageListView: PageListView
    