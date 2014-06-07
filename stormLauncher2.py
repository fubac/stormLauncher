#!/usr/bin/env python

#  pyusb setup:
#  * install libusb
#  * download the pyusb package
#  * use pythons distutils to install:
#    $> python setup.py install
#  source: http://wiki.erazor-zone.de/wiki%3aprojects%3apython%3apyusb%3asetup%3alinux

######


import web
import usb.core # pyusb

launcherDev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
if launcherDev is None:
    raise ValueError('Launcher not found.')
if launcherDev.is_kernel_driver_active(0) is True:
    launcherDev.detach_kernel_driver(0)
launcherDev.set_configuration()

urls = (
    '/cmd/up', 'turretUp',
    '/cmd/down', 'turretDown',
    '/cmd/left', 'turretLeft',
    '/cmd/right', 'turretRight',
    '/cmd/stop', 'turretStop',
    '/cmd/fire', 'turretFire',
)

app = web.application(urls, globals())

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
