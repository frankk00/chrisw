/*
 * Topic .js
 * 
 * Created by Kang Zhang  2010-10-10
 *
 * (c) Copyright 2010 Kang Zhang. All Rights Reserved. 
 */
 
$(document).ready(function()
{
  $("ol.topics > li").click(function(event){
    var $target = $(event.currentTarget);
    var topic_url = "/group/topic/" + $target.attr('data-topic-id');
    // alert("url " + topic_url)
    window.location.replace(topic_url);
  })
})