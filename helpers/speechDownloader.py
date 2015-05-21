from urllib2 import urlopen, Request


class SpeechDownloader(object):

    def __init__(self, url, header, download_path):
        self._url = url
        self._header = header
        self._download_path = download_path

    def download(self):
        # python 2.7 bug: instance returned by urlopen does not implement __exit__
        # so context manager isn't supported for urlopen()
        try:
            request = Request(self._url)
            header_key, header_value = self._header.items()[0]
            request.add_header(header_key, header_value)
            speech = urlopen(request)
            with open(self._download_path, 'wb') as f:
                f.write(speech.read())
        except Exception, err:
            print err
        finally:
            speech.close()
