(() => {
  'use strict'

  const inputEl = document.querySelector('#input')
  const charEl = document.querySelector('#char-count')
  const wordEl = document.querySelector('#word-count')
  const lineEl = document.querySelector('#line-count')
  const sizeEl = document.querySelector('#byte-size')

  function getByteSize (text) {
    const encoder = new TextEncoder()
    return encoder.encode(text).length
  }

  inputEl.addEventListener('input', function () {
    charEl.textContent = inputEl.value.length
    wordEl.textContent = inputEl.value.trim().split(/\s+/).length
    lineEl.textContent = inputEl.value.split('\n').length
    sizeEl.textContent = getByteSize(inputEl.value)
  })
})()
