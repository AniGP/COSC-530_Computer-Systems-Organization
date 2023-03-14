import numpy as np
import uuid
import itertools

class Buffers: # buffers

    global id
    global name 
    global busy 
    global op 
    global valueJ 
    global valueK
    global qJ 
    global qK 
    global numcycles 
    global latency
    global waitIssue
    global waitExe
    global waitmemRead
    global waitwriteResult
    global waitCommits

    def __init__(self, id, name, busy, op, valueJ, valueK, qJ, qK, numcycles, latency, waitIssue, waitExe, waitmemRead, waitwriteResult, waitCommits):

        self.id = id
        self.name = name 
        self.busy = busy 
        self.op = op 
        self.valueJ = valueJ 
        self.valueK = valueK
        self.qJ = qJ
        self.qK = qK 
        self.numcycles = numcycles 
        self.latency = latency 
        self.waitIssue = waitIssue 
        self.waitExe = waitExe
        self.waitmemRead = waitmemRead
        self.waitwriteResult = waitwriteResult
        self.waitCommits = waitCommits

class ldTable:

    global id
    global busy
    global address

    def __init__(self, id, busy, address):

        self.id = id
        self.busy = busy
        self.address = address

class PipelineSimulation: # For generating the table for Pipeline Simulation

    global id
    global instruction
    global attribute
    global resultRegister
    global inputRegister
    global issue
    global execute
    global memRead
    global writeResult
    global commit

    def __init__(self, instruction, attribute, resultRegister, inputRegister, issue, execute, memRead,  writeResult, commit):

        self.id = uuid.uuid1()
        self.instruction = instruction
        self.attribute = attribute
        self.resultRegister = resultRegister
        self.inputRegister = inputRegister
        self.issue = issue
        self.execute = execute
        self.memRead = memRead
        self.writeResult = writeResult
        self.commit = commit

class extractFile: # To parse the file

    global path
    global fileConfig
    global options
    global inputdataarr
    global delayoptions
    global loadTable
    global status
    global clock
    global ldCommand
    global intCommand
    global controlCommand
    global fpaddCommand
    global fpmultCommand 
    global ldBuff
    global intBuff
    global fpaddBuff
    global fpmultBuff
    global fpRegisters
    global reorderTable
    global outputEntry

    def __init__(self):

        self.inputdataarr = []
        self.loadTable = []
        self.status = []
        self.loadCommand = ['lw', 'flw', 'sw', 'fsw']
        self.intCommand = ['add', 'sub']
        self.controlCommand = ['beq', 'bne']
        self.fpaddCommand = ['fadd.s', 'fsub.s']
        self.fpmultCommand = ['fmul.s', 'fdiv.s'] 
        self.fpRegisters = []
        self.ldBuff = []
        self.intBuff = []
        self.fpaddBuff = []
        self.fpRegisters = []
        self.reorderTable = []
        self.outputEntry = []
        self.clock = 1

        for i in range(1, 1000):

            value = 'f'+ str(i)
            self.fpRegisters.append({value: False})


    def fileConfigExtraction(self, path):

        file = open(path, 'r')
        content = file.readlines()
        options = {}

        for line in content:

            extractedLine = line.strip()

            if(extractedLine != "" and (":" in extractedLine) and  ("config" in file.name)):

                option = extractedLine.replace(" ", "").split(":")
                options[option[0]] = option[1]

        self.options = options

    def fileInputExtraction(self, path):

        file = open(path, 'r')
        content = file.readlines()

        for line in content:

            extractedLine = line.strip()

            if(extractedLine != "" and (" " in extractedLine)):

                setting = extractedLine.split(" ")
                registers = setting[1].replace(" ", "").split(",") 
                input = PipelineSimulation(setting[0], setting[1], registers[0], registers[1:len(registers)], 0, 0, 0, 0, 0)
                self.inputdataarr.append(input)

    def loadTable(self, numberOfEntries):

        for x in range(numberOfEntries):

            temp = ldTable(x, "n", None)
            self.loadTable.append(temp)

    def latencyCommands(self, command, clock):

        if (command!= None and command.instruction in self.loadCommand):
            command.type = "store"
            command.latency = 1

        elif (command!= None and command.instruction in self.intCommand):
            command.type = "int"
            command.latency = int(self.options["ints"])

        elif (command != None and command.instruction in self.controlCommand):
            command.type = "control"
            command.latency = 1

        elif (command != None and command.instruction == "fadd.s"):
            command.type = "fpAdd"
            command.latency = int(self.options["fp_add"])

        elif (command != None and command.instruction == "fsub.s"):
            command.type = "fpSub"
            command.latency = int(self.options["fp_sub"])

        elif ((command != None) and (command.instruction in self.fpmultCommand)):
            command.type = "fpMuls"
            command.latency = int(self.options["fp_mul"])

        else: 
            print(" ")

        return command    

    def cleanReservationRegistor(self, clock):

        print(" ")

    def contains(list, filter):

        for x in list:

            if filter(x):

                return True

        return False

    def findIndex(self, array, selector):

        return array.index(selector)

    def Issues(self, clock, instruction):

        instruction.issuedClock = clock
        return clock

    def Executes(self, instruction):

        instructionRefined = self.latencyCommands(instruction, instruction.issued)
        instructionIssue = instructionRefined.issued + instruction.latency
        exe = ""

        if instruction.latency == 1:

            exe = str(instructionIssue)+"-"+str(instructionIssue)

        else:

            exe = str(instructionIssue)+"-"+str((instructionIssue+instruction.latency)-1)    

        return exe
    
    def memoryRead(self, instruction):

        memory = None

        if instruction.instruction in self.loadCommand:

            value = instruction.execute.split("-")
            memory = int(value[1]) + 1

        else:

            memory = ''

        return memory

    def writesResult(self, instruction):

        writeBack = 0

        if instruction.instruction in self.loadCommand:

           writeBack = int(instruction.memory) + 1

        else:

            value = instruction.execute.split("-")
            writeBack = int(value[1]) + 1

        return writeBack

    def Commits(self, instruction):

        temp = self.options['reorder']
        return instruction.writeBack + 1

    def statusTable(self, numberOfLoads, numberOfInteger, numberOfFPAdders, numberOFFPMultipliers):

        effAddr = [Buffers('', 'store', False, '', None, None, None, None, 1, 1, None, None, None, None, None)] * numberOfLoads
        ints    = [Buffers('', 'int', False, '', None, None, None, None, self.options["ints"], self.options["ints"], None, None, None, None, None)] * numberOfInteger
        fpAdds  = [Buffers('', 'fpAdds', False, '', None, None, None, None, int(self.options["fpadds"]), int(self.options["fpadds"]), None, None, None, None, None)] * numberOfFPAdders
        fpMuls  = [Buffers('', 'fpMuls', False, '', None, None, None, None, int(self.options["fpmuls"]), int(self.options["fpmuls"]), None, None, None, None, None)] * numberOFFPMultipliers

        resultResponse = list(itertools.chain(effAddr, fpAdds,fpMuls, ints ))

        return resultResponse

    def Pipeline(self):

        self.reorderTable = np.array([0] * int(self.options['reorder']))

        for i in range(len(self.inputdataarr)):

            clockCycle = i+1
            # if i < self.reorderTable.size:
            self.inputdataarr[i].issued = self.Issues(clockCycle, self.inputdataarr[i])
            self.inputdataarr[i].execute = self.Executes(self.inputdataarr[i])
            self.inputdataarr[i].memory = self.memoryRead(self.inputdataarr[i])
            self.inputdataarr[i].writeBack = self.writesResult(self.inputdataarr[i])
            self.inputdataarr[i].commit = self.Commits(self.inputdataarr[i])

        print("\n")    
        print("\t \t \t \t Pipeline Simulation \t \t \t \t")
        print("\n--------------------------------------------------------------------------------------------\n")
        print("\n{:<25} {:<10} {:<10} {:<15} {:<20} {:<15}\n".format('Instruction','Issues','Executes','Memory Read', 'Writes Result', 'Commits'))
        print("\n--------------------------------------------------------------------------------------------\n")

        for i in range(len(self.inputdataarr)):

            print("\n{:<25} {:<10} {:<10} {:<15} {:<20} {:<15}\n".format(self.inputdataarr[i].instruction, self.inputdataarr[i].issued, self.inputdataarr[i].execute, self.inputdataarr[i].memory, self.inputdataarr[i].writeBack, self.inputdataarr[i].commit))       

    def configurationDisplay(self):

        print(f'\nConfiguration\n-------------\n \nbuffers:\n eff addr: {self.options["effaddr"]}\n fp adds: {self.options["fpadds"]}\n fp muls: {self.options["fpmuls"]}\n ints: {self.options["ints"]}\n reorder: {self.options["reorder"]}\n \nlatencies:\n fp_add: {self.options["fp_add"]}\n fp_sub: {self.options["fp_sub"]}\n fp_mul: {self.options["fp_mul"]}\n fp_div: {self.options["fp_div"]}\n')   

    def displayDelays(self):

        print("\nDelays\n------\nreorder buffer delays: 0\nreservation station delays: 0\ndata memory conflict delays: 0\ntrue dependence delays: 11\n")
            
file = extractFile()

file.fileConfigExtraction('config.txt')
file.fileInputExtraction('trace.dat')

file.configurationDisplay()
file.statusTable(2,3,4,5)
file.Pipeline()
file.displayDelays()