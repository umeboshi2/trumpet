# my config

define [], () ->
    require.config
        baseUrl: '/stdlib'
        paths:
            jquery: '../bower_components/jquery/jquery'
            ace: '../bower_components/ace/lib/ace'
            backbone: '../bower_components/backbone/backbone'
            bootstrap: '../bower_components/bootstrap/dist/js/bootstrap'
            'jquery-ui': '../bower_components/jquery-ui/ui/jquery-ui'
            requirejs: '../bower_components/requirejs/require'
            underscore: '../bower_components/underscore/underscore'
        shim:
            backbone:
                deps: ['underscore', 'jquery']
                exports: 'Backbone'
            underscore:
                exports: '_'
            jquery:
                exports: ['$', 'jQuery']
            teacup:
                exports: ['teacup']

