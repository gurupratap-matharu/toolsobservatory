/* global marked */

(() => {
  'use strict'

  const inputEl = document.querySelector('#input')
  const outputEl = document.querySelector('#output')
  const convertBtn = document.querySelector('#convert')

  convertBtn.addEventListener('click', function () {
    outputEl.innerHTML = marked.parse(inputEl.value)
  })

  function copy () {
    const copyText = document.querySelector('#output')
    copyText.select()
    document.execCommand('copy')
  }

  document.querySelector('#copy').addEventListener('click', copy)
})()
