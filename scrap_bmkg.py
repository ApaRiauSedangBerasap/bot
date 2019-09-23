import sys
import bs4
from bs4 import BeautifulSoup

# parse the latest file
filename = sys.argv[1]
with open(filename, 'r') as f:
    t = f.readlines()
soup = BeautifulSoup("\n".join(t), 'html.parser')
script_elements = soup.select('script')
js_content = [ i for i in script_elements \
        if len(i.contents) > 0 and ".highcharts" in i.contents[0] ]
js_content = js_content[0]

# parse template file
bmkg_filepath='bmkg/bmkg.html'
with open(bmkg_filepath, 'r') as f:
    t = f.readlines()
# soup = BeautifulSoup("".join([i.trim() for i in t]), 'html.parser')
soup = BeautifulSoup("".join(t), 'html.parser')
elm = soup.select_one('#scriptPEKANBARU')
# elm.contents[0]='sfdsf'
elm.string = js_content.string
print 'elm', elm
# print elm.contents
# child = soup.new_tag("a", href="hm/test", class_="child")
# child.string = 'BARU'
# elm.contents = [u'sdfjsdfj']
for i in elm.children:
    if isinstance(i, bs4.element.Tag):
        i.extract()
    # print type(i)
    # print i
# elm.a.extract()
# elm.a.extract()
# print type(elm.a)
# elm.contents[0].replace_with(child)
# elm.append(child)

with open(bmkg_filepath, 'w') as f:
    f.write(soup.prettify().encode('utf-8'))

