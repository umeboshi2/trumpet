# modular template loading
define (require, exports, module) ->
  $ = require 'jquery'
  _ = require 'underscore'
  Backbone = require 'backbone'
  teacup = require 'teacup'

  renderable = teacup.renderable

  div = teacup.div
  # I use "icon" for font-awesome
  icon = teacup.i
  strong = teacup.strong
  span = teacup.span
  label = teacup.label
  input = teacup.input

  text = teacup.text
  img = teacup.img
  # Main Templates must use teacup.
  # The template must be a teacup.renderable, 
  # and accept a layout model as an argument.

  # Tagnames to be used in the template.
  {div, span, link, text, strong, label, input, 
  button, a, nav, form, p,
  ul, li, b,
  h1, h2, h3,
  subtitle, section, hr
  } = teacup
            
    
  ########################################
  # Templates
  ########################################
  jellyfish = renderable () ->
    div 'listview-header', ->
      text 'Jelly fish content'
      
  page_list_entry = renderable (page) ->
    div '.listview-list-entry', ->
      span '.btn-default.btn-xs', ->
        a href:'#jellyfish/editpage/' + page.id,
        style:'color:black', ->
          icon '.edit-page.fa.fa-pencil'
      text "    "
      a href:'#jellyfish/showpage/' + page.id, page.name
        
      
  page_list = renderable () ->
    div '.listview-header', 'Wiki Pages'
    div '.listview-list'
                
  ##################################################################
  # ##########################
  ##################################################################    
          
  module.exports =
    jellyfish: jellyfish
    page_list_entry: page_list_entry
    page_list: page_list
    