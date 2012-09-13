define ['config'], () ->  # Loads a common configuration file
  require ['jquery', 'underscore', 'backbone'], ($, _, Backbone) ->
    console?.log?('main module loaded!')
