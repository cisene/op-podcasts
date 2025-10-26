#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
from datetime import datetime

import yaml
from lxml import etree

SOURCE_YAML = '../yaml/op-podcasts.yaml'

OUTPUT_FILENAME = '../README.md'

OPML_FILENAME = 'op-podcasts.opml'

global config

def writeMarkdown(filepath, contents):
  s = "\n".join(contents) + "\n"
  with open(filepath, "w") as f:
    f.write(contents)

def LoadYamlConfig(filepath):
  config = None
  with open(filepath, 'r') as stream:
    try:
      config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)
  return config

def formatDateStringUTCNow():
  result = datetime.utcnow().strftime('%c +0000')
  return result

def formatDateString(data):
  dt = datetime.fromisoformat(data)
  datestr = dt.strftime("%a, %d %b %Y %H:%M:%S %z")
  return datestr


def ProcessItems(config):
  if config == None:
    print("config is empty")
    exit(0)

  md = []

  md.append(f"# {config['global']['title']}")
  md.append(f"")

  md.append(f"Samlade podcasts för lyssning")
  md.append(f"")

  datecreated_text = datetime.strptime(str(config['global']['dateCreated']), '%Y-%m-%d %H:%M:%S %z').strftime('%c +0000')
  md.append(f"Skapad {datecreated_text}")
  md.append(f"")

  datemodified_text = formatDateStringUTCNow()
  md.append(f"Uppdaterad {datemodified_text}")
  md.append(f"")

  comment_text = f"https://github.com/cisene/op-podcasts"
  md.append(f"Källa: [{comment_text}]({comment_text})")
  md.append(f"")

  md.append(f"OPML: [{OPML_FILENAME}](./{OPML_FILENAME})")
  md.append(f"OPML direkt: [{OPML_FILENAME}](https://raw.githubusercontent.com/cisene/op-podcasts/refs/heads/main/{OPML_FILENAME})")
  md.append(f"")

  md.append(f"[TOC]")
  md.append(f"")

  md.append(f"")

  for section in config['body']:
    if len(section['podcasts']) > 0:
      section_text = section['section']
      section_language = section['language']
      section_podcasts = section['podcasts']

      md.append(f"")
      md.append(f"")
      md.append(f"## {section_text}")
      md.append(f"* Språk: {section_language}")
      md.append(f"")

      for item in section_podcasts:
        item_text = item['text']
        item_language = item['language']
        item_htmlUrl = item['htmlUrl']
        item_xmlUrl = item['xmlUrl']

        md.append(f"### {item_text}")
        md.append(f"* [Hemsida]({item_htmlUrl})")
        md.append(f"* [RSS-flöde]({item_xmlUrl})")
        md.append(f"")

  
  markdown = "\n".join(md)
  writeMarkdown(OUTPUT_FILENAME, markdown)


def main():
  config = None
  config = LoadYamlConfig(SOURCE_YAML)

  #print(config)

  if config != None:
    ProcessItems(config)

if __name__ == '__main__':
  main()
