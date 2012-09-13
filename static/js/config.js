(function() {

  requirejs.config({
    paths: {
      'lib': '../lib',
      'tests': '../tests'
    },
    map: {
      '*': {
        'jquery': '../lib/jquery-1.8.1.min',
        'underscore': '../lib/underscore',
        'backbone': '../lib/backbone'
      }
    },
    shim: {
      'backbone': {
        deps: ['underscore', 'jquery'],
        exports: 'Backbone'
      },
      'underscore': {
        exports: '_'
      }
    }
  });

}).call(this);
