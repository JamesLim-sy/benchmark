import glob
import os
import sys
import argparse as ap
import functools
import collections

class FindPrevilFiles():
    def __init__(self, pd_path, bm_path):
        self.paddle_file_path = pd_path
        self.benchmark_file_path = bm_path
        self.paddle_files = None
        self.benchmark_files = None
        self.lack_tests = None

    def FindPrevilFileType(self, file_path): 
        if not os.path.exists(file_path):
            sys.exit(">>>[ERR]: Please enter an exist file path!\n")
        files = [os.path.splitext(item)[1] for item in os.listdir(file_path)]
        file_type_dict = collections.Counter(files)
        previl_type = list(filter(lambda x: file_type_dict[x] == 
                           max(file_type_dict.values()), file_type_dict.keys()))
        previl_filetype = previl_type[0]
        previl_files = [os.path.split(item.strip(previl_filetype))[1]  \
                            for item in os.listdir(file_path) if previl_filetype in item]
        return set(previl_files)

    def FindLackFiles(self):
        self.benchmark_files = self.FindPrevilFileType(self.benchmark_file_path)
        tmp_paddle_files     = self.FindPrevilFileType(self.paddle_file_path)
        self.paddle_files    = set(map(lambda x: x.split('_op')[0], tmp_paddle_files))
        self.lack_tests      = list(self.paddle_files - self.benchmark_files)

    def NoteDownResult(self) :
        result_name = self.benchmark_file_path[self.benchmark_file_path.rfind(r'/') + 1:] + '_lack.txt'
        with open(result_name, 'w') as fp:
            fp.write('[TODO]: untests OP below: \n')
            fp.write('\n'.join(self.lack_tests))
            fp.close()


if __name__ == '__main__' :
    parser = ap.ArgumentParser(description="To find the exists json config and test scripts in Benchmark system.")
    parser.add_argument('-paddle_path', default = None, help="To find current existing OP file in Paddle")
    parser.add_argument('-benchmark_path', default = None, help="To find current json configs or test scripts for OP test in Benchmark")
    args = parser.parse_args()

    file_collect = FindPrevilFiles(args.paddle_path, args.benchmark_path)
    file_collect.FindLackFiles()
    file_collect.NoteDownResult()
    print('Done!\n')
