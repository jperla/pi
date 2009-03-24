from __future__ import with_statement

from string import Template
import os

import flickrapi

import spider

import mapwords
import soundmap

pi = mapwords.pi[0:100]
words = mapwords.get_best_mapping(pi)

flickr_key = 'c58fc66523328377c37bbf33efc42f99'
flickr_secret = '9fa3d5d78dc938c1'
flickr_url = 'http://farm%(farm)s.static.flickr.com/%(server)s/                 %(id)s_%(secret)s_m.jpg'
flickr_profile_url = 'http://www.flickr.com/photos/%(owner)s/%(id)s'

flickr = flickrapi.FlickrAPI(flickr_key)

s = spider.Spider()

for word in words:
    try:
        base = 'final/images/'
        if not os.path.exists(base + '%s/' % word):
            os.mkdir(base + '%s' % word)
            result = flickr.photos_search(text=word, 
                                        license='1,2,3,4,5,6', 
                                        sort='relevance',
                                        per_page=6)

            for id,photo in enumerate(result.photos[0].photo):
                url = flickr_url % photo.attrib
                profile_url = flickr_profile_url % photo.attrib


                image = s.get(url)
                with open(base + '%s/%s.jpg' % (word, id), 'w') as f:
                    f.write(image)

                with open(base + '%s/%s.credit' % (word, id), 'w') as f:
                    f.write(profile_url)
    except Exception,e:
        print 'No photos for search %s' % word
        print e

