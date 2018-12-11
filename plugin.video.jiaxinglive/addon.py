# -*- coding: utf-8 -*-
import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
from resources.lib.plugin import JiaxingLive

plugin_url = sys.argv[0]
_handle = int(sys.argv[1])

class ParamUtil(object):
    @staticmethod
    def parse_param(paramstring):
        return dict(parse_qsl(paramstring[1:]))

    @staticmethod
    def make_param(**kwargs):
        return '{0}?{1}'.format(plugin_url, urlencode(kwargs))

CHANNEL_ITEMS = {}
for channel in JiaxingLive.get_tv_list():
    channel_item = xbmcgui.ListItem(label=channel['name'])

    channel_item.setInfo('video', {'title': u'直播: 嘉兴{}'.format(channel['name']), 'mediatype': 'video'})
    channel_item.setArt({'thumb': channel['thumb'], 'icon': channel['thumb'], 'fanart': channel['fanart']})

    channel_item.setProperty('IsPlayable', 'true')
    new_url = ParamUtil.make_param(action='play', channel_pinyin=channel['pinyin'])
    CHANNEL_ITEMS[channel['pinyin']]=(channel_item, new_url)

def show_channels():
    for _, (channel_item, url) in CHANNEL_ITEMS.iteritems():
        xbmcplugin.addDirectoryItem(_handle, url, channel_item, False)
    xbmcplugin.endOfDirectory(handle=_handle, succeeded=True)

def play_channel(channel_pinyin):
    channel_item, _ = CHANNEL_ITEMS[channel_pinyin]
    stream_url = JiaxingLive.parse_livestream(channel_pinyin)
    channel_item.setPath(stream_url)
    # xbmcplugin.setResolvedUrl(_handle, True, channel_item)
    xbmc.Player().play(stream_url, channel_item)

def route(paramstring):
    params = ParamUtil.parse_param(paramstring)
    # route to elsewhere
    if params:
        # play source
        if params['action'] == 'play':
            play_channel(params['channel_pinyin'])

    # homepage
    show_channels()

if __name__ == '__main__':
    route(sys.argv[2])
