<div class="imagelist-viewfeed">
  <div class="imagelist-header">
    <p>Images in database</p>
  </div>
  <div class="imagelist-list">
    %for image in images:
    <div class="imagelist-entry">
      <% url = request.route_url('blob', filetype='image', id=image.id) %>
      <% thurl = request.route_url('blob', filetype='thumb', id=image.id) %>
      <p><a class="imagelist-entry-name" href="${url}">${image.name}</a></p>
      <div class="imagelist-entry-image">
	<img src="${thurl}">
      </div>
      <div class="imagelist-delete-image" id="${image.id}">
	<% delurl = request.route_url('admin_images', context='delete', id=image.id) %>
	<input type="hidden" value="${delurl}" id="delurl-${image.id}">
	Delete
      </div>
    </div>
    %endfor
  </div>
</div>
