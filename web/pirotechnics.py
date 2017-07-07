import web
import time
from demux import Demux

urls = (
  '/', 'index',
  '/launch/(\d+)', 'launch'
)

t_globals = {
  'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)

demultiplexer = [
  Demux(3, [5,7,8,10]),
  Demux(11, [12,13,15,16]),
  Demux(18, [19,21,22,23])
]

class index:
  def GET(self):
    return render.index()

class launch:
  def POST(self, id):
    fire(int(id))
    raise web.seeother('/')

def fire(num):
  r = num/16
  d = demultiplexer[r]
  d.signal(num-r*16)
  d.uninhibit()
  time.sleep(3)
  d.inhibit()
  d.reset()

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()
