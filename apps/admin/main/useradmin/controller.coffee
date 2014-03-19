define (require, exports, module) ->
  $ = require 'jquery'
  Backbone = require 'backbone'
  Marionette = require 'marionette'
  MSGBUS = require 'msgbus'

  Views = require 'useradmin/views'
  Collections = require 'collections'

  sidebar_model = new Backbone.Model
    header: 'User Side Bar'
    entries: [
      {
        name: 'listusers'
        label: 'List Users'
      }
      {
        name: 'adduser'
        label: 'New User'
      }
      {
        name: 'listgroups'
        label: 'List Groups'
      }
      {
        name: 'addgroup'
        label: 'Add Group'
      }
    ]
    
  
  class Controller extends Backbone.Marionette.Controller
    make_sidebar: ->
      MSGBUS.events.trigger 'sidebar:close'
      view = new Views.SideBarView model:sidebar_model
      

      window.sidebar = view
      
      MSGBUS.events.trigger 'sidebar:show', view
      
    make_main_content: ->
      MSGBUS.events.trigger 'rcontent:close'
      @set_header 'Manage Users'
      @make_sidebar()
      
    start: ->
      @make_main_content()

    set_header: (title) ->
      header = $ '#header'
      header.text title

    list_users: ->
      @make_sidebar()
      console.log "list_users called on controller"
      @set_header 'List Users'

    add_user: ->
      @make_sidebar()
      console.log "add_user called on controller"
      @set_header 'add user'
      
    list_groups: ->
      @make_sidebar()
      console.log "list_groups called on controller"
      @set_header 'List Groups'

    add_group: ->
      @make_sidebar()
      console.log "add_group called on controller"
      @set_header 'add group'
                  
    show_feed: (feed_id) ->
      @make_sidebar()
      feed_data = MSGBUS.reqres.request 'rss:feeddata', feed_id
      response = feed_data.fetch()
      response.done =>
        view = new Views.FeedDataView
          model: feed_data
        MSGBUS.events.trigger 'rcontent:show', view
        @set_header feed_data.get('feed').title
        $('html, body').animate {scrollTop: 0}, 'fast'

    show_new_feed_form: () ->
      view = new Views.NewFeedView
      MSGBUS.events.trigger 'rcontent:show', view
      #header = $ '#header'
      #header.text 'Add New RSS Feed'
      #header.html ''
      @set_header 'Add New RSS Feed'

    show_edit_feed_form: (feed_id) ->
      console.log 'show_edit_feed_form ' + feed_id
      MSGBUS.events.trigger 'rcontent:close'
      model = MSGBUS.reqres.request 'rss:getfeedinfo', feed_id
      
      view = new Views.EditFeedView
        model: model
      MSGBUS.events.trigger 'rcontent:show', view
      $('html, body').animate {scrollTop: 0}, 'fast'
      
    new_feed_added: (model) ->
      MSGBUS.events.trigger 'sidebar:close'
      feeds = MSGBUS.reqres.request 'rss:feedlist'
      view = new Views.FeedListView
        collection: feeds
      response = feeds.fetch()
      response.done ->
        console.log 'feeds fetched'
      MSGBUS.events.trigger 'sidebar:show', view
      MSGBUS.events.trigger 'rcontent:close'

    feed_info_updated: (model) ->
      console.log 'feed_info_updated called'
      @show_feed model.id
      url = '#simplerss/showfeed/' + model.id
      Backbone.history.navigate url
      
      
              
  module.exports = Controller
  
