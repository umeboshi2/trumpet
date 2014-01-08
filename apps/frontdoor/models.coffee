define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    ########################################
    # Collections
    ########################################

    class SitePath extends Backbone.Model
        defaults:
            name: ''
            type: 'path'
    class SiteAppResource extends Backbone.Model
        defaults:
            name: ''
            type: 'coffee'
            
                        
    
    class SiteTemplate extends Backbone.Model
        defaults:
            name: ''
            content: ''
            type: 'tmpl'
                        
    class SiteCSS extends Backbone.Model
        defaults:
            name: ''
            content: ''
            type: 'css'
                        
    class SiteJS extends Backbone.Model
        defaults:
            name: ''
            content: ''
            type: 'js'



    module.exports =
        SitePath: SitePath
        SiteAppResource: SiteAppResource
        SiteTemplate: SiteTemplate
        SiteCSS: SiteCSS
        SiteJS: SiteJS
        
    
    
