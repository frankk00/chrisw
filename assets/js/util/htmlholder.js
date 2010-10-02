/*
  htmlholder.js
  
  A simple html repacer which could import some parameters into specific html
  page.
*/

function HTMLHolder(html) {
  this._htmlContain = html;
}

HTMLHolder.prototype.getHTML = function (para) {
  var result = this._htmlContain;
  for (var i = 0; i < para.length; i++) {
    result = result.replace("\\" + i, para[i]);
  }
  return result;
}