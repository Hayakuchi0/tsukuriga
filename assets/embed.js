var embedTsukurigaVideo = function() {
  var blockquotes = document.getElementsByTagName('blockquote')
  for (var i = 0; i < blockquotes.length; i++) {
    var bq = blockquotes[i]
    var regex = new RegExp('tsukuriga\\.net\\/watch\\/(\\w+)', 'g')

    var links = bq.getElementsByTagName('a')
    for (var j = 0; j < links.length; j++) {
      var link = links[j]

      while (true) {
        var match = regex.exec(link.href)
        if (match == null) {
          break
        }

        var embed =
          '<div style="width:95%;">' +
          '<div style="overflow:hidden;padding-top:calc(56.25% + 30px);position:relative;">' +
          '<iframe src="https://tsukuriga.net/embed/' + match[1] + '"' +
          'style="border:0;height:100%;left:0;position:absolute;top:0;width:100%; overflow:hidden;"></iframe>' +
          '</div>' +
          '</div>'

        bq.outerHTML = embed
      }
    }
  }
}
embedTsukurigaVideo()
