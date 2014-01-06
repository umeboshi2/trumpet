<div class="facebook-friends">
  <div class="facebook-friends-header">
    <p>Friends</p>
  </div>
  <div class="facebook-friends-list">
    <% longnames = [] %>
    <% shortnames = [] %>
    %for friend in people:
        %if len(friend.name) > 20:
            <% longnames.append(friend) %>
        %else:
            <% shortnames.append(friend) %>
        %endif
    %endfor
    %for friend in shortnames + longnames:
    <div class="facebook-friends-entry">
	<img id="${'fbfriend-%d' % friend.id}" src="${'https://graph.facebook.com/%d/picture' % friend.id}"><br>
	<a class="facebook-friends-entry-name" href="#">${friend.name}</a>
      <div class="facebook-friends-entry-content">
      </div>
    </div>
    %endfor
  </div>
</div>
