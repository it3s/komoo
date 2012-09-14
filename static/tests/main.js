(function() {

  require(['config'], function() {
    return require(['tests/sample_test', 'tests/i18n'], function() {
      if (typeof console !== "undefined" && console !== null) {
        if (typeof console.log === "function") console.log('tests module loaded!');
      }
      return QUnit.start();
    });
  });

}).call(this);
