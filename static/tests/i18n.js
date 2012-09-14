(function() {

  define(['sinon', 'i18n'], function(sinon, I18n) {
    var CATALOG, CATALOG_TEXT, DOMAIN, NTESTING, NTRANSLATED, TESTING, TRANSLATED, gt, gtFake, server, t;
    TESTING = 'testing';
    NTESTING = 'ntesting';
    TRANSLATED = 'translated';
    NTRANSLATED = 'ntranslated';
    DOMAIN = 'test';
    CATALOG_TEXT = "{\n  \"" + DOMAIN + "\": {\n    \"\": {\"Plural-Forms\": \"nplurals=2; plural=(n > 1)\"},\n    \"" + TESTING + "\": [null, \"" + TRANSLATED + "\"],\n    \"" + TESTING + "\": [\"" + NTESTING + "\", \"" + TRANSLATED + "\", \"" + NTRANSLATED + "\"]\n  }\n}";
    CATALOG = JSON.parse(CATALOG_TEXT);
    t = null;
    module('i18n.NullTranslations', {
      setup: function() {
        return t = new I18n.NullTranslations;
      },
      teardown: function() {
        return t = void 0;
      }
    });
    test('gettext', function() {
      var translated;
      expect(1);
      translated = t.gettext(TESTING);
      return equal(translated, TESTING, 'Should return the same string');
    });
    test('ngettext with singular', function() {
      var COUNT, ntranslated;
      expect(1);
      COUNT = 1;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      return equal(ntranslated, TESTING, 'Should return the untranslated singular string');
    });
    test('ngettext with plural', function() {
      var COUNT, ntranslated;
      expect(1);
      COUNT = 2;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      return equal(ntranslated, NTESTING, 'Should return the untranslated singular string');
    });
    gtFake = null;
    gt = null;
    module('i18n.Translations', {
      setup: function() {
        gtFake = {
          gettext: sinon.stub().returns(TRANSLATED),
          ngettext: sinon.stub().returns(NTRANSLATED)
        };
        gt = sinon.stub().returns(gtFake);
        return t = new I18n.Translations(CATALOG, DOMAIN, gt);
      },
      teardown: function() {
        delete window.__;
        delete window.n_;
        t = void 0;
        gt = void 0;
        return gtFake = void 0;
      }
    });
    test('constructor', function() {
      expect(2);
      ok(gt.calledOnce, 'Should create only one instance of Gettext');
      return ok(gt.calledWith({
        domain: DOMAIN,
        locale_data: CATALOG
      }), 'Should create the instance of Gettext passing the correct argument');
    });
    test('gettext', function() {
      var translated;
      expect(3);
      translated = t.gettext(TESTING);
      ok(gtFake.gettext.calledOnce, 'Should call gettext method once');
      ok(gtFake.gettext.calledWith(TESTING), 'Should call gettext method with "testing"');
      return equal(translated, TRANSLATED, 'Should return the translated string');
    });
    test('ngettext with singular', function() {
      var COUNT, ntranslated;
      expect(3);
      COUNT = 1;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      ok(gtFake.ngettext.calledOnce, 'Should call ngettext method once');
      ok(gtFake.ngettext.calledWith(TESTING, NTESTING, COUNT), 'Should call ngettext method with the correct arguments');
      return equal(ntranslated, NTRANSLATED, 'Should return the ntranslated string');
    });
    test('ngettext with plural', function() {
      var COUNT, ntranslated;
      expect(3);
      COUNT = 2;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      ok(gtFake.ngettext.calledOnce, 'Should call ngettext method once');
      ok(gtFake.ngettext.calledWith(TESTING, NTESTING, COUNT), 'Should call ngettext method with the correct arguments"');
      return equal(ntranslated, NTRANSLATED, 'Should return the ntranslated string');
    });
    test('install', function() {
      var COUNT, gntranslated, gtranslated, ntranslated, translated;
      expect(6);
      deepEqual(window.__, void 0, 'Should not have __ as global yet');
      deepEqual(window.n_, void 0, 'Should not have n_ as global yet');
      t.install();
      ok(window.__, 'Should have __ as global');
      ok(window.n_, 'Should have n_ as global');
      translated = t.gettext(TESTING);
      gtranslated = __(TESTING);
      equal(translated, gtranslated, 'Should __ return the correct string');
      COUNT = 2;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      gntranslated = n_(TESTING, NTESTING, COUNT);
      return equal(ntranslated, gntranslated, 'Should n_ return the correct string');
    });
    test('install only gettext', function() {
      expect(4);
      deepEqual(window.__, void 0, 'Should not have __ as global yet');
      deepEqual(window.n_, void 0, 'Should not have n_ as global');
      t.install(['gettext']);
      ok(window.__, 'Should have __ as global');
      return deepEqual(window.n_, void 0, 'Should not have n_ as global');
    });
    module('i18n.Translations integration with Gettext');
    test('constructor', function() {
      expect(1);
      t = new I18n.Translations(CATALOG, DOMAIN);
      return equal(typeof t, 'object', 'Should create an instance if using correct arguments');
    });
    module('i18n.Translations integration with Gettext', {
      setup: function() {
        return t = new I18n.Translations(CATALOG, DOMAIN);
      }
    });
    test('gettext', function() {
      var translated;
      expect(1);
      translated = t.gettext(TESTING);
      return equal(translated, TRANSLATED, 'Should return the translated string');
    });
    test('ngettext with singular', function() {
      var COUNT, ntranslated;
      expect(1);
      COUNT = 1;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      return equal(ntranslated, TRANSLATED, 'Should return the ntranslated string');
    });
    test('ngettext with plural', function() {
      var COUNT, ntranslated;
      expect(1);
      COUNT = 2;
      ntranslated = t.ngettext(TESTING, NTESTING, COUNT);
      return equal(ntranslated, NTRANSLATED, 'Should return the ntranslated string');
    });
    server = null;
    module('i18n helpers', {
      setup: function() {
        server = sinon.fakeServer.create();
        return window.server = server;
      },
      teardown: function() {
        server.restore();
        delete window.__;
        return delete window.n_;
      }
    });
    test('find', function() {
      var url;
      expect(1);
      url = I18n.find('test', 'pt_BR', 'locale');
      return equal(url, 'locale/pt_BR/test.json');
    });
    test('getCatalog success', function() {
      var cb;
      expect(2);
      server.respondWith([
        200, {
          'Content-Type': 'application/json'
        }, CATALOG_TEXT
      ]);
      cb = sinon.spy();
      I18n.getCatalog('url/to/catalog.json', cb);
      server.respond();
      ok(cb.calledOnce);
      return ok(cb.calledWith(CATALOG));
    });
    test('getCatalog fail', function() {
      var cb;
      expect(2);
      server.respondWith([400, {}, '']);
      cb = sinon.spy();
      I18n.getCatalog('url/to/catalog.json', cb);
      server.respond();
      ok(cb.calledOnce);
      return ok(cb.calledWith(null));
    });
    test('install success', function() {
      var translated;
      expect(5);
      server.respondWith([
        200, {
          'Content-Type': 'application/json'
        }, CATALOG_TEXT
      ]);
      deepEqual(window.__, void 0, 'Should not have __ as global yet');
      deepEqual(window.n_, void 0, 'Should not have n_ as global yet');
      I18n.install(DOMAIN);
      server.respond();
      ok(window.__, 'Should have __ as global');
      ok(window.n_, 'Should have n_ as global');
      translated = window.__(TESTING);
      return equal(translated, TRANSLATED, 'Should return the translated string');
    });
    return test('install fail', function() {
      var translated;
      expect(5);
      server.respondWith([400, {}, '']);
      deepEqual(window.__, void 0, 'Should not have __ as global yet');
      deepEqual(window.n_, void 0, 'Should not have n_ as global yet');
      I18n.install(DOMAIN);
      server.respond();
      ok(window.__, 'Should have __ as global');
      ok(window.n_, 'Should have n_ as global');
      translated = __(TESTING);
      return equal(translated, TESTING, 'Should return the translated string');
    });
  });

}).call(this);
