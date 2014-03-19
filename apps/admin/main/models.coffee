define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  ########################################
  # Models
  ########################################


  class User extends Backbone.Model
    defaults:
      username: ''

  class Group extends Backbone.Model
    defaults:
      name: ''

  module.exports =
    User: User
    Group: Group
    