(function() {

  requirejs.config({
    baseUrl: '/static/js',
    paths: {
      lib: '../lib',
      jquery: '../lib/jquery-1.8.1.min',
      underscore: '../lib/underscore',
      backbone: '../lib/backbone',
      tests: '../tests'
    },
    shim: {
      backbone: {
        deps: ['underscore', 'jquery'],
        exports: 'Backbone'
      },
      underscore: {
        exports: '_'
      }
    }
  });

  define(["jquery", "underscore", "backbone"], function($, _, Backbone) {
    return typeof console !== "undefined" && console !== null ? typeof console.log === "function" ? console.log('main module loaded!') : void 0 : void 0;
  });

}).call(this);
