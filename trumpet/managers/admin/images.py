from cStringIO import StringIO
from datetime import datetime

import transaction
from PIL import Image

from trumpet.models.sitecontent import SiteImage



    
class ImageManager(object):
    def __init__(self, session):
        self.session = session
        self.thumbnail_size = 128, 128
        
    def images_query(self):
        return self.session.query(SiteImage)

    def make_thumbnail(self, content):
        imgfile = StringIO(content)
        img = Image.open(imgfile)
        img.thumbnail(self.thumbnail_size, Image.ANTIALIAS)
        outfile = StringIO()
        img.save(outfile, 'JPEG')
        outfile.seek(0)
        thumbnail_content = outfile.read()
        return thumbnail_content
    
    def add_image(self, name, fileobj):
        content = fileobj.read()
        with transaction.manager:
            image = SiteImage(name, content)
            image.thumbnail = self.make_thumbnail(content)
            self.session.add(image)
        return self.session.merge(image)
    
    def delete_image(self, id):
        with transaction.manager:
            image = self.session.query(SiteImage).get(id)
            self.session.delete(image)

    

        
