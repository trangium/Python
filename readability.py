def f(i):
    is_prime = True
    for divisor in range(2, i):
        if i%divisor == 0:
            is_prime = False
    if is_prime: return i**2
    else: return divisor


# def f(i):
#    return i if any(i%divisor==0 for divisor in range(2, i)) else i**2
    

def generate_tests():
    return [(i, i**2) if i in [1, 9, 3, 5, 7] \
            else (i, i) for i in range(10)]

def run_tests():
    for (i, o) in generate_tests():
        try:
            assert f(i)==o
        except:
            print (f"failed test case: {i} => {o}")
            print (f"f({i}) instead returned: {f(i)}")
            assert False
    print("All tests passed.")

def validate_tests():
    inputs = [i for (i,o) in generate_tests()]
    if len(inputs)!=len(set(inputs)):
        print("Test inputs are not unique!")
        print(sorted(inputs))
        assert False

if __name__ == "__main__":
    validate_tests()
    run_tests()
