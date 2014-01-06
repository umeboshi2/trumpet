<div class="admin-list-site-view">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <div class="listview-header">
    Layout Models
  </div>
  <div class="listview-list">
    <% route = 'admin_webviews' %>
    <% mkurl = request.route_url %>
    %for model in models:
    <% url = mkurl(route, context='viewmodel', id=model.id) %>
    <div class="listview-list-entry" id="entry-${model.id}">
      <span><a href="${url}">${model.name}</a></span>
      <div class="action-button delete-button" id="delete-${model.id}">
	Delete
      </div>
      <div class="delete-confirm" id="div-confirm-${model.id}">
	<strong>Confirm Deletion</strong>
	<div class="action-button confirm-button" id="confirm-${model.id}">
	  Confirm
	</div>
	<div class="action-button cancel-button" id="cancel-${model.id}">
	  Cancel
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>

