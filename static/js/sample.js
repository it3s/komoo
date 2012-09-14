define(function() {
  var adder, callbacker;
  adder = function(a, b) {
    return a + b;
  };
  callbacker = function(cb, p) {
    return cb(p);
  };
  return {
    adder: adder,
    callbacker: callbacker
  };
});
