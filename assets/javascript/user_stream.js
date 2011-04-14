

$(document).ready(function()
{
  $(".user_stream_actions .reply_action").click(function(event){
    var target = $(event.currentTarget).parents(".user_stream_item");
    var streamText = target.find(".stream_text").text().trim()
    var authorName = target.attr('author-username')

    template = chrisw.templates.user_stream_reply
    view = { content: "@" + authorName + " "}
    dialog = chrisw.render(template, view)

    $(".chrisw_dialog_content").dialog('close')
    $(dialog).dialog({width:500, resizable:false, title: "Reply to @" + authorName, dialogClass: "chrisw_dialog"})

    return false;
  })


  $(".user_stream_actions .retweet_action").click(function(event){
    var target = $(event.currentTarget).parents(".user_stream_item");
    var streamText = target.find(".stream_text").text().trim()
    var authorName = target.attr('author-username')

    template = chrisw.templates.user_stream_reply
    view = { content: " RT @" + authorName + ": " + streamText}
    dialog = chrisw.render(template, view)

    $(".chrisw_dialog_content").dialog('close')
    $(dialog).dialog({width:500, resizable:false, title: "Retweet to @" + authorName, dialogClass: "chrisw_dialog"})

    return false;
  })


})