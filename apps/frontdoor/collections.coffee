define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  
  { User, Group, RssFeed,
  make_rss_data_model } = require 'models'
  MSGBUS = require 'msgbus'
      

  ########################################
  # Collections
  ########################################
  class BaseCollection extends Backbone.Collection
    # wrap the parsing to retrieve the
    # 'data' attribute from the json response
    parse: (response) ->
      return response.data

  class RssFeedList extends BaseCollection
    model: RssFeed
    url: '/rest/simplerss/feeds'

  # set handlers on message bus
  # 
  MSGBUS.reqres.setHandler 'rss:feedlist', ->
    new RssFeedList

  MSGBUS.reqres.setHandler 'rss:feeddata', (feed_id) ->
    console.log 'handle rss:feeddata ' + feed_id
    model = make_rss_data_model feed_id
    return model
          
  
  module.exports =
    RssFeedList: RssFeedList
    