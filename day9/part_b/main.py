import click

class File:
    def __init__(self, file_id, file_space, empty_space):
        self.file_id = file_id
        self.file_space = file_space
        self.empty_space = empty_space

class FileSystem:
    def __init__(self, input_list):
        self.files = []
        if len(input_list) % 2 != 0:
            input_list.append(0)
        for i in range(0, len(input_list), 2):
            self.files.append(File(i // 2, input_list[i], input_list[i + 1]))
        for i, file_ in enumerate(self.files):
            if file_.empty_space > 0:
                self.first_space = i
                break
        self.backwards_counter = 1

    def __str__(self):
        repres = ""
        for file_ in self.files:
            repres += str(file_.file_id) * file_.file_space + '.' * file_.empty_space
        return repres

    def next_empty_space(self):
        for i in range(self.first_space, len(self.files)):
            if self.files[i].empty_space > 0:
                self.first_space = i
                break

    def defrag(self):
        last_id = self.files[-1].file_id
        first_empty_space = self.files[self.first_space].empty_space
        first_file_space = self.files[self.first_space].file_space
        first_file_id = self.files[self.first_space].file_id
        last_empty_space = self.files[-self.backwards_counter].empty_space
        last_file_space = self.files[-self.backwards_counter].file_space
        last_file_id = self.files[-self.backwards_counter].file_id
        for i, file_ in enumerate(self.files[:-self.backwards_counter]):
            if file_.empty_space >= last_file_space:
                self.files[-self.backwards_counter - 1].empty_space += self.files[-self.backwards_counter].file_space + self.files[-self.backwards_counter].empty_space
                new_file = self.files.pop(-self.backwards_counter)
                self.files.insert(i + 1, File(new_file.file_id, new_file.file_space, file_.empty_space - new_file.file_space))
                file_.empty_space = 0
                break
        self.backwards_counter += 1

    def full_defrag(self):
        while True:
            self.defrag()
            if self.backwards_counter > len(self.files):
                break

    def checksum(self):
        repres = []
        for file_ in self.files:
            repres += [file_.file_id] * file_.file_space + [0] * file_.empty_space
        result = 0
        for i, x in enumerate(repres):
            result += i * x
        return result
            
@click.command()
@click.option('-i', '--input-file', help='Input data file')
def main(input_file):
    with open(input_file) as fd:
        data = list(fd.read().strip())
        data = [int(x) for x in data]
    fs = FileSystem(data)
    fs.full_defrag()
    print(fs)
    print(fs.checksum())

if __name__ == '__main__':
    main()
