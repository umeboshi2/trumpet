<div class="delete-image-container">
  <p>Really delete image?</p>
  <div class="delete-image-button" id="${id}">
    <% url = request.route_url('admin_images', context='confirmdelete', id=id) %>
    <input type="hidden" name="deleteurl" value="${url}" id="deleteurl">
    Confirm
  </div>
  <div>
    <img src="${image_url}">
  </div>
</div>
