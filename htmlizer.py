from __future__ import with_statement

import os
from string import Template

import mapwords
import soundmap

entries = []

pi = mapwords.pi[0:100]
words = mapwords.get_best_mapping(pi)

for wid, word in enumerate(words):
    base = 'final/images/'
    if os.path.exists(base + word):
        photo_urls = ['images/%s/%s' %(word, filename) \
                                for filename in sorted(os.listdir(base+word)) \
                                    if filename.endswith('.jpg')]
        credits = [open(base+'%s/%s'%(word,filename)).read().strip('\r\n ') \
                                for filename in sorted(os.listdir(base+word)) \
                                                if filename.endswith('.credit')]
        assert(len(photo_urls) == len(credits))
    else:
        photo_urls = []
        credits = []

    if len(photo_urls) > 0:
        big_image_url = photo_urls[0]
    else:
        big_image_url = ''


    little_image = Template(open('base/_little_image.html').read())
    little_images = []
    for id, url in enumerate(photo_urls[:6]):
        data = {'url':url,'word':word,'id':id,'credit':credits[id],'wid':wid}
        little_images.append(little_image.substitute(data))


    image = Template(open('base/_image.html').read())
    image_data = {'url':big_image_url,
                  'little_images':''.join(little_images),
                  'word':word,
                  'wid':wid}

    entry = {'word':word,
             'number':soundmap.convert_to_digits(word),
             'image':image.substitute(image_data)}
    entries.append(Template(open('base/_entry.html').read()).substitute(entry))

def chunk(n):
    chunked = []
    for i,c in enumerate(str(n)):
        if i % 5 == 0:
            chunked.append(' ')
        chunked.append(c)
    return ''.join(chunked)

content = {'content': ''.join(entries), 'pi':chunk(pi)}

index = Template(open('base/index.html').read())
with open('final/index.html', 'w') as f:
    f.write(index.substitute(content))


