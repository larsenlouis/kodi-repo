# -*- coding: utf-8 -*-
import sys
from urllib import urlencode, unquote as urldecode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
from resources.lib.plugin import JiaxingLive
from resources.lib.plugin import XiaoXinShuoShiVOD

plugin_url = sys.argv[0]
_handle = int(sys.argv[1])

def printx(string):
    xbmcgui.Dialog().ok('ss', str(string))

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

def index_homepage():
    xbmcplugin.setPluginCategory(_handle, '嘉兴电视')
    xbmcplugin.setContent(_handle, 'tvshows')
    for k, v in CHANNEL_ITEMS.iteritems():
        if k.startswith('vod'):
            continue
        channel_item, url = v
        xbmcplugin.addDirectoryItem(_handle, url, channel_item, False)
    # add 小新说事 vod
    vod_url = ParamUtil.make_param(action='vod_xxss') 
    vod_item = xbmcgui.ListItem(label='回看小新说事')
    xbmcplugin.addDirectoryItem(_handle, vod_url, vod_item, True)

    xbmcplugin.endOfDirectory(handle=_handle, succeeded=True)

def play_channel(channel_pinyin):
    channel_item, _ = CHANNEL_ITEMS[channel_pinyin]
    stream_url = JiaxingLive.parse_livestream(channel_pinyin)
    channel_item.setPath(stream_url)
    # xbmcplugin.setResolvedUrl(_handle, True, channel_item)
    xbmc.Player().play(stream_url, xbmcgui.ListItem())

def show_xxss():
    xbmcplugin.setPluginCategory(_handle, u'小新说事')
    xbmcplugin.setContent(_handle, 'tvshows')
    for idx, item_tuple in enumerate(XiaoXinShuoShiVOD.get_playlist()):
        play_page_url, video_title, video_thumb_url = item_tuple
        xxss_item = xbmcgui.ListItem(label=video_title)
        xxss_item.setInfo('video', {'title': u'回看: {}'.format(video_title), 'mediatype': 'video', 'playpage': play_page_url})
        xxss_item.setArt({'thumb': video_thumb_url, 'icon': video_thumb_url, 'fanart': video_thumb_url})
        xxss_item.setProperty('IsPlayable', 'true')

        new_url = ParamUtil.make_param(action='play', xxss_url=play_page_url)
        xbmcplugin.addDirectoryItem(_handle, new_url, xxss_item, False)
    xbmcplugin.endOfDirectory(handle=_handle, succeeded=True)

def play_xxss(play_page_url):
    play_page_url = urldecode(play_page_url)
    video_url = XiaoXinShuoShiVOD.parse_vodstream(play_page_url)
    xbmc.Player().play(video_url, xbmcgui.ListItem())

def route(paramstring):
    params = ParamUtil.parse_param(paramstring)
    # route to elsewhere
    if params:
        # play source
        if params['action'] == 'play':
            # livestream
            if params.get('channel_pinyin', ''):
                play_channel(params['channel_pinyin'])
            # vod xxss
            elif params.get('xxss_url', ''):
                play_xxss(params['xxss_url'])

        # vod
        elif params['action'] == 'vod_xxss':
            show_xxss()

    # homepage
    index_homepage()

if __name__ == '__main__':
    route(sys.argv[2])
