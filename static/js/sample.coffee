define ->
  adder = (a, b) -> a + b
  callbacker = (cb, p) -> cb p

  return {
    adder: adder
    callbacker: callbacker
  }
