define (require, exports, module) ->
    module.exports =
        # bower components
        jquery: '/components/jquery/jquery'
        underscore: '/components/underscore-amd/underscore'
        backbone: '/components/backbone-amd/backbone'
        'backbone.wreqr': '/components/backbone.wreqr/lib/amd/backbone.wreqr'
        'backbone.babysitter': '/components/backbone.babysitter/lib/amd/backbone.babysitter'
        marionette: '/components/marionette/lib/core/amd/backbone.marionette'
        'jquery-ui': '/components/jquery-ui/ui/jquery-ui'
        ace: '/components/ace/lib/ace'
        bootstrap: '/components/bootstrap/dist/js/bootstrap'
        bsModal: '/components/bootstrap/js/modal'
        
        # self tracked upstream assets
        teacup: '/stdlib/teacup'
        
        # common assets
        common: '/apps/common/app'

        