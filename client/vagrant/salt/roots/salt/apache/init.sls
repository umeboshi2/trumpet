# -*- mode: yaml -*-

apache2:
  pkg:
    - latest
  service:
    - running
    - watch:
      - file: /etc/apache2/default.wsgi
      - file: /etc/apache2/sites-enabled/default

/etc/apache2/default.wsgi:
  file.managed:
    - source: salt://apache/default.wsgi
    - user: root
    - group: root
    - mode: 755

/etc/apache2/sites-enabled/default:
  file.managed:
    - source: salt://apache/default-site
    - user: root
    - group: root
    - mode: 644

date > /tmp/started_apache:
  cmd:
    - wait
    - watch:
      - service: apache2



    
