import pdfkit
import httplib2
from bs4 import BeautifulSoup
import urllib
import os,sys
import urllib.request

http= httplib2.Http()


def urltopdf(url,output):
    status, response = http.request(url)
    location  = urllib.parse.urlparse(url).netloc
    soup = BeautifulSoup(response,'html.parser')

    csslist=[]
    for link in soup.findAll('link'):
        if (link.has_attr("href")):
            link['href'] = "https://{}{}".format(location, link["href"])
            response = urllib.request.urlopen(link['href'])
            if link['href'].find('/'):
                file= link['href'].rsplit('/', 1)[1]
                print(file)
                filename, file_extension = os.path.splitext(file)
                if(file_extension=='css'):
                    cssfile="tmp\\{}".format(file)

                    open(cssfile, "wb").write(response.read())
                    csslist.append(cssfile)
    for img in soup.findAll('img'):
        if(img.has_attr("src")):
            img["src"] = "https://{}{}".format(location,img["src"])

    for script in soup.find_all('script'):

        if(script.has_attr('src')):
            script["src"]="https://{}{}".format(location,script["src"])
    open("tmp//response.html","w",encoding='utf-8').write(str(soup))
    pdfkit.from_file("tmp//response.html",output,css=csslist)


urltopdf(sys.argv[1],sys.argv[2])