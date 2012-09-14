(function() {

  define(['sinon', 'sample'], function(sinon, sample) {
    module('simple examples');
    test('1 + 1', function() {
      expect(1);
      return equal(1 + 1, 2, 'Should be equal to 2');
    });
    module('sample module');
    test('adder', function() {
      expect(1);
      return equal(sample.adder(1, 2), 3, 'Should return 3 when add 1 and 2');
    });
    return test('callbacker (using spy)', function() {
      var HEY, cb;
      expect(2);
      HEY = 'Hey!';
      cb = sinon.spy();
      sample.callbacker(cb, HEY);
      ok(cb.calledOnce, 'Should be called once');
      return ok(cb.calledWith(HEY), 'Should be called with "Hey!" string');
    });
  });

}).call(this);
