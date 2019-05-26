import { docAll, ready } from './utils'

const embedTsukurigaVideo = () => {
  docAll('blockquote').forEach(bq => {
    let regex = new RegExp('tsukuriga\\.net\\/watch\\/(\\w+)', 'g')

    bq.querySelectorAll('a').forEach(link => {

      while (true) {
        let match = regex.exec(link.href)
        if (match == null) {
          break
        }

        bq.outerHTML =
          '<div style="width:95%;">' +
          '<div style="overflow:hidden;padding-top:calc(56.25% + 30px);position:relative;">' +
          '<iframe src="https://tsukuriga.net/embed/' + match[1] + '"' +
          'style="border:0;height:100%;left:0;position:absolute;top:0;width:100%; overflow:hidden;"></iframe>' +
          '</div>' +
          '</div>'
      }
    })
  })
}
ready(() => {
  embedTsukurigaVideo()
})
window.embedTsukurigaVideo = embedTsukurigaVideo
