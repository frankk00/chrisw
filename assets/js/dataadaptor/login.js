/*
  logindataadaptor.js
  
  Provide data for login view.
*/

function LoginDataAdaptor() {
  this.username = "guest";
  this.logined = false;
  this.view = null;
}

LoginDataAdaptor.prototype.setView = function(view) {
  this.view = view;
}

LoginDataAdaptor.prototype.fetchData = function(view, onDone, onError) {
  var current = this;
  
  function onFetchDataDone(result, para) {
    para.data.username = result.action.data.user.username;
    para.data.logined = true;
    
    onDone(para.view);
  }
  
  function onFetchDataError(error, para) {
    para.data.username = "guest";
    para.data.logined = false;
    
    onError(para.view, error);
  }
  
  JsonpQueue.get(
    "/u/profile",
    {},
    onFetchDataDone,
    onFetchDataError,
    {'view': view, 'data': this}
  );
}
