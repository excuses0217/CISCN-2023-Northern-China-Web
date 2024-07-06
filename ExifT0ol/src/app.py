import web
import os
import exifread

web.config.debug = False

urls = (
    '/', 'Index',
    '/upload', 'Upload',
    '/exifhandler', 'ExifHandler'
)

app = web.application(urls, locals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'filename': '', 'filedir': '', 'exif': {}})

class Index:
    def GET(self):
        return render.upload()


class Upload:
    def GET(self):
        return render.upload()

    def POST(self):
        params = web.input(file={})
        filedir = 'uploads/'

        if 'file' in params:
            filename = params['file'].filename
            fileext = filename.split('.')[-1]
            if fileext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
                print('Warning: only allow jpg, jpeg, png, gif!')

            session.filename = filename
            session.filedir = filedir

            fout = open(filedir + filename, 'wb')
            fout.write(params['file'].value)
            fout.close()
            
            return "<script>alert('successfully uploaded');window.location.href='/exifhandler'</script>"
        else:
            return 'no file'


class ExifHandler:
    def GET(self):
        if session.filename != '' and session.exif == {}:
            with open(session.filedir + session.filename, 'rb') as f:
                    tags = exifread.process_file(f)

            exif_info = {}
            for tag, value in tags.items():
                if tag.startswith('EXIF'):
                    exif_info[tag] = str(value)

            session.exif = exif_info
            return render.result(filename=session.filename, exif_info=exif_info)
        elif session.filename == '' and session.exif == {}:
            return "<script>alert('no file uploaded');window.location.href='/'</script>"
        else:
            return render.result(filename=session.filename, exif_info=session.exif)


if __name__ == '__main__':
    app.run()
