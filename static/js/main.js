(function() {

  require(['config'], function() {
    return require(["jquery", "underscore", "backbone"], function($, _, Backbone) {
      return typeof console !== "undefined" && console !== null ? typeof console.log === "function" ? console.log('main module loaded!') : void 0 : void 0;
    });
  });

}).call(this);
