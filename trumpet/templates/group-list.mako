<div class="grouplist-viewfeed">
  <div class="grouplist-header">
    <p>Groups in database</p>
  </div>
  <div class="grouplist-list">
    %for group in groups:
    <div class="grouplist-entry">
      <% vurl = request.route_url('admin_users', context='viewgroup', id=group.id) %>
      <p><a class="grouplist-entry-name" href="${vurl}">${group.name}</a></p>
      <div class="grouplist-delete-group" id="${group.id}">
	<% delurl = request.route_url('admin_users', context='delete', id=group.id) %>
	<input type="hidden" value="${delurl}" id="delurl-${group.id}">
	Delete
      </div>
    </div>
    %endfor
  </div>
</div>
