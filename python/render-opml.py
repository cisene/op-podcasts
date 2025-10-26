#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
from datetime import datetime

import yaml
from lxml import etree

SOURCE_YAML = '../yaml/op-podcasts.yaml'

OUTPUT_FILENAME = '../op-podcasts.opml'

global config

def writeOPML(filepath, contents):
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
  utc_now = datetime.now().isoformat()

  if config == None:
    print("config is empty")
    exit(0)

  # Open OPML
  opml = etree.Element("opml", version = "2.0")

  # Open Head
  head = etree.SubElement(opml, "head")

  # Handle Title
  title_text = f"{config['global']['title']}"
  title = etree.Element("title")
  title.text = str(title_text)
  head.append(title)

  # Handle URL
  url_text = f"{config['global']['url']}"
  url = etree.Element("url")
  url.text = str(url_text)
  head.append(url)

  # Handle dateCreated - 2024-02-19 10:30:00 +0100
  datecreated_text = datetime.strptime(str(config['global']['dateCreated']), '%Y-%m-%d %H:%M:%S %z').strftime('%c +0000')
  dateCreated = etree.Element("dateCreated")
  dateCreated.text = str(datecreated_text)
  head.append(dateCreated)

  # Handle dateModified
  datemodified_text = formatDateStringUTCNow()
  dateModified = etree.Element("dateModified")
  dateModified.text = str(datemodified_text)
  head.append(dateModified)

  # Handle ownerName
  ownerName_text = f"{config['global']['ownerName']}"
  ownerName = etree.Element("ownerName")
  ownerName.text = str(ownerName_text)
  head.append(ownerName)

  #<ownerEmail>christopher.isene@gmail.com</ownerEmail>
  ownerEmail_text = f"{config['global']['ownerEmail']}"
  ownerEmail = etree.Element("ownerEmail")
  ownerEmail.text = str(ownerEmail_text)
  head.append(ownerEmail)

  opml.append(head)

  comment_text = f" Source: https://github.com/cisene/op-podcasts "
  comment = etree.Comment(comment_text)
  opml.append(comment)

  # Close head

  # Open body
  body = etree.Element("body")

  for section in config['body']:
    if len(section['podcasts']) > 0:
      section_text = section['section']
      section_language = section['language']
      section_podcasts = section['podcasts']
      section = etree.Element("outline")
      section.set('text', str(section_text))
      section.set('language', str(section_language))

      for item in section_podcasts:
        item_text = item['text']
        item_language = item['language']
        item_htmlUrl = item['htmlUrl']
        item_xmlUrl = item['xmlUrl']

        outline = etree.Element("outline")
        outline.set('type', "link")
        outline.set('version', "rss")
        outline.set('language', str(item_language))
        outline.set('text', str(item_text))
        outline.set('title', str(item_text))
        outline.set('htmlUrl', str(item_htmlUrl))
        outline.set('xmlUrl', str(item_xmlUrl))

        section.append(outline)

      body.append(section)

  # Close body
  opml.append(body)

  opml_contents = etree.tostring(opml, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
  
  writeOPML(OUTPUT_FILENAME, opml_contents)


def main():
  config = None
  config = LoadYamlConfig(SOURCE_YAML)

  #print(config)

  if config != None:
    ProcessItems(config)

if __name__ == '__main__':
  main()
