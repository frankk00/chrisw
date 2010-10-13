/*
 * Topic .js
 * 
 * Created by Kang Zhang  2010-10-10
 *
 * (c) Copyright 2010 Kang Zhang. All Rights Reserved. 
 */
 
$(document).ready(function()
{
  // add hooks for all topic items
  $("ol.topics > li").click(function(event){
    var $target = $(event.currentTarget);
    var topic_url = "/group/topic/" + $target.attr('data-topic-id');
    // window.location.replace(topic_url);
    window.location = (topic_url);
  })
})