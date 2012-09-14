(function() {
  var __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; },
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  define(['module', 'jquery', 'gettext'], function(module, $, Gettext) {
    var NullTranslations, Translations, find, getCatalog, install;
    NullTranslations = (function() {

      function NullTranslations() {}

      NullTranslations.prototype.gettext = function() {
        return Gettext.strargs(arguments[0], Array.prototype.slice.call(arguments, 1));
      };

      NullTranslations.prototype.ngettext = function() {
        return Gettext.strargs(arguments[2] > 1 ? arguments[1] : arguments[0], Array.prototype.slice.call(arguments, 2));
      };

      NullTranslations.prototype.install = function(names) {
        var _this = this;
        if (names == null) names = ['gettext', 'ngettext'];
        if (__indexOf.call(names, 'gettext') >= 0) {
          window.__ = function() {
            return _this.gettext.apply(_this, arguments);
          };
        }
        if (__indexOf.call(names, 'ngettext') >= 0) {
          return window.n_ = function() {
            return _this.ngettext.apply(_this, arguments);
          };
        }
      };

      return NullTranslations;

    })();
    Translations = (function(_super) {

      __extends(Translations, _super);

      function Translations(catalog, domain, gettextClass) {
        if (domain == null) domain = 'main';
        if (gettextClass == null) gettextClass = Gettext;
        this.gt = new gettextClass({
          domain: domain,
          locale_data: catalog
        });
      }

      Translations.prototype.gettext = function() {
        return Gettext.strargs(this.gt.gettext.apply(this.gt, arguments), Array.prototype.slice.call(arguments, 1));
      };

      Translations.prototype.ngettext = function() {
        return Gettext.strargs(this.gt.ngettext.apply(this.gt, arguments), Array.prototype.slice.call(arguments, 2));
      };

      return Translations;

    })(NullTranslations);
    find = function(domain, language, localeUrl) {
      if (domain == null) domain = 'main';
      if (language == null) language = 'en';
      if (localeUrl == null) localeUrl = 'locale';
      return "" + localeUrl + "/" + language + "/" + domain + ".json";
    };
    getCatalog = function(url, cb) {
      url = require.toUrl(url);
      return $.ajax({
        url: url
      }).done(function(data) {
        return cb(data);
      }).fail(function() {
        return cb(null);
      });
    };
    install = function(domain, language, localeUrl) {
      var catalogUrl;
      if (domain == null) domain = 'main';
      if (localeUrl == null) localeUrl = 'locale';
      if (language == null) language = module.config().language;
      catalogUrl = find(domain, language, localeUrl);
      return getCatalog(catalogUrl, function(catalog) {
        var t;
        if (catalog) {
          t = new Translations(catalog, domain);
        } else {
          t = new NullTranslations();
        }
        return t.install();
      });
    };
    return {
      Gettext: Gettext,
      NullTranslations: NullTranslations,
      Translations: Translations,
      find: find,
      getCatalog: getCatalog,
      install: install
    };
  });

}).call(this);
