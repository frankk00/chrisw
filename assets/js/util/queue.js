/*
  JsonpQueue.js
  
  Which could offer some low level access to the backend database.
*/
$.debug(true);

var JsonpQueue = {
  pendingCalls: {},
  callInProgress: 0, 
};

JsonpQueue.cancelAll = function() {
  JsonpQueue.pendingCalls = {};
};

JsonpQueue.call = function(url, paras, onDone, onError, debug) {
  var callbackID = new Date().getTime() + "x" + Math.floor(Math.random() * 1000);
  JsonpQueue.pendingCalls.callbackID = {
    doneHandler: onDone,
    errorHandler: onError    
  };
  
  url += (url.indexOf("?") < 0 ? "?" : "&") + "result_type=json";
  
  $.post(
    "/login?result_type=json",
    paras,
    function(data) {
      if (JsonpQueue.pendingCalls.callbackID) {
        var result = jQuery.parseJSON(data);
        if (result.status == "ok") {
          JsonpQueue.pendingCalls.callbackID.doneHandler(result.result);
        } else {
          JsonpQueue.pendingCalls.callbackID.errorHandler(result.error)
        }
      }
    }
  );
};