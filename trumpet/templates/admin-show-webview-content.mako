<% model = webview.model %>
<% mkurl = request.route_url %>
<% route = 'admin_webviews' %>
<input type="hidden" name="webview_id" value="${webview.id}"/>
<input type="hidden" name="model_id" value="${model.id}"/>
<div class="listview-header">
  <% url = mkurl(route, context='updatewebview', id=webview.id) %>
  View WebView <a href="${url}">${webview.name}</a>
</div>
<div class="listview-header">
  <% url = mkurl(route, context='viewmodel', id=model.id) %>
  Model: <a href="${url}">${model.name}</a> Fields
</div>
<div class="listview-list field-list">
  %for field in model.fields:
  <% field = field.field %>
  <div class="listview-entry">
    ${field.name} (${field.type})
  </div>
  %endfor
</div>
<div class="listview-header">
  Template ${webview.template.name}
  <div class="edit-template action-button pull-right">edit</div>
</div>
<div class="listview-list editing-space"></div>
<p>We need to use ace for text, html and teacup types.</p>
<div class="listview-header">
  <span> 
    <span class="attach-btn attach-css action-button pull-left">add</span>
    ${cssform.render()|n}
  </span>
</div>
<div class="listview-list">
  %for css in webview.css:
    <div class="listview-list-entry">
      ${css.css.name}
      <div class="action-button pull-right detach-css" data="${css.css_id}">detach</div>
    </div>
  %endfor
</div>
<div class="listview-header">
  <span> 
    <span class="attach-btn attach-js action-button pull-left">add</span>
    ${jsform.render()|n}
  </span>
</div>
<div class="listview-list">
  %for js in webview.js:
    <div class="listview-list-entry">
      ${js.js.name}
      <div class="action-button pull-right detach-js" data="${js.js_id}">detach</div>
    </div>
  %endfor
</div>
