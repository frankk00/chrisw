/*
  vertical.js
  
  Series of some standard views.
*/

function VerticalLayout(container) {
  this._views = [];
  this._names = [];
  this.container = container;
}

VerticalLayout.prototype.registView = function(div) {
  if (div == null) {
    div = document.createElement("div");
  }
  this.container.appendChild(div);
  return div;
}

VerticalLayout.prototype.appendView = function(viewName, view) {
  this._views.push(view);
  this._names.push(viewName);
}

VerticalLayout.prototype.removeAll = function() {
  this._views = [];
  this._names = [];
  this.container.innerHTML = "";
}

VerticalLayout.prototype.findView = function(viewName) {
  var x = this._indexOf(viewName);
  if (x != -1) {
    return this._views[x];
  }
  return null;
}

VerticalLayout.prototype._indexOf = function(viewName) {
  for (var i = 0; i < this._names.length; i++) {
    if (this._names[i] == viewName) {
      return i;
    }
  }
  return -1;
}