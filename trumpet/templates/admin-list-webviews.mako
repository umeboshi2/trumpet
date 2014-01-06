<div class="admin-list-site-view">
  <div class="listview-header">
    Web Views
    <div class="action-button pull-right add-webview-button">add webview</div>
  </div>
  <div class="listview-list">
    <% route = 'admin_webviews' %>
    <% mkurl = request.route_url %>
    <% models = [] %>
    %for webview in webviews:
    <% url = mkurl(route, context='showwebview', id=webview.id) %>
    <div class="listview-list-entry" id="entry-${webview.id}">
      <span><a href="${url}">${webview.name}</a></span>
      <div class="action-button delete-button" id="delete-${webview.id}">
	Delete
      </div>
      <div class="delete-confirm" id="div-confirm-${webview.id}">
	<strong>Confirm Deletion</strong>
	<div class="action-button confirm-button" id="confirm-${webview.id}">
	  Confirm
	</div>
	<div class="action-button cancel-button" id="cancel-${webview.id}">
	  Cancel
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>

