(function($){
  $.fn.twitterTimeline = function(){
    var th = this;
    $.ajax({
      url: 'http://127.0.0.1:5000/_tweets/',
      dataType: 'json',
      beforeSend: function() {
        $(th).addClass('loader');
      }
    }).done(function(data) {
      $(th).removeClass('loader');
      prepareTweetBlock(data);
    });
    prepareTweetBlock = function(data) {
      var container = document.createElement('div');
      container.className = "tweet-container vertical-only";

      for(t in data.timeline) {
        var tweet = document.createElement('div');
        tweet.className = "tweet";

        var tweetText = document.createElement('div');
        tweetText.className = "text";
        tweetText.innerText = data.timeline[t].text;

        tweet.appendChild(tweetText);
        container.appendChild(tweet);
      }
      $(th).append(container);
      //init jScrollPane
      $(container).jScrollPane();
    };
    linkify = function(txt) {
      prepareUrl = function(url) {
        var full_url = url;
        if (!full_url.match('^https?:\/\/')) {
          full_url = 'http://' + full_url;
        }
        return '<a target="_blank" href="' + full_url + '">' + url + '</a>';
      };
      txt = txt.replace(/((https?\:\/\/)|(www\.))(\S+)(\w{2,4})(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/gi, prepareUrl);
      return txt;
    };
  };
})(jQuery);
