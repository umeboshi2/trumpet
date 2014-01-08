
define [
    'teacup'
], (teacup) ->
    'use strict'
    { renderable, div, header, ul, li, a, h1, p } = teacup
    renderable () ->
        p 'message'
