requirejs.config
  paths:
    'lib': '../lib'
    'jquery': '../lib/jquery-1.8.1.min'
    'underscore': '../lib/underscore'
    'backbone': '../lib/backbone'
    'gettext': '../lib/Gettext'
    'locale': '../locale'
    'tests': '../tests'
    'sinon': '../lib/sinon-1.4.2'
  shim:
    'backbone':
      deps: ['underscore', 'jquery']
      exports: 'Backbone'
    'underscore':
      exports: '_'
    'sinon':
      exports: 'sinon'
    'gettext':
      exports: 'Gettext'
  config:
    'i18n':
      language: 'pt_BR'
