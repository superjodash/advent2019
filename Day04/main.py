input_start = 347312
input_end = 805915

def main():
    global input_start
    global input_end
    # #valid
    # print(is_num_valid(111111))
    # print(is_num_valid(122345))
    # print(is_num_valid(111123))
    # # invalid
    # print(is_num_valid(135679))
    # print(is_num_valid(223450))
    # print(is_num_valid(123789))
    count = 0
    curr = input_start
    while(curr <= input_end):
        if(is_num_valid(curr)):
            print(curr)
            count += 1
        curr += 1
    print (f"Total: {count}")

def is_num_valid(num):
    v = str(num)
    last = v[0]
    d = False
    for r in range(1, 6):
        lv = int(last)
        cu = int(v[r])
        if(cu < lv):
            return False # bail early if number decreases
        if(cu == lv and d == False):
            d = True # we have met the double criteria
        last = v[r]
    return d

main()