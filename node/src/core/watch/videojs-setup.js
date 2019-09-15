import videojs from 'video.js'
import lang_ja from 'video.js/dist/lang/ja.json'

import { ready } from '../../utils'
import './styles.scss'

ready(() => {
  videojs.addLanguage('ja', Object.assign(lang_ja, {
    'No compatible source was found for this media.': '現在エンコード処理中のため閲覧できません'
  }))
  const player = videojs('video-player', {
    'aspectRatio': '16:9'
  })
})
