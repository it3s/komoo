define ['config'], () ->  # Loads a common configuration file
  require ['i18n'], (I18n) ->
    console?.log?('main module loaded!')
    I18n.install()
