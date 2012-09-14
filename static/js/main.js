(function() {

  define(['config'], function() {
    return require(['i18n'], function(I18n) {
      if (typeof console !== "undefined" && console !== null) {
        if (typeof console.log === "function") console.log('main module loaded!');
      }
      return I18n.install();
    });
  });

}).call(this);
