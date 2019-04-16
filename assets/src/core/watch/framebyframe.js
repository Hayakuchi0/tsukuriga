import { doc, ready, range } from '../../utils'


class Video {
  constructor(video) {
    this.$el = doc(video)[0]
    const fps = parseInt(this.$el.dataset.fps)
    const duration = parseFloat(this.$el.dataset.duration)
    if (!fps || !duration) {
      throw Error("動画情報が取得できませんでした")
    }
    const frameLength = 1 / fps
    const framesCount = Math.floor(fps * duration)
    this.frames = range(framesCount).map(i => i * frameLength)
  }

  get currentFrame() {
    let minDiffFrame = 0
    let diff = []
    this.frames.forEach((frameVal, frame) => {
      diff[frame] = Math.abs(this.$el.currentTime - frameVal)
      minDiffFrame = (diff[minDiffFrame] < diff[frame]) ? minDiffFrame : frame
    })
    return minDiffFrame
  }

  ready() {
    if (this.$el.currentTime === 0) this.$el.play()
    if (!this.$el.paused) this.$el.pause()
    return this
  }

  push_frame() {
    if (this.currentFrame >= this.frames.length) return
    this.$el.currentTime = parseFloat(this.frames[this.currentFrame + 1])
  }

  back_frame() {
    if (this.currentFrame <= 0) return
    this.$el.currentTime = parseFloat(this.frames[this.currentFrame - 1])
  }
}

ready(() => {
  const video = new Video('video')
  doc('#prev-frame')[0].addEventListener('click', () => {
    video.ready().back_frame()
  })
  doc('#next-frame')[0].addEventListener('click', () => {
    video.ready().push_frame()
  })
})
