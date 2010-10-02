/*
  JsonpQueue.js
  
  Which could offer some low level access to the backend database.
*/
var JsonpQueue = {
  pendingCalls: {},
  callInProgress: 0, 
};

JsonpQueue.cancelAll = function() {
  JsonpQueue.pendingCalls = {};
};

JsonpQueue.get = function(url, paras, onDone, onError, morePara) {
  var callbackID = new Date().getTime() + "x" + Math.floor(Math.random() * 1000);
  JsonpQueue.pendingCalls.callbackID = {
    doneHandler: onDone,
    errorHandler: onError    
  };
  
  url += (url.indexOf("?") < 0 ? "?" : "&") + "result_type=json";
  
  for (var i in paras) {
    url += "&" + i + "=" + paras[i];
  }
  
  $.get(
    url,
    function(data) {
      if (JsonpQueue.pendingCalls.callbackID) {
        try {
          var result = jQuery.parseJSON(data);
          if (result.status == "ok") {
            if (morePara) {
              JsonpQueue.pendingCalls.callbackID.doneHandler(result, morePara);
            } else {
              JsonpQueue.pendingCalls.callbackID.doneHandler(result);
            }
          } else {
            if (morePara) {
              JsonpQueue.pendingCalls.callbackID.errorHandler(result, morePara);
            } else {
              JsonpQueue.pendingCalls.callbackID.errorHandler(result);
            }
          }
        } catch(e) {
          if (morePara) {
            JsonpQueue.pendingCalls.callbackID.errorHandler(e, morePara);
          } else {
            JsonpQueue.pendingCalls.callbackID.errorHandler(e);
          }
        }
        //delete JsonpQueue.pendingCalls.callbackID;
      }
    }
  );
}

JsonpQueue.post = function(url, paras, onDone, onError) {
  var callbackID = new Date().getTime() + "x" + Math.floor(Math.random() * 1000);
  JsonpQueue.pendingCalls.callbackID = {
    doneHandler: onDone,
    errorHandler: onError    
  };
  
  url += (url.indexOf("?") < 0 ? "?" : "&") + "result_type=json";
  
  $.post(
    url,
    paras,
    function(data) {
      if (JsonpQueue.pendingCalls.callbackID) {
        try {
          var result = jQuery.parseJSON(data);
          if (result.status == "ok") {
            JsonpQueue.pendingCalls.callbackID.doneHandler(result);
          } else {
            JsonpQueue.pendingCalls.callbackID.errorHandler(result);
          }
        } catch(e) {
          JsonpQueue.pendingCalls.callbackID.errorHandler(e);
        }
        //delete JsonpQueue.pendingCalls.callbackID;
      }
    }
  );
};