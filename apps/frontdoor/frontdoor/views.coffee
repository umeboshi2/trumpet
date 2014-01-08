define (require, exports, module) ->
  Backbone = require 'backbone'
  MSGBUS = require 'msgbus'
  Marionette = require 'marionette'

  Templates = require 'views/templates'

  class LoginView extends Backbone.Marionette.ItemView
    template: Templates.login_form
    
    
  
  module.exports =
    LoginView: LoginView
    