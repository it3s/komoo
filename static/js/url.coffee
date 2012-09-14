define
  load: (name, req, load, config) ->
    url = req.toUrl name
    load url
