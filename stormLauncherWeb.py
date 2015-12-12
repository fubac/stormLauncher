#!/usr/bin/env python

# Decpendencies: webpy and pyusb (1.0)
#
#  pyusb setup:
#  * install libusb (http://libusb.sourceforge.net/)
#  * download the pyusb package (http://pyusb.sf.net/)
#  * use pythons distutils to install:
#    $> python setup.py install
#  source: http://wiki.erazor-zone.de/wiki%3aprojects%3apython%3apyusb%3asetup%3alinux

######


import web # webpy
import usb.core # pyusb

launcherDev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
if launcherDev is None:
    raise ValueError('Launcher not found.')
if launcherDev.is_kernel_driver_active(0) is True:
    launcherDev.detach_kernel_driver(0)
launcherDev.set_configuration()

urls = (
    '/', 'index',
    '/cmd/up', 'turretUp',
    '/cmd/down', 'turretDown',
    '/cmd/left', 'turretLeft',
    '/cmd/right', 'turretRight',
    '/cmd/stop', 'turretStop',
    '/cmd/fire', 'turretFire',
)


app = web.application(urls, globals())

class index:
    def GET(self):
        return """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Rocket Launcher</title>
<script src="http://code.jquery.com/jquery-1.10.2.js"></script>
<style type="text/css">
#left {
    position: absolute;
    left: 0px;
    top: 20px;
    border-right: 20px solid black;
    border-top: 20px solid transparent;
    border-bottom: 20px solid transparent;
}
#right {
    position: absolute;
    left: 60px;
    top:  20px;
    border-left: 20px solid black;
    border-top: 20px solid transparent;
    border-bottom: 20px solid transparent;
}
#up {
    position: absolute;
    left: 20px;
    top: 0px;
    width: 0; 
    height: 0; 
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-bottom: 20px solid black;
}
#down {
    position: absolute;
    left: 20px;
    top: 60px;
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-top: 20px solid black;
}
#fire {
    position: absolute;
    left: 25px;
    top: 25px;
    border-radius: 100%;
    width: 30px;
    height: 30px;
    color:red;
    background:red;
}


</style>
</head>
<body>
<p id="left"/>
<p id="right"/>
<p id="up"/>
<p id="down"/>
<p id="fire"/>
<script>
call = function(cmd) {
   $.get( \""""+web.ctx.home+"""/cmd/"+cmd, function() {})
}
$( "#left" ).mouseup(function(){call("stop")} ).mousedown(function(){ call($(this).attr('id')) } );
$( "#right" ).mouseup(function(){call("stop")} ).mousedown(function(){ call($(this).attr('id')) } );
$( "#up" ).mouseup(function(){call("stop")} ).mousedown(function(){ call($(this).attr('id')) } );
$( "#down" ).mouseup(function(){call("stop")} ).mousedown(function(){ call($(this).attr('id')) } );
$( "#fire" ).mousedown(function(){ call($(this).attr('id')) } );
$( "body" ).keydown(function(event) {
    if(event.which == 37) {
      event.preventDefault();
      call('left');
    }
    if(event.which == 38) {
      event.preventDefault();
      call('up');
    }
    if(event.which == 39) {
      event.preventDefault();
      call('right');
    }
    if(event.which == 40) {
      event.preventDefault();
      call('down');
    }
    if(event.which == 13) {
      event.preventDefault();
      call('fire');
    }
});
$( "body" ).keyup(function(event) {
    if(event.which == 37 || event.which == 38 || event.which == 39 || event.which == 40 || event.which == 13) {
      event.preventDefault();
      call('stop');
    }
});

</script>
</body>
</html>
"""

class turretUp:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'up'

class turretDown:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'down'

class turretLeft:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'left'

class turretRight:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'right'

class turretStop:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'stop'

class turretFire:
    def GET(self):
        launcherDev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])
        return 'fire'

if __name__ == '__main__':
    app.run()
