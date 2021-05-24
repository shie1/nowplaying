from time import sleep
from os import popen
import sys, os, re, web

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
            status1 = popen("playerctl status").read().replace("\n","")
            sleep(1)
            status2 = popen("playerctl status").read().replace("\n","")
            
            try:
                artist = deEmojify(popen("playerctl metadata | grep ':artist'").read().split("              ")[1].replace('\n', ""))
            except:
                artist = "Not found..."
            try:
                song = deEmojify(popen("playerctl metadata | grep ':title'").read().split("              ")[1].replace('\n', ""))
            except:
                song = "Not playing..."
                
            try:
                cover = deEmojify(popen("playerctl metadata | grep ':art'").read().split("              ")[1].replace('\n', ""))
            except:
                cover = "https://i.pinimg.com/originals/ad/be/5f/adbe5f762b5a61c1024223ccb260786d.png"
                
            yield f"\n<script>setCover({cover});$('script')[$('script').length - 1].remove()</script>"
                            
            if((status1 == "Stopped") or (status1 == "Paused")) and (status1 == status2):
                yield "\n<script>$('body').fadeOut('slow');$('script')[$('script').length - 1].remove()</script>"
            else:
                yield "\n<script>$('body').fadeIn('fast2');$('script')[$('script').length - 1].remove()</script>"
                
            yield f"\n<script>setSong('{artist}','{song}');$('script')[$('script').length - 1].remove()</script>"                
            sleep(.5)

if __name__ == "__main__":
    app.run(port=port)