"""
Keys that are implemented.

Taken from linux/input.h

This lists all key names, the ones that every os module should have implemented
are uncommented.
"""

#*
#* Keys and buttons
#*
#* Most of the keys/buttons are modeled after USB HUT 1.12
#* (see http://www.usb.org/developers/hidpage).
#* Abbreviations in the comments:
#* AC - Application Control
#* AL - Application Launch Button
#* SC - System Control
#*/
KEY_NAMES = (
    # "KEY_RESERVED",
    "KEY_ESC",
    "KEY_1",
    "KEY_2",
    "KEY_3",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_0",
    "KEY_MINUS",
    "KEY_EQUAL",
    "KEY_BACKSPACE",
    "KEY_TAB",
    "KEY_Q",
    "KEY_W",
    "KEY_E",
    "KEY_R",
    "KEY_T",
    "KEY_Y",
    "KEY_U",
    "KEY_I",
    "KEY_O",
    "KEY_P",
    "KEY_LEFTBRACE",
    "KEY_RIGHTBRACE",
    "KEY_ENTER",
    "KEY_LEFTCTRL",
    "KEY_A",
    "KEY_S",
    "KEY_D",
    "KEY_F",
    "KEY_G",
    "KEY_H",
    "KEY_J",
    "KEY_K",
    "KEY_L",
    "KEY_SEMICOLON",
    "KEY_APOSTROPHE",
    "KEY_GRAVE",
    "KEY_LEFTSHIFT",
    "KEY_BACKSLASH",
    "KEY_Z",
    "KEY_X",
    "KEY_C",
    "KEY_V",
    "KEY_B",
    "KEY_N",
    "KEY_M",
    "KEY_COMMA",
    "KEY_DOT",
    "KEY_SLASH",
    "KEY_RIGHTSHIFT",
    "KEY_KPASTERISK",
    "KEY_LEFTALT",
    "KEY_SPACE",
    "KEY_CAPSLOCK",
    "KEY_F1",
    "KEY_F2",
    "KEY_F3",
    "KEY_F4",
    "KEY_F5",
    "KEY_F6",
    "KEY_F7",
    "KEY_F8",
    "KEY_F9",
    "KEY_F10",
    "KEY_NUMLOCK",
    "KEY_SCROLLLOCK",
    "KEY_KP7",
    "KEY_KP8",
    "KEY_KP9",
    "KEY_KPMINUS",
    "KEY_KP4",
    "KEY_KP5",
    "KEY_KP6",
    "KEY_KPPLUS",
    "KEY_KP1",
    "KEY_KP2",
    "KEY_KP3",
    "KEY_KP0",
    "KEY_KPDOT",

    # "KEY_ZENKAKUHANKAKU",
    # "KEY_102ND",
    "KEY_F11",
    "KEY_F12",
    # "KEY_RO",
    # "KEY_KATAKANA",
    # "KEY_HIRAGANA",
    # "KEY_HENKAN",
    # "KEY_KATAKANAHIRAGANA",
    # "KEY_MUHENKAN",
    # "KEY_KPJPCOMMA",
    "KEY_KPENTER",
    "KEY_RIGHTCTRL",
    "KEY_KPSLASH",
    # "KEY_SYSRQ",
    "KEY_RIGHTALT",
    # "KEY_LINEFEED",
    "KEY_HOME",
    "KEY_UP",
    "KEY_PAGEUP",
    "KEY_LEFT",
    "KEY_RIGHT",
    "KEY_END",
    "KEY_DOWN",
    "KEY_PAGEDOWN",
    "KEY_INSERT",
    "KEY_DELETE",
    # "KEY_MACRO",
    # "KEY_MUTE",
    # "KEY_VOLUMEDOWN",
    # "KEY_VOLUMEUP",
    # "KEY_POWER",  # SC System Power Down */
    "KEY_KPEQUAL",
    "KEY_KPPLUSMINUS",
    # "KEY_PAUSE",
    # "KEY_SCALE",  # AL Compiz Scale (Expose) */

    "KEY_KPCOMMA",
    # "KEY_HANGEUL",
    # "KEY_HANGUEL",
    # "KEY_HANJA",
    # "KEY_YEN",
    "KEY_LEFTMETA",
    "KEY_RIGHTMETA",
    # "KEY_COMPOSE",

    # "KEY_STOP",  # AC Stop */
    # "KEY_AGAIN",
    # "KEY_PROPS",  # AC Properties */
    # "KEY_UNDO",  # AC Undo */
    # "KEY_FRONT",
    # "KEY_COPY",  # AC Copy */
    # "KEY_OPEN",  # AC Open */
    # "KEY_PASTE",  # AC Paste */
    # "KEY_FIND",  # AC Search */
    # "KEY_CUT",  # AC Cut */
    # "KEY_HELP",  # AL Integrated Help Center */
    # "KEY_MENU",  # Menu (show menu) */
    # "KEY_CALC",  # AL Calculator */
    # "KEY_SETUP",
    # "KEY_SLEEP",  # SC System Sleep */
    # "KEY_WAKEUP",  # System Wake Up */
    # "KEY_FILE",  # AL Local Machine Browser */
    # "KEY_SENDFILE",
    # "KEY_DELETEFILE",
    # "KEY_XFER",
    # "KEY_PROG1",
    # "KEY_PROG2",
    # "KEY_WWW",  # AL Internet Browser */
    # "KEY_MSDOS",
    # "KEY_COFFEE",  # AL Terminal Lock/Screensaver */
    # "KEY_SCREENLOCK",
    # "KEY_DIRECTION",
    # "KEY_CYCLEWINDOWS",
    # "KEY_MAIL",
    # "KEY_BOOKMARKS",  # AC Bookmarks */
    # "KEY_COMPUTER",
    # "KEY_BACK",  # AC Back */
    # "KEY_FORWARD",  # AC Forward */
    # "KEY_CLOSECD",
    # "KEY_EJECTCD",
    # "KEY_EJECTCLOSECD",
    # "KEY_NEXTSONG",
    # "KEY_PLAYPAUSE",
    # "KEY_PREVIOUSSONG",
    # "KEY_STOPCD",
    # "KEY_RECORD",
    # "KEY_REWIND",
    # "KEY_PHONE",  # Media Select Telephone */
    # "KEY_ISO",
    # "KEY_CONFIG",  # AL Consumer Control Configuration */
    # "KEY_HOMEPAGE",  # AC Home */
    # "KEY_REFRESH",  # AC Refresh */
    # "KEY_EXIT",  # AC Exit */
    # "KEY_MOVE",
    # "KEY_EDIT",
    # "KEY_SCROLLUP",
    # "KEY_SCROLLDOWN",
    # "KEY_KPLEFTPAREN",
    # "KEY_KPRIGHTPAREN",
    # "KEY_NEW",  # AC New */
    # "KEY_REDO",  # AC Redo/Repeat */

    "KEY_F13",
    "KEY_F14",
    "KEY_F15",
    "KEY_F16",
    "KEY_F17",
    "KEY_F18",
    "KEY_F19",
    "KEY_F20",
    "KEY_F21",
    "KEY_F22",
    "KEY_F23",
    "KEY_F24",

    # "KEY_PLAYCD",
    # "KEY_PAUSECD",
    # "KEY_PROG3",
    # "KEY_PROG4",
    # "KEY_DASHBOARD",  # AL Dashboard */
    # "KEY_SUSPEND",
    # "KEY_CLOSE",  # AC Close */
    # "KEY_PLAY",
    # "KEY_FASTFORWARD",
    # "KEY_BASSBOOST",
    # "KEY_PRINT",  # AC Print */
    # "KEY_HP",
    # "KEY_CAMERA",
    # "KEY_SOUND",
    # "KEY_QUESTION",
    # "KEY_EMAIL",
    # "KEY_CHAT",
    # "KEY_SEARCH",
    # "KEY_CONNECT",
    # "KEY_FINANCE",  # AL Checkbook/Finance */
    # "KEY_SPORT",
    # "KEY_SHOP",
    # "KEY_ALTERASE",
    # "KEY_CANCEL",  # AC Cancel */
    # "KEY_BRIGHTNESSDOWN",
    # "KEY_BRIGHTNESSUP",
    # "KEY_MEDIA",

    # "KEY_SWITCHVIDEOMODE",  # Cycle between available video
    #				outputs (Monitor/LCD/TV-out/etc) */
    # "KEY_KBDILLUMTOGGLE",
    # "KEY_KBDILLUMDOWN",
    # "KEY_KBDILLUMUP",

    # "KEY_SEND",  # AC Send */
    # "KEY_REPLY",  # AC Reply */
    # "KEY_FORWARDMAIL",  # AC Forward Msg */
    # "KEY_SAVE",  # AC Save */
    # "KEY_DOCUMENTS",

    # "KEY_BATTERY",

    # "KEY_BLUETOOTH",
    # "KEY_WLAN",
    # "KEY_UWB",

    # "KEY_UNKNOWN",

    # "KEY_VIDEO_NEXT",  # drive next video source */
    # "KEY_VIDEO_PREV",  # drive previous video source */
    # "KEY_BRIGHTNESS_CYCLE",  # brightness up, after max is min */
    # "KEY_BRIGHTNESS_ZERO",  # brightness off, use ambient */
    # "KEY_DISPLAY_OFF",  # display device to off state */

    # "KEY_WIMAX",
    # "KEY_RFKILL",  # Key that controls all radios */

    # "KEY_MICMUTE",  # Mute / unmute the microphone */

    #* Code 255 is reserved for special needs of AT keyboard driver */

    # "BTN_MISC",
    # "BTN_0",
    # "BTN_1",
    # "BTN_2",
    # "BTN_3",
    # "BTN_4",
    # "BTN_5",
    # "BTN_6",
    # "BTN_7",
    # "BTN_8",
    # "BTN_9",

    # "BTN_MOUSE",
    "BTN_LEFT",
    "BTN_RIGHT",
    "BTN_MIDDLE",
    "BTN_SIDE",
    "BTN_EXTRA",
    "BTN_FORWARD",
    "BTN_BACK",
    # "BTN_TASK",

    # "BTN_JOYSTICK",
    # "BTN_TRIGGER",
    # "BTN_THUMB",
    # "BTN_THUMB2",
    # "BTN_TOP",
    # "BTN_TOP2",
    # "BTN_PINKIE",
    # "BTN_BASE",
    # "BTN_BASE2",
    # "BTN_BASE3",
    # "BTN_BASE4",
    # "BTN_BASE5",
    # "BTN_BASE6",
    # "BTN_DEAD",

    # "BTN_GAMEPAD",
    # "BTN_A",
    # "BTN_B",
    # "BTN_C",
    # "BTN_X",
    # "BTN_Y",
    # "BTN_Z",
    # "BTN_TL",
    # "BTN_TR",
    # "BTN_TL2",
    # "BTN_TR2",
    # "BTN_SELECT",
    # "BTN_START",
    # "BTN_MODE",
    # "BTN_THUMBL",
    # "BTN_THUMBR",

    # "BTN_DIGI",
    # "BTN_TOOL_PEN",
    # "BTN_TOOL_RUBBER",
    # "BTN_TOOL_BRUSH",
    # "BTN_TOOL_PENCIL",
    # "BTN_TOOL_AIRBRUSH",
    # "BTN_TOOL_FINGER",
    # "BTN_TOOL_MOUSE",
    # "BTN_TOOL_LENS",
    # "BTN_TOOL_QUINTTAP",  # Five fingers on trackpad */
    # "BTN_TOUCH",
    # "BTN_STYLUS",
    # "BTN_STYLUS2",
    # "BTN_TOOL_DOUBLETAP",
    # "BTN_TOOL_TRIPLETAP",
    # "BTN_TOOL_QUADTAP",  # Four fingers on trackpad */

    # "BTN_WHEEL",
    # "BTN_GEAR_DOWN",
    # "BTN_GEAR_UP",

    # "KEY_OK",
    # "KEY_SELECT",
    # "KEY_GOTO",
    # "KEY_CLEAR",
    # "KEY_POWER2",
    # "KEY_OPTION",
    # "KEY_INFO",  # AL OEM Features/Tips/Tutorial */
    # "KEY_TIME",
    # "KEY_VENDOR",
    # "KEY_ARCHIVE",
    # "KEY_PROGRAM",  # Media Select Program Guide */
    # "KEY_CHANNEL",
    # "KEY_FAVORITES",
    # "KEY_EPG",
    # "KEY_PVR",  # Media Select Home */
    # "KEY_MHP",
    # "KEY_LANGUAGE",
    # "KEY_TITLE",
    # "KEY_SUBTITLE",
    # "KEY_ANGLE",
    # "KEY_ZOOM",
    # "KEY_MODE",
    # "KEY_KEYBOARD",
    # "KEY_SCREEN",
    # "KEY_PC",  # Media Select Computer */
    # "KEY_TV",  # Media Select TV */
    # "KEY_TV2",  # Media Select Cable */
    # "KEY_VCR",  # Media Select VCR */
    # "KEY_VCR2",  # VCR Plus */
    # "KEY_SAT",  # Media Select Satellite */
    # "KEY_SAT2",
    # "KEY_CD",  # Media Select CD */
    # "KEY_TAPE",  # Media Select Tape */
    # "KEY_RADIO",
    # "KEY_TUNER",  # Media Select Tuner */
    # "KEY_PLAYER",
    # "KEY_TEXT",
    # "KEY_DVD",  # Media Select DVD */
    # "KEY_AUX",
    # "KEY_MP3",
    # "KEY_AUDIO",  # AL Audio Browser */
    # "KEY_VIDEO",  # AL Movie Browser */
    # "KEY_DIRECTORY",
    # "KEY_LIST",
    # "KEY_MEMO",  # Media Select Messages */
    # "KEY_CALENDAR",
    # "KEY_RED",
    # "KEY_GREEN",
    # "KEY_YELLOW",
    # "KEY_BLUE",
    # "KEY_CHANNELUP",  # Channel Increment */
    # "KEY_CHANNELDOWN",  # Channel Decrement */
    # "KEY_FIRST",
    # "KEY_LAST",  # Recall Last */
    # "KEY_AB",
    # "KEY_NEXT",
    # "KEY_RESTART",
    # "KEY_SLOW",
    # "KEY_SHUFFLE",
    # "KEY_BREAK",
    # "KEY_PREVIOUS",
    # "KEY_DIGITS",
    # "KEY_TEEN",
    # "KEY_TWEN",
    # "KEY_VIDEOPHONE",  # Media Select Video Phone */
    # "KEY_GAMES",  # Media Select Games */
    # "KEY_ZOOMIN",  # AC Zoom In */
    # "KEY_ZOOMOUT",  # AC Zoom Out */
    # "KEY_ZOOMRESET",  # AC Zoom */
    # "KEY_WORDPROCESSOR",  # AL Word Processor */
    # "KEY_EDITOR",  # AL Text Editor */
    # "KEY_SPREADSHEET",  # AL Spreadsheet */
    # "KEY_GRAPHICSEDITOR",  # AL Graphics Editor */
    # "KEY_PRESENTATION",  # AL Presentation App */
    # "KEY_DATABASE",  # AL Database App */
    # "KEY_NEWS",  # AL Newsreader */
    # "KEY_VOICEMAIL",  # AL Voicemail */
    # "KEY_ADDRESSBOOK",  # AL Contacts/Address Book */
    # "KEY_MESSENGER",  # AL Instant Messaging */
    # "KEY_DISPLAYTOGGLE",  # Turn display (LCD) on and off */
    # "KEY_SPELLCHECK",  # AL Spell Check */
    # "KEY_LOGOFF",  # AL Logoff */

    # "KEY_DOLLAR",
    # "KEY_EURO",

    # "KEY_FRAMEBACK",  # Consumer - transport controls */
    # "KEY_FRAMEFORWARD",
    # "KEY_CONTEXT_MENU",  # GenDesc - system context menu */
    # "KEY_MEDIA_REPEAT",  # Consumer - transport control */
    # "KEY_10CHANNELSUP",  # 10 channels up (10+) */
    # "KEY_10CHANNELSDOWN",  # 10 channels down (10-) */
    # "KEY_IMAGES",  # AL Image Browser */

    # "KEY_DEL_EOL",
    # "KEY_DEL_EOS",
    # "KEY_INS_LINE",
    # "KEY_DEL_LINE",

    # "KEY_FN",
    # "KEY_FN_ESC",
    # "KEY_FN_F1",
    # "KEY_FN_F2",
    # "KEY_FN_F3",
    # "KEY_FN_F4",
    # "KEY_FN_F5",
    # "KEY_FN_F6",
    # "KEY_FN_F7",
    # "KEY_FN_F8",
    # "KEY_FN_F9",
    # "KEY_FN_F10",
    # "KEY_FN_F11",
    # "KEY_FN_F12",
    # "KEY_FN_1",
    # "KEY_FN_2",
    # "KEY_FN_D",
    # "KEY_FN_E",
    # "KEY_FN_F",
    # "KEY_FN_S",
    # "KEY_FN_B",

    # "KEY_BRL_DOT1",
    # "KEY_BRL_DOT2",
    # "KEY_BRL_DOT3",
    # "KEY_BRL_DOT4",
    # "KEY_BRL_DOT5",
    # "KEY_BRL_DOT6",
    # "KEY_BRL_DOT7",
    # "KEY_BRL_DOT8",
    # "KEY_BRL_DOT9",
    # "KEY_BRL_DOT10",

    # "KEY_NUMERIC_0",  # used by phones, remote controls, */
    # "KEY_NUMERIC_1",  # and other keypads */
    # "KEY_NUMERIC_2",
    # "KEY_NUMERIC_3",
    # "KEY_NUMERIC_4",
    # "KEY_NUMERIC_5",
    # "KEY_NUMERIC_6",
    # "KEY_NUMERIC_7",
    # "KEY_NUMERIC_8",
    # "KEY_NUMERIC_9",
    # "KEY_NUMERIC_STAR",
    # "KEY_NUMERIC_POUND",

    # "KEY_CAMERA_FOCUS",
    # "KEY_WPS_BUTTON",  # WiFi Protected Setup key */

    # "KEY_TOUCHPAD_TOGGLE",  # Request switch touchpad on or off */
    # "KEY_TOUCHPAD_ON",
    # "KEY_TOUCHPAD_OFF",

    # "KEY_CAMERA_ZOOMIN",
    # "KEY_CAMERA_ZOOMOUT",
    # "KEY_CAMERA_UP",
    # "KEY_CAMERA_DOWN",
    # "KEY_CAMERA_LEFT",
    # "KEY_CAMERA_RIGHT",

    # "KEY_ATTENDANT_ON",
    # "KEY_ATTENDANT_OFF",
    # "KEY_ATTENDANT_TOGGLE",  # Attendant call on or off */
    # "KEY_LIGHTS_TOGGLE",  # Reading light on or off */

    # "BTN_TRIGGER_HAPPY",
    # "BTN_TRIGGER_HAPPY1",
    # "BTN_TRIGGER_HAPPY2",
    # "BTN_TRIGGER_HAPPY3",
    # "BTN_TRIGGER_HAPPY4",
    # "BTN_TRIGGER_HAPPY5",
    # "BTN_TRIGGER_HAPPY6",
    # "BTN_TRIGGER_HAPPY7",
    # "BTN_TRIGGER_HAPPY8",
    # "BTN_TRIGGER_HAPPY9",
    # "BTN_TRIGGER_HAPPY10",
    # "BTN_TRIGGER_HAPPY11",
    # "BTN_TRIGGER_HAPPY12",
    # "BTN_TRIGGER_HAPPY13",
    # "BTN_TRIGGER_HAPPY14",
    # "BTN_TRIGGER_HAPPY15",
    # "BTN_TRIGGER_HAPPY16",
    # "BTN_TRIGGER_HAPPY17",
    # "BTN_TRIGGER_HAPPY18",
    # "BTN_TRIGGER_HAPPY19",
    # "BTN_TRIGGER_HAPPY20",
    # "BTN_TRIGGER_HAPPY21",
    # "BTN_TRIGGER_HAPPY22",
    # "BTN_TRIGGER_HAPPY23",
    # "BTN_TRIGGER_HAPPY24",
    # "BTN_TRIGGER_HAPPY25",
    # "BTN_TRIGGER_HAPPY26",
    # "BTN_TRIGGER_HAPPY27",
    # "BTN_TRIGGER_HAPPY28",
    # "BTN_TRIGGER_HAPPY29",
    # "BTN_TRIGGER_HAPPY30",
    # "BTN_TRIGGER_HAPPY31",
    # "BTN_TRIGGER_HAPPY32",
    # "BTN_TRIGGER_HAPPY33",
    # "BTN_TRIGGER_HAPPY34",
    # "BTN_TRIGGER_HAPPY35",
    # "BTN_TRIGGER_HAPPY36",
    # "BTN_TRIGGER_HAPPY37",
    # "BTN_TRIGGER_HAPPY38",
    # "BTN_TRIGGER_HAPPY39",
    # "BTN_TRIGGER_HAPPY40",

    #*  We avoid low common keys in module aliases so they don't get huge. */
    # "KEY_MIN_INTERESTING",
    # "KEY_MAX",
    # "KEY_CNT",
    )
