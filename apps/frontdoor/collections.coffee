define (require, exports, module) ->
    $ = require 'jquery'
    _ = require 'underscore'
    Backbone = require 'backbone'

    ########################################
    # Collections
    ########################################
    class SitePathList extends Backbone.Collection
        model: SitePath
        url: '/rest/sitepath'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
                        

    class SiteAppResList extends Backbone.Collection
        model: SiteAppResource
        url: '/rest/siteapp'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
           
    class SiteTemplateList extends Backbone.Collection
        model: SiteTemplate
        url: '/rest/sitetmpl'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
                        
    class SiteCSSList extends Backbone.Collection
        model: SiteCSS
        url: '/rest/sitecss'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
                        
    class SiteJSList extends Backbone.Collection
        model: SiteJS
        url: '/rest/sitejs'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data


    module.exports =
        SitePathList: SitePathList
        SiteAppResList: SiteAppResList
        SiteTemplateList: SiteTemplateList
        SiteCSSList: SiteCSSList
        SiteJSList: SiteJSList
        
    
    
