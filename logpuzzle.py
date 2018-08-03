#!/usr/bin/python

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def get_value(tuples):
  return tuples[1]

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  
  hostname_match = re.search(r'_([\w.-]+)',filename)
  if not hostname_match:
    sys.stderr.write('The filename is not correct' + filename)
    sys.exit(1)
  hostname = 'http://' + hostname_match.group(1)
  
  url_list = []
  url_tuples = {}

  f = open(filename, 'rU')
  text = f.read()
  f.close()
  url_match = re.findall(r'GET\s([\w.\/-]+\.jpg)\sHTTP', text)
  for url in url_match:
    if 'puzzle' in url:
      fig_name = re.search(r'\/([\w.-]+.jpg)', url)
      name_list = fig_name.group(1).split('-')
      if not url in url_tuples:
        url_tuples[url] = name_list[-1]

  sorted_url = sorted(url_tuples.items(), key = get_value)
  for u in sorted_url:
    full_url = hostname + u[0]
    url_list.append(full_url)
  return url_list
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  full_dest_dir = os.path.abspath(dest_dir)
 
  i = 0
  f = open(full_dest_dir + '/index.html', 'w+')
  f.write('<html>\n')
  f.write('<body>\n')

  print 'Retrieving...'
  for url in img_urls:
    urllib.urlretrieve(url,full_dest_dir + '/img' + str(i) + '.jpg')
    f.write('<img src="'+full_dest_dir+'/img'+str(i)+'.jpg">'),
    i += 1
  f.write('\n')
  f.write('</body>\n')
  f.write('</html>') 
  f.close()
  print 'Done'


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
