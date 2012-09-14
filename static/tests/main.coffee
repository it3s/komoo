require ['config'], () ->  # Loads a common configuration file
  require [
      'tests/sample_test'
      'tests/i18n'
    ], () ->
      console?.log?('tests module loaded!')
      QUnit.start();  # Tests loaded, run tests
