input_start = 347312
input_end = 805915


def main():
    run()
    # runTests()


def run():
    global input_start
    global input_end
    count = 0
    curr = input_start
    while(curr <= input_end):
        if(is_num_valid(curr)):
            print(curr)
            count += 1
        curr += 1
    print(f"Total: {count}")


def runTests():
    # valid

    print("Should be VALID (TRUE)")
    print("122345:", is_num_valid(122345))
    print("112233:", is_num_valid(112233))
    print("111122:", is_num_valid(111122))
    print("357788:", is_num_valid(357788))
    print("777899:", is_num_valid(777899))
    print("778888:", is_num_valid(778888))
    print("788999:", is_num_valid(788999))

    # invalid

    print("", "Should be INVALID (FALSE)")
    print("111111:", is_num_valid(111111))
    print("111123:", is_num_valid(111123))
    print("135679:", is_num_valid(135679))
    print("223450:", is_num_valid(223450))
    print("123789:", is_num_valid(123789))
    print("123444:", is_num_valid(123444))
    print("357778:", is_num_valid(357778))
    print("357779:", is_num_valid(357779))
    print("777888:", is_num_valid(777888))
    print("777779:", is_num_valid(777779))
    print("799999:", is_num_valid(799999))

    """Rules
        # Six digits
        # Numbers must be 347312 <= X <= 805915
        # Numbers must never decrease from left to right
        # There must be at least one pair of numbers
        # Numbers that appear in groups do not count toward the "pair" condition
    """


def is_num_valid(num):
    numVal = str(num)
    last = numVal[0]
    consecutive = 1
    doubles = 0
    for r in range(1, 6):
        lastit = r == 5  # last iteration
        lastVal = int(last)
        curVal = int(numVal[r])
        if(curVal < lastVal):
            return False  # bail early if number decreases
        if(curVal == lastVal):
            consecutive += 1
        else:
            if consecutive == 2:
                doubles += 1
            consecutive = 1

        if lastit and consecutive == 2:
            doubles += 1

        # if(lastit and consecutive > 1 and consecutive % 2 != 0):
            # bail because we have uneven pairs
            # return [False, "uneven", consecutive, lastVal, curVal]
        #    return False
        last = numVal[r]
    # return [doubles > 0, consecutive, lastVal, curVal]
    return doubles > 0


main()
