define ['sample'], (sample) ->

  test 'simple test', ->
    equal 1 + 1, 2

  test 'sample adder', ->
    equal sample.adder(1, 2), 3

