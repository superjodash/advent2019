class Computer:

    instrptr: int = 0               # Instruction Pointer
    memory = []                     # memory
    ops = {
        # OpCodes {code: parameter count }
        1: 4,       # ADD
        2: 4,       # MULT
        3: 2,       # INPUT
        4: 2,       # OUTPUT
        99: 1       # HALT
    }

    def __init__(self, memory=[]):
        if len(memory) > 0:
            self.memory = memory.copy()

    def run(self):
        instr = self.instr_next()
        op = self.instr_op(instr)
        #print(f"Instruction: {op}")
        while(op != 99):
            #print('ptr: ', self.instrptr)
            if self.instrptr == 221:
                self.instrptr = 221
            params = self.ops.get(op)
            # print('params count', params)
            if params == None:
                # Unknown OpCode
                raise ValueError(op, "Invalid opcode")
            params -= 1
            modes = self.instr_modes(instr, params)
            if op == 1:
                self.op_add(modes, self.instr_nextn(params))
            elif op == 2:
                self.op_mult(modes, self.instr_nextn(params))
            elif op == 3:
                self.op_input(modes, self.instr_nextn(params))
            elif op == 4:
                self.op_output(modes, self.instr_nextn(params))
            elif op == 99:
                return
            #self.instrptr += params
            instr = self.instr_next()
            op = self.instr_op(instr)

    def instr_op(self, instr):
        return int(str(instr)[-2:])

    def instr_modes(self, instr, params: int):
        sinstr = str(instr)
        sinstrl = len(sinstr)
        lo = len(sinstr[-2:])     
        ml = sinstrl - lo
        md = {}
        modes = sinstr[0:ml][::-1]  # get modes in reverse
        lmodes = len(modes)
        for i in range(0, params):
            if i < lmodes:
                md[i] = int(modes[i])
            else:
                md[i] = 0
        return md

    def instr_next(self):
        instr = self.memory[self.instrptr]
        self.instrptr += 1
        return instr

    def instr_nextn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.instr_next())
        return args

    def instr_peekn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.memory[self.instrptr + i])
        return args

    def memory_write(self, index, value):
        self.memory[index] = value

    def memory_read(self, index):
        return self.memory[index]

    def memory_dump(self):
        return self.memory

        # Operations

    def op_add(self, modes, params):
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]

        val = p1 + p2
        # print(f"putting {val} to index {reg} ")
        self.memory_write(reg, val)

    def op_mult(self, modes, params):
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]

        val = p1 * p2
        # print(f"putting {val} to index {reg} ")
        self.memory_write(reg, val)

    def op_input(self, modes, params):
        if len(params) != 1:
            raise ValueError(params)
        p1 = self.memory_read(params[0]) if modes.get(0) == 0 else params[0]
        self.memory_write(p1, int(input("Input:")))

    def op_output(self, modes, params):
        if len(params) != 1:
            raise ValueError(params)
        p1 = self.memory_read(params[0]) if modes.get(0) == 0 else params[0]
        print(f"[{p1}]")
