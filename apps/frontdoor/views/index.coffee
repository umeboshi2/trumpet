define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'
    templates = require 'view/templates'
    
    ########################################
    # Index View
    ########################################
    class IndexView extends Backbone.View
        el: $ 'page'
        


    module.exports =
        SitePath: SitePath
        SiteAppResource: SiteAppResource
        SiteTemplate: SiteTemplate
        SiteCSS: SiteCSS
        SiteJS: SiteJS
        
    
    

