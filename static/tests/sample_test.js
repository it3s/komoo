(function() {

  define(['sample'], function(sample) {
    test('simple test', function() {
      return equal(1 + 1, 2);
    });
    return test('sample adder', function() {
      return equal(sample.adder(1, 2), 3);
    });
  });

}).call(this);
