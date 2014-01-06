<div class="facebook-newsfeed">
  <div class="facebook-newsfeed-header">
    <p>News Feed</p>
  </div>
  <div class="facebook-newsfeed-list">
    %for post in posts:
    <% post = post.content %>
    <div class="facebook-newsfeed-entry">
      <p>
	<img src="${'https://graph.facebook.com/%d/picture' % int(post['from']['id'])}">
	<a class="facebook-newsfeed-entry-name" href="#">${post['from']['name']}</a>
      </p>
      <div class="facebook-newsfeed-entry-content">
	%if 'message' in post:
	    ${post['message']}
	%else:
	    KEYS:--${post.keys()}
	%endif
      </div>
    </div>
    %endfor
  </div>
</div>
