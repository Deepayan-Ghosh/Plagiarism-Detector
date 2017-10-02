from three_way_detector import three_way_detector


class Reader:
    def __init__(self):
        self.src_file_name = ''
        self.doc_file = ''
        self.src_content = ''
        self.doc_content = ''
        self.detector = None

    def set_filename(self, file_name, doc_name):
        self.src_file_name = file_name
        self.doc_file = doc_name
        return self

    def read(self):
        with open(self.src_file_name, 'r') as f:
            self.src_content = f.read()
        with open(self.doc_file, 'r') as f:
            self.doc_content = f.read()
        return self.detect()

    def set_content(self, text1, text2):
        self.src_content = str(text1)
        self.doc_content = str(text2)
        return self.detect()

    def detect(self):
        self.detector = three_way_detector(self.src_content.upper(), self.doc_content.upper())
        final_index_list, common_words_list = self.detector.execute()
        src_list, doc_list = [], []
        src_index_list = []

        for each in self.src_content.upper().split():
            ch = each[len(each) - 1]
            if not 'A' <= ch <= 'Z':
                src_list.append(each[:len(each) - 1])
            else:
                src_list.append(each)

        for each in self.doc_content.upper().split():
            ch = each[len(each) - 1]
            if not 'A' <= ch <= 'Z':
                doc_list.append(each[:len(each) - 1])
            else:
                doc_list.append(each)

        for each in final_index_list:
            start = self.src_content.index(self.doc_content[each[0]:each[1]])
            end = start + (each[1] - each[0])
            src_index_list.append((start, end))

        print src_index_list

        src_size = len(src_list)
        doc_size = len(doc_list)

        b = len(common_words_list)
        plag_percent_1 = (b / float(src_size)) * 100
        plag_percent_2 = (b / float(doc_size)) * 100

        print plag_percent_1, plag_percent_2
        return src_index_list, final_index_list, plag_percent_1, plag_percent_2


if __name__ == "__main__":
    reader_obj = Reader()
    reader_obj.set_filename('b.txt', 'b.txt').read()
    # reader_obj.read()
