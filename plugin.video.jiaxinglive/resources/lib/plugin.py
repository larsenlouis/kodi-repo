# -*- coding: utf-8 -*-
import re
import requests


class JiaxingLive(object):
    channels = {
        'tv': {
            'xwzh': {
                'id': 11,
                'meta': {
                    'name': u'新闻综合',
                    'thumb': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/201801081032080fXl.png',
                    'fanart': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/201801081032080fXl.png'
                }
            },
            'whys': {
                'id': 12,
                'meta': {
                    'name': u'文化影视',
                    'thumb': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/20180108103352QyHm.png',
                    'fanart': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/20180108103352QyHm.png'
                }
            },
            'ggpd': {
                'id': 14,
                'meta': {
                    'name': u'公共频道',
                    'thumb': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/20180108103610t3t1.png',
                    'fanart': 'http://imgs.jiaxingren.com/material/publishcontent/img/170x120/2018/01/20180108103610t3t1.png'
                }
            }
        }
    }

    @classmethod
    def __construct_livestream_regex_pattern(self, channel_pinyin):
        return re.compile(r'http://stream1.jiaxingren.com/' +
                          channel_pinyin + '/playlist.m3u8\?_upt=\w{18}')

    @classmethod
    def parse_livestream(self, channel_pinyin):
        channel_id = self.channels['tv'][channel_pinyin]['id']
        r = requests.get(
            'http://www.jiaxingren.com/m2o/program_switch.php?channel_id={}'.format(channel_id))
        r.encoding = 'utf8'
        pattern = self.__construct_livestream_regex_pattern(channel_pinyin)
        live_url = pattern.findall(r.text)[0]
        # real sd live live url
        # real_live_url = requests.get(live_url).text.strip().split('\n')[-1]
        # with open('/dev/shm/shit.log', 'a') as f:
        #     f.write(real_live_url+'\n')
        # real_live_url = 'http://stream1.jiaxingren.com/{}/{}'.format(channel_pinyin,real_live_url)
        return live_url

    @classmethod
    def get_tv_list(self):
        ret = []
        for channel_pinyin, info in self.channels['tv'].iteritems():
            ret.append({
                'id': info['id'],
                'name': info['meta']['name'],
                'pinyin': channel_pinyin,
                'thumb': info['meta']['thumb'],
                'fanart': info['meta']['fanart'],
            })
        return ret

    @classmethod
    def get_tv_channel_name(self, channel_pinyin):
        return self.channels['tv'][channel_pinyin]['meta']['name']

class XiaoXinShuoShiVOD(object):
    playlist_section_pattern = re.compile('<ul.*</ul>', re.S)
    item_in_playlist_page_pattern = re.compile('<a href="(.*?)".*?<img src="(.*?)" width="\d+" height="\d+" />.*?<p>(.*?)</p>.*?</a>', re.S)
    video_url_pattern = re.compile('http.*?\.m3u8')

    @classmethod
    def get_playlist(cls, page=0):
        # the pagination acts like a mysql query
        # that selects with an offset of [variable] and limit 16
        offset = page * 16
        # xxss
        page_url = 'http://www.jiaxingren.com/folder24/folder147/folder149/folder355/?pp={offset}'.format(offset=offset)
        r = requests.get(page_url)
        r.encoding = 'utf8'

        playlist_html = cls.playlist_section_pattern.findall(r.text)[0]
        ret = []
        for play_page_url, thumbnail_url, title in cls.item_in_playlist_page_pattern.findall(playlist_html):
            ret.append(
                (play_page_url, title, thumbnail_url)
            )
        return ret

    @classmethod
    def parse_vodstream(cls, play_page_url):
        r = requests.get(play_page_url)
        r.encoding = 'utf8'
        return cls.video_url_pattern.findall(r.text)[0]


if __name__ == '__main__':
    # print(JiaxingLive.parse_livestream('xwzh', 'tv'))
    # print(JiaxingLive.get_tv_list())
    pass
