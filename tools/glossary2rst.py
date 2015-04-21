#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import re
import sys

from lxml import etree

SKIP_TAGS = ['indexterm', 'info', 'primary', 'title']

KNOWN_TAGS = [
    'code',
    'command',
    'filename',
    'link',
    'literal',
    'glossary',
    'glossdef',
    'glossdiv',
    'glossentry',
    'glossterm',
    'para',
    'phrase',
    'systemitem',
    'title'
    ]

# Marks the first glossdiv entry
FIRST_GLOSSDIV = True


def remove_indent(s):
    """Remove indention of paragraph."""
    s = "\n".join(i.lstrip() for i in s.splitlines())
    return s


def concat(element):
    """Concatenate element and its children."""
    s = ""
    if element.text is not None:
        s += remove_indent(element.text)
    # Add all children
    for i in element.getchildren():
        s += convert(i)
        if i.tail is not None:
            if len(s) > 0 and not s[-1].isspace() and i.tail[0] in " \t":
                s += i.tail[0]
            s += remove_indent(i.tail)
    return s


def indent(element, indent):
    """Indent paragraph."""
    start = "\n\n"

    lines = [" " * indent + i for i in concat(element).splitlines()
             if i and not i.isspace()]
    return start + "\n".join(lines)


def link(element):
    # Only handles the single link we need...
    href = element.attrib['{http://www.w3.org/1999/xlink}href']
    href = href.lstrip()
    if href == "https://git.openstack.org/cgit/openstack/openstack-manuals":
        s = ("`openstack/openstack-manuals repository " +
             "<https://git.openstack.org/cgit/openstack/openstack-manuals>`__")
        return s
    print ("link not handled %s" % href)
    sys.exit(1)


def glossdiv(element):

    s = ""
    global FIRST_GLOSSDIV
    if FIRST_GLOSSDIV:
        s = '.. glossary::\n\n'
        FIRST_GLOSSDIV = False

    return s + concat(element)


def glossentry(element):
    s = "\n"
    glossterm = element.find("{http://docbook.org/ns/docbook}glossterm")
    if glossterm.text is not None:
        s += "   " + glossterm.text + "\n"

    glossdef = element.find("{http://docbook.org/ns/docbook}glossdef")
    if glossdef is not None:
        s += indent(glossdef, 6)
    return s


def convert(element):
    if not isinstance(element.tag, basestring):
        print("Element %s not handled, aborting!" % element.text)
    tag = element.tag.replace('{http://docbook.org/ns/docbook}', '')
    if tag in SKIP_TAGS:
        return ""
    if tag not in KNOWN_TAGS:
        print("Tag %s not handled, aborting!" % tag)
        sys.exit(1)
    if tag == "command":
        return ":command:`%s`" % element.text
    if tag == "code":
        return "`%s`" % element.text
    if tag == "filename":
        return ":file:`%s`" % element.text
    if tag == "glossary":
        return concat(element)
    if tag == "glossdiv":
        return glossdiv(element)
    if tag == "glossentry":
        return glossentry(element)
    if tag == "link":
        return link(element)
    if tag == "literal":
        return "`%s`" % element.text
    if tag == "para":
        return "\n\n" + concat(element)
    if tag == "phrase":
        return element.text
    if tag == "systemitem":
        return element.text

    print("not handled tag %s - %s" % (element.tag, element.text))
    sys.exit(1)


def rst_convert(element):
    output = convert(element)
    # Replace multiple empty lines with single empty line
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output


def glossary_convert(filename):

    try:
        parser = etree.XMLParser(remove_comments=True)
        doc = etree.parse(filename, parser=parser)
    except etree.XMLSyntaxError as e:
        print(" Warning: file %s is invalid XML: %s" % (filename, e))

    rstcontent = rst_convert(doc.getroot()).encode('utf-8')
    heading = "========\n" + "Glossary\n" + "========\n\n"
    heading += ".. comments\n"
    heading += "   This file file is automatically generated, edit the master"
    heading += "   doc/glossary/glossary-terms.xml to update it."

    if len(sys.argv) != 2:
        print(heading + rstcontent)
    else:
        with open(sys.argv[1], 'w') as fp:
            fp.write(heading)
            fp.write(rstcontent)


if __name__ == '__main__':
    glossary_convert("doc/glossary/glossary-terms.xml")
