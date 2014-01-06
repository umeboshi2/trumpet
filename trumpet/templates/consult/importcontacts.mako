<div class="contacts-import">
  <% r = 'consult_contacts' %>
  <% kw = dict(context='importsubmit', id='somebody') %>
  <% url = request.route_url(r, **kw) %>
  <form action="${url}" method="post" accept-charset="utf-8"
	enctype="multipart/form-data">
    <label for="vcf">VCF</label>
    <input id="vcf" name="vcf" type="file" value=""/>
    <input type="submit" value="submit" />
  </form>
</div>

