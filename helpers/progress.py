from datetime import datetime
import sys


class Progress(object):

    def __init__(self, total_count, bar_length=30):

        self.total_count = total_count
        self.bar_length = bar_length
        self.start_time = datetime.now()

    def update(self, current_count):

        status = ''
        progress = (current_count / float(self.total_count))
        completed = int(round(self.bar_length * progress))

        if progress >= 1:

            progress = 1.0

            total_time = datetime.now() - self.start_time
            average_time = total_time / self.total_count

            status = 'Done\n'
            status += 'Total Tasks: ' + str(self.total_count) + '\n'
            status += 'Total Time: ' + str(total_time) + '\n'
            status += 'Average Time: ' + str(average_time) + '\n'

        text = '\r' + 'Progress: [{0}] {1}% {2}'.format(
            '#' * completed + '-' * (self.bar_length - completed),
            round(progress * 100, 1),
            status
        )

        sys.stdout.write(text)
        sys.stdout.flush()
