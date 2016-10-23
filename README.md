# all1input
hacked together minimal software kvm for linux host, linux/win/osx clients

## Assumptions
You are using evdev with a bluetooth or usb hid on a linux host, with 1 screen per client computer.

I also assume you have some technical know-how. At this time I do not have time or energy to write a decent readme.

## Features
* ssl certs for encryption and authentication
* configurable mouse acceleration
* stability (it does not go down easily, no freezes observed so far)

## Known Bugs
* if no physical mouse is connected to a windows client, the cursor remains invisible but works otherwise
* doubleclick in osx only works for a few select applications because of a missing click count, hint: (Quartz.CGEventSetIntegerValueField(mouseEvent, Quartz.kCGMouseEventClickState, num))
* after a resolution change in osx, the mouse cursor can only move horizontally (bug in xcode?)
* keyboards connected to the linux host are stuck in numlock mode

## Todo
* hide cursor on screen exit (wishful thinking? windows does not allow global mouse cursor visibility control)
* transfer keystate at screen enter
* daemonize / make taskbar app
* make proper package

## Planned Features
* implement media keys
* support multiple screens per client
* chord typing
* speech recognition relay
* client side hotkeys
* deebouncing for broken keys and switches, also accessibility
* mouse accessibility mode: restrict axes
