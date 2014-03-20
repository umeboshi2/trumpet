# require config comes first
require.config
  baseUrl: 'user'
  paths:
    jquery: '/components/jquery/jquery'
    #underscore: '/components/underscore-amd/underscore'
    underscore: '/components/lodash/dist/lodash.compat'
    backbone: '/components/backbone-amd/backbone'
    'backbone.wreqr': '/components/backbone.wreqr/lib/amd/backbone.wreqr'
    'backbone.babysitter': '/components/backbone.babysitter/lib/amd/backbone.babysitter'
    marionette: '/components/marionette/lib/core/amd/backbone.marionette'
    validation: '/components/backbone.validation/dist/backbone-validation-amd'
    bootstrap: '/components/bootstrap/dist/js/bootstrap'
    'jquery-ui': '/components/jquery-ui/ui/jquery-ui'
    requirejs: '/components/requirejs/require'
    text: '/components/requirejs-text/text'
    teacup: '/components/teacup/lib/teacup'
    ace: '/components/ace-builds/src/ace'
    marked: '/components/marked/lib/marked'
    
    common: '/app/common'

    # FIXME: work with using bootstrap components
    bsModal: '/components/bootstrap/js/modal'

  # FIXME:  try to reduce the shim to only the
  # necessary resources
  shim:
    #jquery:
    #  exports: ['$', 'jQuery']
    bootstrap:
      deps: ['jquery']
    bsModal:
      deps: ['jquery']


requirements = [
  'application'
  'frontdoor/main'
  ]

require [
  'application'
  'frontdoor/main'
  ], (App) ->
  # debug
  window.app = App
  
  start_app_one = () ->
    if App.ready == false
      setTimeout(start_app_two, 100)
    else
      App.start()
        
  start_app_two = () ->
    if App.ready == false
      setTimeout(start_app_one, 100)
    else
      App.start()
    
  start_app_one()
    
