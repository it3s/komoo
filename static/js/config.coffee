requirejs.config
  paths:
    'lib': '../lib'
    'tests': '../tests'
    'jquery': '../lib/jquery-1.8.1.min'
    'underscore': '../lib/underscore'
    'backbone': '../lib/backbone'
    'gettext': '../lib/Gettext'
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
