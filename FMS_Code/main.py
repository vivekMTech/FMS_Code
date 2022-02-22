import asyncio  # asyncio for concurrency files process.
import random  # random for generating strings and length


class FMS:
    def __init__(self):
        self.const_string = 'MARUTI'  # take constant keyword as 'MARUTI'

    # generating random string
    async def generate_string(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # using chars variable, we generate random string
        string_len = random.randint(5, 20)  # generate random string len
        seq = [''.join(random.choices(chars, k=string_len)),
               self.const_string]  # sequence list with random and const string
        return ''.join(random.choices(seq))  # generate string from sequence and return it

    # write random strings in files
    async def write_random_strings(self, file_name):
        file_descriptor = open(file_name, "a+")  # file descriptor for file
        gen_string = await self.generate_string()  # generate string using generate_string() Coroutine
        file_descriptor.write(gen_string + "\n")  # write string in file
        file_descriptor.close()

    # count 'MARUTI' keyword from files
    async def count_keyword(self, file_name):
        with open(file_name, 'r') as file:  # open file in read mode
            file_content = file.read(-1)  # -1 means read whole file content
            count = file_content.count(self.const_string)  # count 'MARUTI' keyword from content
        return count

    # write counts in counts.log
    async def write_counts(self, file_name1, file_name2):
        count_task_file1 = asyncio.create_task(self.count_keyword(file_name1))  # task is count from file1
        count_task_file2 = asyncio.create_task(self.count_keyword(file_name2))  # task is count from file2
        count_file1, count_file2 = await asyncio.gather(count_task_file1, count_task_file2)

        file_descriptor = open("counts.log", "w+")  # open file descriptor in write mode
        file_descriptor.write("{} -> {}\n".format(file_name1, count_file1))  # write count of file1 in 'count.log'
        file_descriptor.write("{} -> {}\n".format(file_name2, count_file2))  # write count of file2 in 'count.log'
        file_descriptor.close()


# define flow of coroutines
async def main():
    fms_obj = FMS()  # FMS object for accessing coroutines
    while True:
        write_file1 = asyncio.create_task(
            fms_obj.write_random_strings("file1.txt"))  # call write_random_strings() for file1
        write_file2 = asyncio.create_task(
            fms_obj.write_random_strings("file2.txt"))  # call write_random_strings() for file2
        write_count_log = asyncio.create_task(fms_obj.write_counts("file1.txt", "file2.txt"))  # call write in count.log
        await asyncio.gather(write_file1, write_file2, write_count_log, return_exceptions=True)


asyncio.run(main())  # event loop for running main() method
