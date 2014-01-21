define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  ########################################
  # Models
  ########################################

  class RssFeed extends Backbone.Model
    defaults:
      name: 'No RSS'
      url: '#'
    url: '/rest/simplerss/feeds'
    
      
  make_rss_data_model = (rss_id) ->
    class RssData extends Backbone.Model
      url: '/rest/simplerss/feeds/' + rss_id + '/feeddata'
    return new RssData(rss_id)
    
      
  module.exports =
    RssFeed: RssFeed
    make_rss_data_model: make_rss_data_model
