import web
import RPi.GPIO as GPIO
import time

urls = (
  '/', 'index',
  '/launch/(\d+)', 'launch',
  '/i', 'inh',
  '/u', 'unh'
)

t_globals = {
  'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)

class index:
  def GET(self):
    return render.index()

class launch:
  def POST(self, id):
    fire(int(id))
    raise web.seeother('/')

class inh:
  def GET(self):
    inhibit(0)
    raise web.seeother('/')

class unh:
  def GET(self):
    uninhibit(0)
    raise web.seeother('/')

def fire(num):
  r=0
  if num > 15:
    r=1
  if num > 31:
    r=2
  signal(num-r*16, r,  GPIO.HIGH)
  uninhibit(r)
  time.sleep(3)
  inhibit(r)
  signal(num-r*16, r, GPIO.LOW)
  return

def signal(num, r, level):
  print "signal num="+str(num)+" range="+str(r)
  pin = [[5,7,8,10],[12,13,15,16],[19,21,22,23]]
  o="Firing pins:"
  if num & 1:
    GPIO.output(pin[r][0], level)
    o+=" "+str(pin[r][0])
  if num & 2:
    GPIO.output(pin[r][1], level)
    o+=" "+str(pin[r][1])
  if num & 4:
    GPIO.output(pin[r][2], level)
    o+=" "+str(pin[r][2])
  if num & 8:
    GPIO.output(pin[r][3], level)
    o+=" "+str(pin[r][3])
  print o
  return

def uninhibit(r):
  pin=[3, 11, 18]
  GPIO.output(pin[r], GPIO.LOW)
  return

def inhibit(r):
  pin=[3, 11, 18]
  GPIO.output(pin[r], GPIO.HIGH)
  return

def setup():
  pin = [5,7,8,10,12,13,15,16,19,21,22,23,3,11,18]
  GPIO.setmode(GPIO.BOARD)
  for index in range(len(pin)):
    print(pin[index])
    GPIO.setup(pin[index], GPIO.OUT)
    GPIO.output(pin[index], GPIO.LOW)
  inhibit(0)
  inhibit(1)
  inhibit(2)
  return

def cleanup():
  GPIO.cleanup()
  return

setup()

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()
