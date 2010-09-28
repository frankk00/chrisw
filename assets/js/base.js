$(window).ready(function() {
  
  $("#login").dialog({
    disabled: true,
    modal: true,
    position: 'center',
    minHeight: 150,
    minWidth: 400,
    buttons: {
      Login: function() {
        $.post(
          "/login?result_type=json",
          {
            uid: $("#id_uid").val(),
            password: $("#id_password").val(),
            back_url: "/",
          },
          function(data) {
            var result = jQuery.parseJSON(data);
            if (result.redirect) {
              document.location = result.redirect;
            }
            alert("data load: " + data);
          }
        );
      },
      Cancel: function() {
        $(this).dialog('close');
      }
    }
  });
  $("#login").dialog('close');
  
  $("#login_span").click(function() {
    loadLoginPart();
    $("#login").dialog('open');
  })
  
  
  $("#logout_span").click(function() {
    $.post(
      "/logout?result_type=json",
      function(data) {
        alert("data load: " + data);
        location.reload();
      }
    );
  })
  
})

function loadLoginPart() {
  $("#login")[0].innerHTML = '<table border="0" cellspacing="5" cellpadding="5"><tbody><tr><th><label for="id_uid">Uid:</label></th><td><input type="text" name="uid" id="id_uid"></td></tr> <tr><th><label for="id_password">Password:</label></th><td><input type="text" name="password" id="id_password"></td></tr>    		</tbody></table>';
}

