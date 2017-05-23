#!/usr/bin/python
#encoding: utf-8

import cStringIO
from flup.server.fcgi import WSGIServer
from PIL import Image, ImageFont, ImageDraw

#CGI server bind address
bindaddr = '127.0.0.1'
#CGI server bind port, should be the same as configured in nginx
bindport = 3456
#Absolute path to font
fontpath = '/path/to/your/font.ttf'
#Image size
imgsize = 144
#Font size
fontsize = 100


def imgapi(environ, start_response):
    url = environ['PATH_INFO'].decode('utf-8')
    splitted = url.split('/')
    if len(splitted) != 4:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'Invalid request!'
    #print 'listsize:', len(splitted)
    #print 'fgcol:', splitted[1]
    #print 'bgcol:', splitted[2]
    #print 'char:', splitted[3]
    fgcol = splitted[1].strip()
    if len(fgcol) != 6:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'Error: Invalid request!'
    bgcol = splitted[2].strip()
    if len(bgcol) != 6:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'Error: Invalid request!'
    r, g, b = bgcol[:2], bgcol[2:4], bgcol[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    if len(splitted) != 4:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'Error: Invalid request!'
    font = ImageFont.truetype(fontpath, 100)
    w, h = font.getsize(splitted[3])
    img = Image.new('RGB', (imgsize, imgsize), (r, g, b))
    draw = ImageDraw.Draw(img)
    fgcol = '#' + fgcol
    draw.text(((imgsize-w)/2, (imgsize-h)/2), splitted[3], font=font, fill=fgcol)
    buf = cStringIO.StringIO()
    img.save(buf, format="PNG")
    start_response('200 OK', [('Content-Type', 'image/png')])
    return buf.getvalue()


if __name__ == '__main__':
    WSGIServer(imgapi, bindAddress=(bindaddr, bindport)).run()
