from time import sleep
from os import popen
import sys, os, re, web
lasttitle = ""
i = 1

if(os.popen("ls | grep 'static'").read() == ""):
    os.system("mkdir static")

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if(len(sys.argv) > 1):
    try:
        port = int(sys.argv[1])
    except:
        port = 8080
else:
    port = 8080
    
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

urls = (
    '/(.*)', 'hello'
)

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

class hello:
    def GET(self, name):
        yield open(resource_path("page.html"), "r").read().replace("<!--STYLE-->", f"<style>\n{open(resource_path('styles.css'), 'r').read()}\n</style>").replace("<!--CODE-->", f"<script>\n{open(resource_path('code.js'), 'r').read()}\n</script>")
        while True:     
            global lasttitle
            global i
            try:
                artist = deEmojify(popen("playerctl metadata | grep ':artist'").read().split("              ")[1].split('\n')[0])
            except:
                artist = "Not found..."
            try:
                song = deEmojify(popen("playerctl metadata | grep ':title'").read().split("              ")[1].split('\n')[0])
            except:
                song = "Not playing..."
                
            try:
                cover = popen("playerctl metadata | grep ':artUrl'").read().split("              ")[1].split('\n')[0]
            except:
                cover = os.getcwd() + "/placeholder.png"
            
            if(lasttitle != song):
                lasttitle = song
                db = '\\'
                os.system(f"cp {cover.replace('file://', '').replace(' ', db)} static/cover.{cover.split('.')[len(cover.split('.')) - 1]}")
                cover = "cover." + cover.split('.')[len(cover.split('.')) - 1]
                yield f"\n<script>$('img#trackart').attr('src', 'static/{cover}?t={str(i)}');$('script')[$('script').length - 1].remove()</script>"
                i = i + 1
                
            yield f"\n<script>setSong('{artist}','{song}');$('script')[$('script').length - 1].remove()</script>"                
            sleep(.5)

if __name__ == "__main__":
    app.run(port=port)