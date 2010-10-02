function login(username, password, onDone, onError) {
  
  function onDone1(data) {
    onDone();
  }
  
  function onError1(error) {
    onError();
  }
  JsonpQueue.post(
    "/login",
    {
      'username': username,
      'password': password,
      'back_url': "/"
    },
    onDone1,
    onError1
  )
}

function logout(onDone, onError) {
  function onDone1(data) {
    onDone();
  }
  
  function onError1(error) {
    onError();
  }
  
  JsonpQueue.get(
    "/logout",
    {},
    onDone1,
    onError1
  )
}