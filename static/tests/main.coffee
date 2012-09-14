require ['config'], () ->  # Loads a common configuration file
  require [
      'tests/sample_test'
    ], () ->
      console?.log?('tests module loaded!')
      QUnit.start();  # Tests loaded, run tests
