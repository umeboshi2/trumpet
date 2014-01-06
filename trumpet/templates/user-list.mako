<div class="userlist-viewfeed">
  <div class="userlist-header">
    <p>Users in database</p>
  </div>
  <div class="userlist-list">
    %for user in users:
    <div class="userlist-entry">
      <% vurl = request.route_url('admin_users', context='view', id=user.id) %>
      <p><a class="userlist-entry-name" href="${vurl}">${user.username}</a></p>
      <div class="userlist-delete-user" id="${user.id}">
	<% delurl = request.route_url('admin_users', context='delete', id=user.id) %>
	<input type="hidden" value="${delurl}" id="delurl-${user.id}">
	Delete
      </div>
    </div>
    %endfor
  </div>
</div>
