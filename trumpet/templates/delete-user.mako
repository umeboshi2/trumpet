<div class="delete-user-container">
  <p>Really delete user?</p>
  <div class="delete-user-button" id="${id}">
    <% url = request.route_url('admin_users', context='confirmdelete', id=id) %>
    <input type="hidden" name="deleteurl" value="${url}" id="deleteurl">
    Confirm
  </div>
</div>
