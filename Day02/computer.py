class Computer:

    instrptr: int = 0               # Instruction Pointer
    memory = []                     # memory
    ops = {1: 4, 2: 4, 99: 1}       # OpCodes {code: parameter count }

    def __init__(self, memory=[]):
        if len(memory) > 0:
            self.memory = memory.copy()

    def run(self):
        op = self.instr_next()
        while(op != 99):
            #print('op: ', op)
            params = self.ops.get(op)
            #print('params count', params)
            if params == None:
                # Unknown OpCode
                raise ValueError(op)
            params -= 1
            if op == 1:
                self.op_add(self.instr_nextn(params))
            elif op == 2:
                self.op_mult(self.instr_nextn(params))
            elif op == 99:
                return
            op = self.instr_next()

    def instr_next(self):
        instr = self.memory[self.instrptr]
        self.instrptr += 1
        return instr

    def instr_nextn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.instr_next())
        return args

    def memory_write(self, index, value):
        self.memory[index] = value

    def memory_read(self, index):
        return self.memory[index]

    def memory_dump(self):
        return self.memory

        # Operations

    def op_add(self, params):
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.memory_read(params[0])
        p2 = self.memory_read(params[1])
        reg = params[2]

        val = p1 + p2
        #print(f"putting {val} to index {reg} ")
        self.memory_write(reg, val)

    def op_mult(self, params):
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.memory_read(params[0])
        p2 = self.memory_read(params[1])
        reg = params[2]

        val = p1 * p2
        #print(f"putting {val} to index {reg} ")
        self.memory_write(reg, val)
