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
        9: 2,       # RBASE (P1)
        99: 1       # HALT
    }

    debug = False

    def __init__(self, memorySize):

        self.__instrptr: int = 0
        self.__relativeBase: int = 0
        self.__halt = False
        self.__memory = [0 for x in range(0, memorySize)]
        self.__input_buffer = []
        self.__output_buffer = []
        self.last_output = 0

    def load(self, program):
        #buffer1[pos:pos+len(buffer2)] = buffer2
        self.__memory_writebuffer(0, program)

    def run(self):
        while(self.step()):
            pass
        return self.__output_buffer

    def step(self):
        if(self.__halt):
            return False
        instr = self.__instr_next()
        op = self.__instr_op(instr)
        if(self.debug):
            print(f"Instruction: {op}, InstrPtr: {self.__instrptr}")
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
        elif op == 9:
            self.__op_adjustrelbase(modes, self.__instr_nextn(params))
        elif op == 99:
            self.__op_halt(modes, self.__instr_nextn(params))
            return False
        if(self.debug):
            print(f"Output Buffer: {self.__output_buffer}")
        return True

    def is_done(self):
        return self.__halt

    def input_add(self, queue):
        if type(queue) in [list, tuple]:
            self.__input_buffer.extend(queue)
        else:
            self.__input_buffer.append(queue)

    def __input_pop(self):
        if(self.__input_count() > 0):
            val = self.__input_buffer[0]
            self.__input_buffer = self.__input_buffer[1:]
            return val
        return None

    def __input_count(self):
        return len(self.__input_buffer)

    def output_pop(self):
        if(self.output_count() > 0):
            val = self.__output_buffer[0]
            self.__output_buffer = self.__output_buffer[1:]
            return val
        return None

    def output_get(self):
        return self.__output_buffer.copy()

    def output_count(self):
        return len(self.__output_buffer)

    """
    *********************************
    Instruction Pointer
    *********************************
    """

    def __instr_next(self):
        instr = self.__memory[self.__instrptr]
        self.__instrptr += 1
        return instr

    def __instr_nextn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.__instr_next())
        return args

    def __instr_peek(self):
        return self.__memory[self.__instrptr]

    def __instr_peekn(self, n):
        args = []
        for i in range(0, n):
            args.append(self.__memory[self.__instrptr + i])
        return args

    def __instr_set(self, addr):
        self.__instrptr = addr

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
        if(index >= len(self.__memory)):
            raise IndexError(index, "buffer overrun")
        self.__memory[index] = value

    def __memory_writebuffer(self, index, buffer):
        self.__copy_buffer(buffer, self.__memory, 0, len(buffer))

    def __memory_read(self, index):
        if(index >= len(self.__memory)):
            raise IndexError(index, "buffer overrun")
        return self.__memory[index]

    def __memory_moderead(self, mode, value):
        if(mode == 2):
            return self.__memory_read(self.__relativeBase + value)
        elif(mode == 1):
            return value
        else:
            return self.__memory_read(value)

    def __memory_dump(self):
        return self.__memory

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

        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        reg = params[2]  # write parameters are always in position mode

        val = p1 + p2
        self.__memory_write(reg, val)
        if(self.debug):
            print(f"[OP] ADD({p1},{p2}) = {val} into [{reg}]")

    def __op_mult(self, modes, params):
        """ 
        Opcode 2 is multiply:
            multiply the first two parameter values and store the result in the position stored in the third parameter
        """
        # expecting 3 parameters
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        reg = params[2]  # write parameters are always in position mode

        val = p1 * p2
        self.__memory_write(reg, val)
        if(self.debug):
            print(f"[OP] MULT({p1},{p2}) = {val} into [{reg}]")

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
        if(self.debug):
            print(f"[OP] INPUT({inputValue}) into [{p1}]")

    def __op_output(self, modes, params):
        """
        Opcode 4 is output:
            outputs the value of its only parameter. 
        """
        if len(params) != 1:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        self.last_output = p1
        self.__output_buffer.append(p1)
        if(self.debug):
            print(f"[OP] OUTPUT({p1})")

    def __op_jumptrue(self, modes, params):
        """ 
        Opcode 5 is jump-if-true:
            if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter.
            Otherwise, it does nothing.
        """
        if len(params) != 2:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        if p1 != 0:
            self.__instr_set(p2)
        if(self.debug):
            print(f"[OP] JMPT({p1}) = {p1 != 0} update instruction pointer to [{p2}]")

    def op_jumpfalse(self, modes, params):
        """
        Opcode 6 is jump-if-false: 
            if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. 
            Otherwise, it does nothing.
        """
        if len(params) != 2:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        if p1 == 0:
            self.__instr_set(p2)
        if(self.debug):
            print(f"[OP] JMPF({p1}) = {p1 == 0} update instruction pointer to [{p2}]")

    def __op_lessthan(self, modes, params):
        """
        Opcode 7 is less than: 
            if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
        """
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        reg = params[2]  # write parameters are always in position mode
        val = 0
        if p1 < p2:
            val = 1
        self.__memory_write(reg, val)
        if(self.debug):
            print(f"[OP] LESS-THAN({p1}) = {p1 < p2} update to {val} reg [{reg}]")

    def __op_equals(self, modes, params):
        """
        Opcode 8 is equals: 
            if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. 
            Otherwise, it stores 0.
        """
        if len(params) != 3:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        p2 = self.__memory_moderead(modes.get(1), params[1])
        reg = params[2]  # write parameters are always in position mode
        val = 0
        if p1 == p2:
            val = 1
        self.__memory_write(reg, val)
        if(self.debug):
            print(f"[OP] EQUALS({p1}) = {p1 == p2} update to {val} reg [{reg}]")


    def __op_adjustrelbase(self, modes, params):
        """
        Opcode 9 adjusts the relative base:
            the relative base increases (or decreases, if the value is negative) by the value of the parameter.
        """
        if len(params) != 1:
            raise ValueError(params)
        p1 = self.__memory_moderead(modes.get(0), params[0])
        self.__relativeBase += p1
        if(self.debug):
            print(f"[OP] RBASE({p1}) updated to {self.__relativeBase}")

    def __op_halt(self, modes, params):
        self.__halt = True
        if(self.debug):
            print(f"[OP] HALT")

    """
    *********************************
    Utilities
    *********************************
    """

    def __copy_buffer(self, from_buffer, to_buffer, start, length):
        if type(from_buffer) in [list, tuple]:
            to_buffer[start:start+length] = from_buffer.copy()
        else:
            raise ValueError(
                from_buffer, "can only write a list or tuple")
