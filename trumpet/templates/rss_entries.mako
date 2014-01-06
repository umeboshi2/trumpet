<div class="rssviewer-viewfeed">
  <div class="rssviewer-viewfeed-header">
    <p>Feed: ${feed.name}.</p>
  </div>
  <div class="rssviewer-viewfeed-list">
    %for entry in rss.content.entries:
    <div class="rssviewer-viewfeed-entry">
      <p><a class="rssviewer-viewfeed-entry-link" href="${entry.link}">${entry.title}</a></p>
      <div class="rssviewer-viewfeed-entry-content">
	%if 'content' in entry:
	${entry.content|n}
	%elif 'summary' in entry:
	${entry.summary|n}
	%endif
      </div>
    </div>
    %endfor
  </div>
</div>
