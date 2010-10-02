function StandardPanel(layout) {
  this.layout = layout;
}

StandardPanel.prototype.hashmark = function() {
  return "standardpanel";
}

function SlidePanel(id, layout) {
  this._id = id;
  this.layout = layout;
  this._title = "";
  this._on = false;
}

SlidePanel.prototype.hashmark = function() {
  return "slidepanel";
}

SlidePanel.prototype.click = function(title, onDone) {
  if (!this._on) {
    this._on = true;
    this._title = title;
    $("#" + this._id).show("slide", {}, 1000, onDone);
  } else {
    if (this._title == title) {
      this._on = false;
      $("#" + this._id).hide("slide", {}, 1000, onDone);
    } else {
      this._on = true;
      this._title = title;
      if (onDone) {
        onDone();
      }
    }
  }
}

SlidePanel.prototype.show = function(title, onDone) {
  if (!this._on) {
    this._on = true;
    this._title = title;
    $.log(this._id);
    
    $("#" + this._id).show("slide", {}, 1000, onDone);
  } else {
    if (onDone) {
      onDone();
    }
  }
}

SlidePanel.prototype.hide = function(title, onDone) {
  if (this._on) {
    this._on = false;
    $("#" + this._id).hide("slide", {}, 1000, onDone);
  } else {
    if (onDone) {
      onDone();
    }
  }
}
