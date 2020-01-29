from collections import deque


class Computer:

    ops = {
        # OpCodes {code: parameter count including instruction }
        1: 4,       # ADD(P1,P2,DEST)
        2: 4,       # MULT(P1,P2,DEST)
        3: 2,       # INPUT(DEST)
        4: 2,       # OUTPUT(SOURCE)
        5: 3,       # JUMP-TRUE (CONDITION != 0,DEST)
        6: 3,       # JUMP-FALSE (CONDITION == 0,DEST)
        7: 4,       # LESS-THAN (P1,P2,DEST)
        8: 4,       # EQUAL (P1,P2,DEST)
        99: 1       # HALT
    }

    def __init__(self, memory=[]):

        self.debug = False
        self.instrptr: int = 0               # Instruction Pointer
        self.memory = []                     # memory
        # load input which will be read sequentially upon read instruction
        self.__input_queue = []
        self.__output_queue = []
        self.last_output = 0
        self.__halt = False

        if len(memory) > 0:
            self.memory = memory.copy()

    def run(self):
        while(self.step()):
            pass
        return self.__output_queue

    def step(self):
        if(self.__halt):
            return False
        instr = self.__instr_next()
        op = self.__instr_op(instr)
        if(self.debug):
            print(f"Instruction: {op}")
            print('ptr: ', self.instrptr)
        params = self.ops.get(op)
        if params == None:
            # Unknown OpCode
            raise ValueError(op, "Invalid opcode")
        params -= 1
        modes = self.__instr_modes(instr, params)
        if op == 1:
            self.__op_add(modes, self.__instr_nextn(params))
        elif op == 2:
            self.__op_mult(modes, self.__instr_nextn(params))
        elif op == 3:
            self.__op_input(modes, self.__instr_nextn(params))
        elif op == 4:
            self.__op_output(modes, self.__instr_nextn(params))
        elif op == 5:
            self.__op_jumptrue(modes, self.__instr_nextn(params))
        elif op == 6:
            self.op_jumpfalse(modes, self.__instr_nextn(params))
        elif op == 7:
            self.__op_lessthan(modes, self.__instr_nextn(params))
        elif op == 8:
            self.__op_equals(modes, self.__instr_nextn(params))
        elif op == 99:
            self.__halt = True
            return False
        return True

    def is_done(self):
        return self.__halt

    def input_add(self, queue):
        if type(queue) in [list, tuple]:
            self.__input_queue.extend(queue)
        else:
            self.__input_queue.append(queue)

    def __input_pop(self):
        if(self.__input_count() > 0):
            val = self.__input_queue[0]
            self.__input_queue = self.__input_queue[1:]
            return val
        return None

    def __input_count(self):
        return len(self.__input_queue)

    def output_pop(self):
        if(self.output_count() > 0):
            val = self.__output_queue[0]
            self.__output_queue = self.__output_queue[1:]
            return val
        return None

    def output_count(self):
        return len(self.__output_queue)

    """
    *********************************
    Instruction Pointer
    *********************************
    """

    def __instr_next(self):
        instr = self.memory[self.instrptr]
        self.instrptr += 1
        return instr

    def __instr_nextn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.__instr_next())
        return args

    def __instr_peek(self):
        return self.memory[self.instrptr]

    def __instr_peekn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.memory[self.instrptr + i])
        return args

    def __instr_set(self, addr):
        self.instrptr = addr

    def __instr_op(self, instr):
        return int(str(instr)[-2:])

    def __instr_modes(self, instr, params: int):
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

    """
    *********************************
    Memory
    *********************************
    """

    def __memory_write(self, index, value):
        if(index >= len(self.memory)):
            raise IndexError(index, "buffer overrun")
        self.memory[index] = value

    def __memory_read(self, index):
        if(index >= len(self.memory)):
            raise IndexError(index, "buffer overrun")
        return self.memory[index]

    def __memory_dump(self):
        return self.memory

    """
    *********************************
    Operations
    *********************************
    """

    def __op_add(self, modes, params):
        """ 
        Opcode 1 is add:
            add the first two parameter values and store the result in the position stored in the third parameter
        """
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.__memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]  # write parameters are always in position mode

        val = p1 + p2
        # print(f"putting {val} to index {reg} ")
        self.__memory_write(reg, val)

    def __op_mult(self, modes, params):
        """ 
        Opcode 2 is multiply:
            multiply the first two parameter values and store the result in the position stored in the third parameter
        """
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.__memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]  # write parameters are always in position mode

        val = p1 * p2
        # print(f"putting {val} to index {reg} ")
        self.__memory_write(reg, val)

    def __op_input(self, modes, params):
        """
        Opcode 3 is input:
            take a single integer as input and saves it to the position given by its only parameter. 
        """
        if len(params) != 1:
            raise ValueError(params)
        p1 = params[0]  # write parameters are always in position mode
        inputValue = ""
        if self.__input_count() > 0:
            inputValue = self.__input_pop()
        else:
            inputValue = input("Input:")
        self.__memory_write(p1, int(inputValue))

    def __op_output(self, modes, params):
        """
        Opcode 4 is output:
            outputs the value of its only parameter. 
        """
        if len(params) != 1:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        self.last_output = p1
        self.__output_queue.append(p1)

    def __op_jumptrue(self, modes, params):
        """ 
        Opcode 5 is jump-if-true:
            if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
            Otherwise, it does nothing.
        """
        if len(params) != 2:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        if p1 != 0:
            p2 = self.__memory_read(params[1]) if modes.get(
                1) == 0 else params[1]
            self.__instr_set(p2)

    def op_jumpfalse(self, modes, params):
        """
        Opcode 6 is jump-if-false: 
            if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. 
            Otherwise, it does nothing.
        """
        if len(params) != 2:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        if p1 == 0:
            p2 = self.__memory_read(params[1]) if modes.get(
                1) == 0 else params[1]
            self.__instr_set(p2)

    def __op_lessthan(self, modes, params):
        """
        Opcode 7 is less than: 
            if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
        """
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.__memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]  # write parameters are always in position mode
        if p1 < p2:
            self.__memory_write(reg, 1)
        else:
            self.__memory_write(reg, 0)

    def __op_equals(self, modes, params):
        """
        Opcode 8 is equals: 
            if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
        """
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_read(params[0]) if modes.get(0) == 0 else params[0]
        p2 = self.__memory_read(params[1]) if modes.get(1) == 0 else params[1]
        reg = params[2]  # write parameters are always in position mode
        if p1 == p2:
            self.__memory_write(reg, 1)
        else:
            self.__memory_write(reg, 0)
