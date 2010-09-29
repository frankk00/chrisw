/*
  group.js
  
  Standard group view
*/

function GroupView(data) {
  this.data = data;
  this._div = null;
}

GroupView.prototype.installUI = function(div) {
  this._div = div;
  this._installGroupInfo();
  this._installTopic(0);
}

GroupView.prototype.unInstallUI = function() {
  if (this._div) {
    this._div.innerHTML = "";
    this._div = null;
  }
}

GroupView.prototype._installGroupInfo = function() {
  var info = document.createElement("div");
  info.setAttribute("class", "group-info-panel");
  this._div.appendChild(info);
  
  info.innerHTML = 
  "<table><tbody><tr><td id='group-title' class='group-title' width='60%'>"
  + this.data.group.title + "</td><td class='group-owner' width='10%'>" 
  + this.data.group.create_user.username 
  + "</td><td class='group-command' width='30%'>" 
  + "<a class='ui-corner-all bottom-button' id='button' href='#' onclick=''>Join it</a> &nbsp;" 
  + "<a class='ui-corner-all bottom-button' id='button' href='#' onclick=''>Introduce to others</a>" + "</td></tr></tbody></table>";
}

GroupView.prototype._installTopic = function(id) {
  if (id < this.data.topics.length) {
    var topic = document.createElement("div");
    this._div.appendChild(topic);
    topic.setAttribute("class", "group-topic-panel");
    topic.innerHTML = "<div class='group-topic-panel'>"
    + "<div class='group-topic-header-panel'>" + this.data.topics[id].title + "</div>"
    + "<div class='group-topic-content-panel'>" + this.data.topics[id].content + "</div>"
    + "</div><hr />";
    
    this._installTopic(id + 1);
  }
}
