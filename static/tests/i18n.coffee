define ['sinon', 'i18n'], (sinon, I18n) ->

  TESTING = 'testing'
  NTESTING = 'ntesting'

  TRANSLATED = 'translated'
  NTRANSLATED = 'ntranslated'

  DOMAIN = 'test'
  CATALOG_TEXT = """{
    "#{DOMAIN}": {
      "": {"Plural-Forms": "nplurals=2; plural=(n > 1)"},
      "#{TESTING}": [null, "#{TRANSLATED}"],
      "#{TESTING}": ["#{NTESTING}", "#{TRANSLATED}", "#{NTRANSLATED}"]
    }
  }"""
  CATALOG = JSON.parse CATALOG_TEXT

  t = null
  module 'i18n.NullTranslations',
    setup: ->
      t = new I18n.NullTranslations
    teardown: ->
      t = undefined

  test 'gettext', ->
    expect 1
    translated = t.gettext TESTING

    equal translated, TESTING, 'Should return the same string'

  test 'ngettext with singular', ->
    expect 1
    COUNT = 1
    ntranslated = t.ngettext TESTING, NTESTING, COUNT

    equal ntranslated, TESTING, 'Should return the untranslated singular string'

  test 'ngettext with plural', ->
    expect 1
    COUNT = 2
    ntranslated = t.ngettext TESTING, NTESTING, COUNT

    equal ntranslated, NTESTING, 'Should return the untranslated singular string'


  gtFake = null
  gt = null
  module 'i18n.Translations',
    setup: ->
      gtFake =
        gettext: sinon.stub().returns TRANSLATED
        ngettext: sinon.stub().returns NTRANSLATED

      gt = sinon.stub().returns gtFake
      t = new I18n.Translations CATALOG, DOMAIN, gt
    teardown: ->
      delete window.__
      delete window.n_
      t = undefined
      gt = undefined
      gtFake = undefined

  test 'constructor', ->
    expect 2
    ok gt.calledOnce, 'Should create only one instance of Gettext'
    ok gt.calledWith({ domain: DOMAIN, locale_data: CATALOG}),
        'Should create the instance of Gettext passing the correct argument'

  test 'gettext', ->
    expect 3
    translated = t.gettext TESTING

    ok gtFake.gettext.calledOnce, 'Should call gettext method once'
    ok gtFake.gettext.calledWith(TESTING),
        'Should call gettext method with "testing"'
    equal translated, TRANSLATED, 'Should return the translated string'


  test 'ngettext with singular', ->
    expect 3
    COUNT = 1
    ntranslated = t.ngettext TESTING, NTESTING, COUNT

    ok gtFake.ngettext.calledOnce, 'Should call ngettext method once'
    ok gtFake.ngettext.calledWith(TESTING, NTESTING, COUNT),
        'Should call ngettext method with the correct arguments'
    equal ntranslated, NTRANSLATED, 'Should return the ntranslated string'

  test 'ngettext with plural', ->
    expect 3
    COUNT = 2
    ntranslated = t.ngettext TESTING, NTESTING, COUNT

    ok gtFake.ngettext.calledOnce, 'Should call ngettext method once'
    ok gtFake.ngettext.calledWith(TESTING, NTESTING, COUNT),
        'Should call ngettext method with the correct arguments"'
    equal ntranslated, NTRANSLATED, 'Should return the ntranslated string'

  test 'install', ->
    expect 6
    deepEqual window.__, undefined, 'Should not have __ as global yet'
    deepEqual window.n_, undefined, 'Should not have n_ as global yet'

    t.install()

    ok window.__, 'Should have __ as global'
    ok window.n_, 'Should have n_ as global'

    translated = t.gettext TESTING
    gtranslated = __ TESTING

    equal translated, gtranslated, 'Should __ return the correct string'

    COUNT = 2
    ntranslated = t.ngettext TESTING, NTESTING, COUNT
    gntranslated = n_ TESTING, NTESTING, COUNT

    equal ntranslated, gntranslated, 'Should n_ return the correct string'

  test 'install only gettext', ->
    expect 4
    deepEqual window.__, undefined, 'Should not have __ as global yet'
    deepEqual window.n_, undefined, 'Should not have n_ as global'

    t.install(['gettext'])

    ok window.__, 'Should have __ as global'
    deepEqual window.n_, undefined, 'Should not have n_ as global'

  module 'i18n.Translations integration with Gettext'

  test 'constructor', ->
    expect 1
    t = new I18n.Translations CATALOG, DOMAIN
    equal typeof(t), 'object',
        'Should create an instance if using correct arguments'

  module 'i18n.Translations integration with Gettext',
      setup: ->
        t = new I18n.Translations CATALOG, DOMAIN

  test 'gettext', ->
    expect 1
    translated = t.gettext TESTING
    equal translated, TRANSLATED, 'Should return the translated string'


  test 'ngettext with singular', ->
    expect 1
    COUNT = 1
    ntranslated = t.ngettext TESTING, NTESTING, COUNT
    equal ntranslated, TRANSLATED, 'Should return the ntranslated string'

  test 'ngettext with plural', ->
    expect 1
    COUNT = 2
    ntranslated = t.ngettext TESTING, NTESTING, COUNT
    equal ntranslated, NTRANSLATED, 'Should return the ntranslated string'


  server = null
  module 'i18n helpers',
    setup: ->
      server = sinon.fakeServer.create()
      window.server = server
    teardown: ->
      server.restore()
      delete window.__
      delete window.n_

  test 'find', ->
    expect 1
    url = I18n.find 'test', 'pt_BR', 'locale'
    equal url, 'locale/pt_BR/test.json'

  test 'getCatalog success', ->
    expect 2
    server.respondWith [
      200
      'Content-Type': 'application/json'
      CATALOG_TEXT
    ]

    cb = sinon.spy()

    I18n.getCatalog 'url/to/catalog.json', cb

    server.respond()

    ok cb.calledOnce
    ok cb.calledWith CATALOG

  test 'getCatalog fail', ->
    expect 2
    server.respondWith [400, {}, '']

    cb = sinon.spy()

    I18n.getCatalog 'url/to/catalog.json', cb

    server.respond()

    ok cb.calledOnce
    ok cb.calledWith null

  test 'install success', ->
    expect 5
    server.respondWith [
      200
      'Content-Type': 'application/json'
      CATALOG_TEXT
    ]

    deepEqual window.__, undefined, 'Should not have __ as global yet'
    deepEqual window.n_, undefined, 'Should not have n_ as global yet'

    I18n.install(DOMAIN)

    server.respond()

    ok window.__, 'Should have __ as global'
    ok window.n_, 'Should have n_ as global'

    translated = window.__ TESTING
    equal translated, TRANSLATED, 'Should return the translated string'

  test 'install fail', ->
    expect 5
    server.respondWith [400, {}, '']

    deepEqual window.__, undefined, 'Should not have __ as global yet'
    deepEqual window.n_, undefined, 'Should not have n_ as global yet'

    I18n.install(DOMAIN)

    server.respond()

    ok window.__, 'Should have __ as global'
    ok window.n_, 'Should have n_ as global'

    translated = __ TESTING
    equal translated, TESTING, 'Should return the translated string'
