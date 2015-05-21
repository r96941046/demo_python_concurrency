import os

from urllib import urlencode

from multiprocessing.pool import Pool

from helpers.parseArgs import parse_args
from helpers.speechDownloader import SpeechDownloader
from helpers.progress import Progress


CWD = os.getcwd()


# This part enables using Pool.map and Pool.apply on
# a function defined in a class
import copy_reg
import types


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class SpeechDownloadService(object):

    SPEECH_URL = 'http://translate.google.com/translate_tts?'
    TEXT_FILE_NAME = 'vocabulary.txt'
    DOWNLOAD_DIR_NAME = 'Files'
    DOWNLOAD_FILE_TYPE = '.mp3'
    REQUEST_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }

    def __init__(self, language, task_path):
        self._language = language
        self._task_path = task_path
        self._text_file_path = self._task_path + self.TEXT_FILE_NAME
        self._download_dir = self._task_path + self.DOWNLOAD_DIR_NAME

    def setup_download_dir(self):
        download_dir = self._download_dir
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return download_dir

    def start(self):

        print 'Start Speech Download Service...'

        language = self._language
        download_dir = self.setup_download_dir()

        with open(self._text_file_path, 'r') as f:

            # python 2.7 not supporting context manager with Pool()
            pool = Pool(processes=8)

            progress = Progress(len(f.readlines()))
            f.seek(0)
            results = []

            def update_progress(result):
                results.append(result)
                progress.update(len(results))

            for text in f:
                text = text.rstrip('\n')
                encoded_args = urlencode({
                    'tl': language,
                    'q': text
                })

                url = self.SPEECH_URL + encoded_args
                download_path = os.path.join(download_dir, text + self.DOWNLOAD_FILE_TYPE)

                downloader = SpeechDownloader(url, self.REQUEST_HEADER, download_path)
                # Pool().apply() blocks until the process is finished
                # pool.apply(downloader.download)
                pool.apply_async(downloader.download, callback=update_progress)

            # Prevents any more tasks from being submitted to the pool
            pool.close()
            # Wait for the worker process to exit
            pool.join()

            print 'Done, Downloaded %d Speeches' % len(results)


def main():
    options = parse_args(CWD)
    service = SpeechDownloadService(options.lang, options.dir)
    service.start()


if __name__ == '__main__':
    main()
