/*
  loader.js
  
  A short-cuts to load javascript and css files.
*/

function loadJavascriptFiles(files) {
  for (var i = 0; i < files.length; i++) {
    $.rloader({type: 'js', src: files[i]})
  }
}

function loadCssFiles(files) {
  for (var i = 0; i < files.length; i++) {
    $.rloader({type: 'css', src: files[i]})
  }
}