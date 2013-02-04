#!/usr/bin/python

# build.py
#
# Created by Jordan Suchow.
# http://jwsu.ch/ow
#
# Heavily modified by Alexander Blocker.
# http://www.awblocker.com

import fileinput
import os
import sys
import re
import argparse

kScriptsDir = 'scripts'
kChaptersDir = 'chapters'
kTemplatesDir = 'templates'

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument("chapters", nargs='+',metavar='CHAPTER',
                      help='Name of chapter to build.')
  parser.add_argument("--appendix", action='store_true',
                      help='Make appendices instead of regular chapters.')
  
  # Parse arguments
  args = parser.parse_args(argv)

  # Check for conflict
  if args.appendix:
    chapter_pattern = 'appendix-%s.tex'
    re_chapter = re.compile('appendix-.*\.tex')
  else:
    chapter_pattern = 'chapter-%s.tex'
    re_chapter = re.compile('chapter-.*\.tex')

  chapter_list = os.listdir(kChaptersDir + '/')
  chapter_list = [fname for fname in chapter_list if re_chapter.match(fname)]
  for chapter in args.chapters:
    # Build filename for new chapter
    new_chapter_fname = chapter_pattern % chapter
    new_chapter_name, _ = os.path.splitext(new_chapter_fname)
  
    # Check for conflicts
    if new_chapter_fname in chapter_list:
      print >> sys.stderr, '%s already exists. Will not overwrite.'
      continue
    
    # copy the template chapter to the chapters directory
    os.system('cp -R %(templateDir)s/chapter.tex %(chapterDir)s/%(chapter)s' %
              {'templateDir' : kTemplatesDir, 'chapterDir' : kChaptersDir,
               'chapter' : new_chapter_fname})
    
    # Find last chapter in thesis
    with open('thesis.tex', 'rb') as f:
      max_chapter = 0
      if args.appendix:
        for i, line in enumerate(f):
          if re.search('\\include{%s/%s' % (kChaptersDir, 'appendix-'), line):
            max_chapter = i
      
      if max_chapter == 0:
        for i, line in enumerate(f):
          if re.search('\\include{%s/%s' % (kChaptersDir, 'chapter-'), line):
            max_chapter= i

    # add the chapter to the thesis
    f = fileinput.input('thesis.tex', inplace=True)
    for i, line in enumerate(f):
      print line,
      if i == max_chapter:
        print '\\include{%s/%s}' % (kChaptersDir, new_chapter_name)

    f.close()

  # exit terminal
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))

