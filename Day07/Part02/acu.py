from computer import Computer

class AmplifierControlUnit:

    ampUnits = []
    ampCount = 0
    signal = 0

    def __init__(self, sequence, firmware):
        for a in range(0, len(sequence)):
            cx = Computer(firmware)
            v = sequence[a]
            cx.input_add(v)
            self.ampUnits.append(cx)
        self.ampCount = len(self.ampUnits)

    def run(self):
        ampptr = 0
        running = True
        while(running):
            last = ampptr == self.ampCount - 1
            amp = self.ampUnits[ampptr]
            res = self.__runAmp(amp)
            if(last and res):
                running = False
            ampptr = (ampptr + 1) % self.ampCount
        return self.signal

    def __runAmp(self, cx):
        if(cx.is_done()):
            return True

        cx.input_add(self.signal)
        while(cx.step()):
            if(cx.output_count() > 0):
                self.signal = cx.output_pop()
                break
        return cx.is_done()