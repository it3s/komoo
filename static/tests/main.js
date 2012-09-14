(function() {

  require(['config'], function() {
    return require(['tests/sample_test'], function() {
      if (typeof console !== "undefined" && console !== null) {
        if (typeof console.log === "function") console.log('tests module loaded!');
      }
      return QUnit.start();
    });
  });

}).call(this);
