import { doc, ready, range } from '../../utils'


class Video {
  constructor(video) {
    this.$el = doc(video)
    const fps = parseInt(this.$el.dataset.fps)
    const duration = parseFloat(this.$el.dataset.duration)
    if (!fps || !duration) {
      throw Error('動画情報が取得できませんでした')
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

  const push_frame = () => video.ready().push_frame()
  const back_frame = () => video.ready().back_frame()

  doc('#next-frame').addEventListener('click', push_frame)
  doc('#prev-frame').addEventListener('click', back_frame)

  document.addEventListener('keydown', e => {
    if (document.activeElement.tagName === 'TEXTAREA' || e.shiftKey || e.altKey || e.ctrlKey || e.metaKey) return

    switch (e.code) {
      case 'ArrowRight':
        push_frame()
        e.preventDefault()
        break
      case 'ArrowLeft':
        back_frame()
        e.preventDefault()
        break
      case 'Space':
        if (video.$el.paused) {
          video.$el.play()
        } else {
          video.$el.pause()
        }
        e.preventDefault()
        break
    }
  })
})
