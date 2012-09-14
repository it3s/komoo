(function() {

  define({
    load: function(name, req, load, config) {
      var url;
      url = req.toUrl(name);
      return load(url);
    }
  });

}).call(this);
