/*
  JsonpQueue.js
  
  Which could offer some low level access to the backend database.
*/
var JsonpQueue = {
  pendingCallIDs: {},
  callInProgress: 0, 
};

JsonpQueue.cancelAll = function() {
  JsonpQueue.pendingCallIDs = {};
};

JsonpQueue.queryOne = function(query, onDone, onError, debug) {
  var q = JSON.stringify({ ""})
};