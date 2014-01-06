<div class="admin-list-site-view">
  <% dtformat = '%b %d %Y - %H:%M:%S' %>
  <% timeformat = '%I:%M %p' %>
  <div class="listview-header">
    Layout Fields
  </div>
  <div class="listview-list">
    <% route = 'admin_webviews' %>
    <% mkurl = request.route_url %>
    %for field in fields:
    <div class="listview-list-entry" id="entry-${field.id}">
      <span>${field.name}  (${field.type})</span>
      <div class="action-button delete-button" id="delete-${field.id}">
	Delete
      </div>
      <div class="delete-confirm" id="div-confirm-${field.id}">
	<strong>Confirm Deletion</strong>
	<div class="action-button confirm-button" id="confirm-${field.id}">
	  Confirm
	</div>
	<div class="action-button cancel-button" id="cancel-${field.id}">
	  Cancel
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>

