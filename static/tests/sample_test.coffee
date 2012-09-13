define ['sample'], (sample) ->

  module 'simple examples'

  test '1 + 1', ->
    expect 1
    equal 1 + 1, 2, 'Should be equal to 2'


  module 'sample module'

  test 'adder', ->
    expect 1
    equal sample.adder(1, 2), 3, 'Should return 3 when add 1 and 2'

  test 'callbacker (using spy)', ->
    expect 2

    HEY = 'Hey!'
    cb = sinon.spy()
    sample.callbacker cb, HEY

    ok cb.calledOnce, 'Should be called once'
    ok cb.calledWith(HEY), 'Should be called with "Hey!" string'

