import os
from flask import *
import uuid


class upload:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self):
        pass

    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def removeUploadIdFilme(self, uploadFolder, filename):
        try:
            if (filename):
                os.unlink(os.path.join(uploadFolder, filename))
        except (Exception) as error:
            flash("Ocorreu algum erro na remoção do arquivo", "error")
            print(error)
            return error
        finally:
            return

    def upload(self, uploadFolder):
        file = request.files['file']

        if file and upload().allowed_file(file.filename):
            filename = "%s.%s" % (self.formatName(),
                                  self.extension(file.filename))
            osPathJoin = os.path.join(uploadFolder, filename)
            file.save(osPathJoin)
            return filename

    def extension(self, filename):
        return filename.split('.')[-1].lower()

    def formatName(self):
        return uuid.uuid4()
