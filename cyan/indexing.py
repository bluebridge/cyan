import datetime
import os


class IndexingBase:
    file_name = ''

    def __init__(self, file_name: str):
        self.file_name = file_name

    def get_last_modified_date(self):
        try:
            modified_time = os.path.getmtime(self.file_name)
        except OSError:
            modified_time = 0

        if modified_time == 0:
            return None

        return datetime.datetime.fromtimestamp(modified_time).date()

    def is_indexed(self, index_name: str):
        is_expired = self.is_file_expired()

        if is_expired:
            try:
                os.remove(self.file_name)
            except OSError:
                pass

            return False

        with open(self.file_name, 'r') as logfile:
            file_lines = logfile.readlines()
            res = list(filter(lambda x: index_name in x, file_lines))

            if len(res) == 0:
                return False

            return True

    def is_file_expired(self):
        last_modified_date = self.get_last_modified_date()
        current_date = datetime.datetime.now().date()

        if last_modified_date is None:
            return True

        return last_modified_date < current_date

    def log_indexing(self, index_name: str):
        with open(self.file_name, 'a') as logfile:
            logfile.write("%s\n" % index_name)

    def index(self, index_name: str, indexing_callback):
        # if not index_name:
        #     return

        is_indexed = not index_name or self.is_indexed(index_name)

        if is_indexed:
            return

        # self.run_index(index_name)
        indexing_callback()
        self.log_indexing(index_name)

    def run_index(self, index_name: str):
        print('indexing, dude')
