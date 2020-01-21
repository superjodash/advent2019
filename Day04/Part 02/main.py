input_start = 347312
input_end = 805915


def main():
    global input_start
    global input_end
    # #valid
    print("Should be VALID (TRUE)")
    print(is_num_valid(111111))
    print(is_num_valid(122345))
    print(is_num_valid(111123))
    print(is_num_valid(112233))
    print(is_num_valid(111122))
    # invalid
    print("Should be INVALID (FALSE)")
    print(is_num_valid(135679))
    print(is_num_valid(223450))
    print(is_num_valid(123789))
    print(is_num_valid(123444))

    # count = 0
    # curr = input_start
    # while(curr <= input_end):
    #     if(is_num_valid(curr)):
    #         print(curr)
    #         count += 1
    #     curr += 1
    # print(f"Total: {count}")


def is_num_valid(num):
    v = str(num)
    last = v[0]
    consecutive = 1
    for r in range(1, 6):
        lv = int(last)
        cv = int(v[r])
        if(cv < lv):
            return False  # bail early if number decreases
        if(cv == lv):
            consecutive += 1
        else:
            if(consecutive % 2 != 0):
                return False  # bail because we have uneven pairs
            else:
                consecutive = 1
        last = v[r]
    return True


main()
