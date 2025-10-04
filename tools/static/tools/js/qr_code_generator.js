/* global QRCode */

(() => {
  'use strict'

  const inputEl = document.querySelector('#input')
  const outputEl = document.querySelector('#output')
  const generateBtn = document.querySelector('#generate')

  generateBtn.addEventListener('click', function () {
    outputEl.replaceChildren()
    const qrcode = new QRCode(outputEl, {
      text: inputEl.value,
      width: 600,
      height: 600,
      colorDark: document.querySelector('#foreground').value,
      colorLight: document.querySelector('#background').value,
      correctLevel: QRCode.CorrectLevel.H
    })
  })

  function download () {
    const image = outputEl.querySelector('img')
    const imageUrl = image.src
    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `qrcode-${inputEl.value}.png`
    link.click()
  }

  document.querySelector('#download').addEventListener('click', download)
})()
