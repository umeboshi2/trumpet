<input type="hidden" name="model_id" value="${model.id}"/>
<div class="listview-header">
  View Model ${model.name}
</div>
<div class="listview-header">
  Fields
  <div class="action-button pull-right add-field-button">add field</div>
</div>
<div class="listview-list field-list">
  %for field in model.fields:
  <% field = field.field %>
  <div class="listview-entry">
    ${field.name} (${field.type})
    <span class="field-buttons">
      <div class="action-button delete-button" id="delete-${field.id}" field-type="${field.type}">delete</div>
      <div class="action-button edit-button" id="edit-${field.id}" field-type="${field.type}">edit</div>
    </span>
  </div>
  %endfor
</div>
<div class="listview-list editing-space"></div>
<p>We need to use ace for text, html and teacup types.</p>
