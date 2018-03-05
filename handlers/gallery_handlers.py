from handlers.base_handler import BaseHandler


class GalleryHandler(BaseHandler):
    def get(self):
        return self.render_template("gallery.html")
