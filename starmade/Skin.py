import zipfile

skin_body_name = "skin_main_diff.png"
skin_body_em_name = "skin_main_em.png"
skin_helmet_name = "skin_helmet_diff.png"
skin_helmet_em_name = "skin_helmet_em.png"

class Skin:
    _body = None
    _body_em = None
    _helmet_texture = None
    _helmet = None
    
    def __init__(
            self,
            body = None,
            body_em = None,
            helmet = None,
            helmet_em = None
            ):
        
        # get the default textures and hard-code so they are
        # used in the event none are supplied...
        self._body = body
        self._body_em = body_em
        self._helmet = helmet
        self._helmet_em = helmet_em

    def compile(self, filename):
        zipper = zipfile.ZipFile(
            filename,
            mode="w",
            compression = zipfile.ZIP_DEFLATED,
            allowZip64 = False
            )
        
        zipper.write(self._body, skin_body_name)
        zipper.write(self._body_em, skin_body_em_name)
        zipper.write(self._helmet, skin_helmet_name)
        zipper.write(self._helmet_em, skin_helmet_em_name)

        zipper.close()
