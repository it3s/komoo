define ['module', 'jquery', 'gettext'], (module, $, Gettext) ->

  class NullTranslations
    gettext: () ->
      Gettext.strargs(
        arguments[0],
        Array.prototype.slice.call(arguments, 1)
      )

    ngettext: () ->
      Gettext.strargs(
        if arguments[2] > 1 then arguments[1] else arguments[0],
        Array.prototype.slice.call(arguments, 2)
      )

    install: (names=['gettext', 'ngettext']) ->
      if 'gettext' in names
        window.__ = () => @gettext.apply this, arguments

      if 'ngettext' in names
        window.n_ = () => @ngettext.apply this, arguments


  class Translations extends NullTranslations
    constructor: (catalog, domain='main', gettextClass=Gettext) ->
      @gt = new gettextClass domain: domain, locale_data: catalog

    gettext: () ->
      Gettext.strargs(
        @gt.gettext.apply(@gt, arguments),
        Array.prototype.slice.call(arguments, 1)
      )

    ngettext: () ->
      Gettext.strargs(
        @gt.ngettext.apply(@gt, arguments),
        Array.prototype.slice.call(arguments, 2)
      )


  find = (domain='main', language='en', localeUrl='locale') ->
    "#{localeUrl}/#{language}/#{domain}.json"

  getCatalog = (url, cb) ->
    url = require.toUrl url
    $.ajax(url: url).done((data) ->
      cb data
    ).fail(->
      cb null
    )

  install = (domain='main', language, localeUrl='locale') ->
    language ?= module.config().language
    catalogUrl = find domain, language, localeUrl
    getCatalog catalogUrl, (catalog) ->
      if catalog
        t = new Translations catalog, domain
      else
        t = new NullTranslations()
      t.install()

  return {
    Gettext: Gettext
    NullTranslations: NullTranslations
    Translations: Translations
    find: find
    getCatalog: getCatalog
    install: install
  }
