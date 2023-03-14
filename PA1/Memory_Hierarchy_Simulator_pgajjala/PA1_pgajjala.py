import math
import numpy as np


def read_strings(line): # This function is to parse the file

    strings = line.split(':')[0].strip()
    return strings


def read_numbers(line): # This function is to parse the file

    numbers = int(line.split(':')[-1].strip())
    return numbers


def read_policy(line): # This function is to parse the file

    policy = line.split(':')[-1].strip()
    return policy


def string_to_int(hex_val): # This function is to convert hexadecimal to integer

    hex_to_int = int("0x"+hex_val, 16)
    return hex_to_int       


def right_shift(arr, string, new_tag): # This function is to right shift the bits 

    arr[1:(string+1)] = arr[0:string]
    arr[0] = new_tag
    return arr


def find_index(arr, index): 

    for (string,item) in enumerate(arr):
        
        if item == index:
            
            return string


def get_miss_hit(arr, tag):  # This function is to label hit and miss

    result = " "

    if tag in arr: # for hit

        result = "hit"
        string = find_index(arr, tag)
        arr = right_shift(arr, string, tag)
        
        return arr, result

    else: # for miss
        
        result = "miss"

        if -1 in arr:
            
            string = find_index(arr, -1)
            arr[string] = tag
            
        else: 
            
            string = len(arr)-1
            arr = right_shift(arr, string, tag)
        
        return arr, result


def findMin(arr): 
    
    min = arr[0]
    i = 0
    j = 0
    
    for ele in arr:
        
        if min >= ele:
            
            min = ele
            j = i
        i = i + 1
    
    return j, min


# Data Translation Lookaside Buffer

class DataTranslationLookasideBuffer():
    
    def __init__(self, ):
        
        self.sets = 0
        self.associativityciativity = 0
        self.index = 0

    def read(self, path_to_config_file):

        f = open(path_to_config_file, 'r')
        lines = f.readlines()
        
        for (string, line) in enumerate(lines):
            
            line = line.strip()                
            
            if (line.startswith("Data TLB configuration")):
                
                self.sets = read_numbers(lines[string+1])
                self.associativity = read_numbers(lines[string+2])
                self.index = int(math.log2(self.sets))
                
                print("\n")

                print("Data TLB contains " + str(self.sets)+" sets.\n", )
                print("Each set contains " + str(self.associativity)+" entries.\n")
                print("Number of bits used for the index is " + str(self.index)+".\n\n")
                
                break;

# Page Table 

class PageTable():
    
    def __init__(self, ):
        
        self.virtual_pagenum = 0
        self.physical_pagenum = 0
        self.pagesize = 0
        self.index = 0
        self.offset = 0

    def read(self, path_to_config_file):
        
        f = open(path_to_config_file, 'r')
        lines = f.readlines()
        
        for (string, line) in enumerate(lines):
            
            line = line.strip()   
            
            if (line.startswith("Page Table configuration")):
                
                self.virtual_pagenum = read_numbers(lines[string+1])
                self.physical_pagenum = read_numbers(lines[string+2])
                self.pagesize = read_numbers(lines[string+3])

                self.index = int(math.log2(self.virtual_pagenum))
                self.offset = int(math.log2(self.pagesize))

                print("Number of virtual pages is "+str(self.virtual_pagenum)+".\n")
                print("Number of physical pages is "+str(self.physical_pagenum)+".\n")
                print("Each page contains "+str(self.pagesize)+".bytes.\n")
                print("Number of bits used for the page table index is "+str(self.index)+".\n")
                print("Number of bits used for the page offset is "+str(self.offset)+".\n\n")
                
                f.close() 
                
                break;    


# Find index in Page Table

def pageTable_findIndex(arr, item):
   
    k = 0

    for i in arr:
        
        if i == item:
            
            return k
        
        k = k + 1


# Hits and Misses for Page Table

def pageTable_result(item, arr_bits, count_bits):

    if item in arr_bits: # hit
        
        pt_result = "hit"
        string = pageTable_findIndex(arr_bits, item)
        count_bits[string] = count_bits[string] + 1
        
        return arr_bits, count_bits, string, pt_result

    else: # miss
        
        pt_result = "miss"

        if "-1" in arr_bits:
            
            string = pageTable_findIndex(arr_bits, "-1")
            arr_bits[string] = item
            count_bits[string] = count_bits[string] + 1
        
        else: 
            
            j, min = findMin(count_bits)
            string = j
            arr_bits[string] = item
            count_bits[string] = 0
        
        return arr_bits, count_bits, string, pt_result

# Data Cache (L1 Cache)

class DataCache():
    
    def __init__(self, ):
        
        self.sets = 0
        self.associativity = 0
        self.block_size = 0
        self.policy = None
        self.index = 0
        self.offset = 0

    def read(self, path_to_config_file):
        
        f = open(path_to_config_file, 'r')
        lines = f.readlines()
        
        for (string, line) in enumerate(lines):
            
            line = line.strip()   
            
            if (line.startswith("Data Cache configuration")):
                
                self.sets = read_numbers(lines[string+1])
                self.associativity = read_numbers(lines[string+2])
                self.block_size = read_numbers(lines[string+3])
                self.policy = read_policy(lines[string+4])
                self.index = int(math.log2(self.sets))
                self.offset = int(math.log2(self.block_size))

                print("D-cache contains "+str(self.sets)+" sets.\n")
                print("Each set contains "+str(self.associativity)+" entries.\n")
                print("Each line is "+str(self.block_size)+" bytes.\n")

                if (self.policy == "n"):
                    print("The cache uses a write-allocate and write-back policy.\n")
                else:
                    print("The cache not use a write-allocate and write-through policy.\n")

                print("Number of bits used for the index is "+str(self.index)+".\n")
                print("Number of bits used for the offset is "+str(self.offset)+".\n\n")
                

                f.close()

                break;

# L2 Cache

class L2Cache():
    
    def __init__(self, ):
       
        self.sets = 0
        self.associativity = 0
        self.block_size = 0
        self.policy = None
        self.index = 0
        self.offset = 0

    def read(self, path_to_config_file):
        f = open(path_to_config_file, 'r')
        lines = f.readlines()
        
        for (string, line) in enumerate(lines):
            
            line = line.strip()   
            
            if (line.startswith("L2 Cache configuration")):
                
                self.sets = read_numbers(lines[string+1])
                self.associativity = read_numbers(lines[string+2])
                self.block_size = read_numbers(lines[string+3])
                self.policy = read_policy(lines[string+4])

                self.index = int(math.log2(self.sets))
                self.offset = int(math.log2(self.block_size))

                print("L2-cache contains "+str(self.sets)+" sets.\n")
                print("Each set contains "+str(self.associativity)+" entries.\n")
                print("Each line is "+str(self.block_size)+" bytes.\n")

                if (self.policy == "n"):
                    print("The cache uses a write-allocate and write-back policy.\n")
                else:
                    print("The cache not use a write-allocate and write-through policy.\n")

                print("Number of bits used for the index is "+str(self.index)+".\n")
                print("Number of bits used for the offset is "+str(self.offset)+".\n\n")
                
                f.close()

                break;


class virtual_addresses():
    
    def __init__(self, ):
        
        self.virtual_addr = None
        self.tlb = None
        self.L2Cache = None
    
    def read(self, path_to_config_file):
        
        f = open(path_to_config_file, 'r')
        lines = f.readlines()
        
        for (string, line) in enumerate(lines):
            
            line = line.strip()   
            
            if (line.startswith("Virtual addresses")):
                
                self.virtual_addr = read_strings(lines[string])
                self.tlb = read_strings(lines[string+1])
                self.L2Cache = read_strings(lines[string+2])
                print("The addresses read in are virtual addresses.\n\n")
                
                f.close()

                break;

# Define the size of Physical Address and Virtual Address Bits

sizeof_physicaladdress = 32 #32 bits
sizeof_virtualaddress = 32 #32 bits

class data_for_table():
    
    def __init__(self, ):
        
        self.read_write=None 
        self.virtual_address=None 
        self.virtual_address_in_bits=None
        self.virtual_page=None 
        self.tlb_index=None 
        self.tlb_tag=None 
        self.page_offset=None 
        self.l2tag = None
        self.l2index = None
        
    def calculate(self, line, dtlb, pt, dc):
        
        self.read_write = line.split(':')[0]
        
        virt_addr = string_to_int(line.split(':')[1].replace('\n', ''))
        self.virtual_address_in_bits = format(int(bin(virt_addr),2),'b').zfill(sizeof_virtualaddress)
        self.virtual_address = format(virt_addr,'x').zfill(int(sizeof_virtualaddress/4))
        
        virtual_page = self.virtual_address_in_bits[:sizeof_virtualaddress-pt.offset]
        self.virtual_page = format(int(virtual_page,2),'x')

        self.tlb_tag = int(self.virtual_address_in_bits[:sizeof_virtualaddress-pt.offset-dtlb.index],2)
        self.tlb_index = int(self.virtual_address_in_bits[(-pt.offset-dtlb.index):-pt.offset],2)


if __name__ == "__main__":

    path_to_config_file = "/home/pgajjala/COSC530_FA22_pgajjala/Memory_Hierarchy_Simulator_pgajjala/trace.config"

    # Please replace the file with "long_trace.dat" if you want to check the working of the code on long trace file
    
    path_to_dat_file = "/home/pgajjala/COSC530_FA22_pgajjala/Memory_Hierarchy_Simulator_pgajjala/trace.dat" 
    data_in_file = open(path_to_dat_file, "r")

    dtlb = DataTranslationLookasideBuffer()
    dtlb.read(path_to_config_file)

    pt = PageTable()
    pt.read(path_to_config_file)

    dc = DataCache()
    dc.read(path_to_config_file)

    l2 = L2Cache()
    l2.read(path_to_config_file)

    virtual_addresses = virtual_addresses()
    virtual_addresses.read(path_to_config_file)
    
    DTLB_MAX = pow(2, dtlb.index) 
    tlb_res_array = np.full((DTLB_MAX,dtlb.associativity),-1, dtype="int") 
    pt_res_array = np.full((DTLB_MAX,pt.physical_pagenum),-1, dtype="int")
    tlb_tag_list = []

    arr_bits = np.full(pt.physical_pagenum, "-1")
    count_bits = np.array([0,0,0,0]) 

    print(
        "        Virtual      Virt.     Page    TLB     TLB      TLB     PT     Phys            DC  DC          L2  L2   \n" +
        "        Address      Page #    Off     Tag     Ind      Res.    Res.   Pg #   DC Tag   Ind Res. L2 Tag Ind Res. \n" +
        "---------------------------------------------------------------------------------------------------------------\n")



    for line in data_in_file.readlines():
        
        data = data_for_table()
        data.calculate(line, dtlb, pt, dc)
        
        tlb_res_array[data.tlb_index], tlb_result = get_miss_hit(tlb_res_array[data.tlb_index], data.tlb_tag)
        
        arr_bits, count_bits, py_bit, pt_result = pageTable_result(data.virtual_page, arr_bits, count_bits)
        
        if tlb_result == "hit":
            pt_result = " "

        py_ = format(int(bin(py_bit),2),'b') 
        dc_physical_address = py_ + data.virtual_address_in_bits[-pt.offset:]
        dc_index = format(int(dc_physical_address[-dc.offset-dc.index:-dc.offset],2),'x')
        dc_tag = format(int(dc_physical_address[:-dc.offset-dc.index],2),'x')

        table = [data.read_write, data.virtual_address, data.virtual_page, data.page_offset, data.tlb_tag, data.tlb_index, tlb_result, pt_result, py_bit, dc_tag, dc_index]

        for item in table:
            print(str(item), end = '\t')
        print("\n")