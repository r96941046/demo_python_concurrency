import os
import optparse


def parse_args(CWD):
    usage = """
        usage: %prog [options]
    """
    parser = optparse.OptionParser(usage)

    help = 'The language of speech to get from text'
    parser.add_option('--lang', type='str', default='en', help=help)

    help = 'The task destination folder'
    parser.add_option('--dir', type='str', help=help)

    options, args = parser.parse_args()

    if len(args):
        parser.error('Bad Arguments')

    if options.dir[-1] != '/':
        options.dir += '/'

    download_path = os.path.join(CWD, options.dir)
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    return options
