def decimal_to_binary_value(number: int) -> str:
    if number == 0:
        return "0"

    digits = []
    positive_number = abs(number)
    while positive_number > 0:
        digits.append(str(positive_number % 2))
        positive_number //= 2

    binary = "".join(reversed(digits))
    return binary


def get_direct_code(number: int) -> str:
    BITS = 32      
    ABS_BITS = BITS - 1  

    if number >= 0:
        sign_bit = "0"
        mag = decimal_to_binary_value(number)
    else:
        sign_bit = "1"
        mag = decimal_to_binary_value(number) 

    if len(mag) > ABS_BITS:
        print(f"Внимание: {number} не помещается в 32-битный прямой код без переполнения.")
        mag = mag[-ABS_BITS:]
    else:
        mag = mag.zfill(ABS_BITS)
    return sign_bit + mag

def get_reversed_code(number: int) -> str:
    direct_code = get_direct_code(number)
    
    if number >= 0:
        return direct_code
    else:
        inverted = ""
        for bit in direct_code:
            inverted += "1" if bit == "0" else "0"
        return inverted
    
def get_additional_code(n: int) -> str:
    BITS = 32
    
    if n >= 0:
        return get_direct_code(n)
    else:
        reversed_code = get_reversed_code(n)
        additional_code = ""
        carry = 1  
        
        for i in range(BITS - 1, -1, -1): 
            bit = int(reversed_code[i])
            new_bit = (bit + carry) % 2
            carry = (bit + carry) // 2
            additional_code = str(new_bit) + additional_code
        
        return additional_code

def main():
    while True:
        try:
            user_input = input("Введите целое число (q для выхода): ")
            if user_input.lower() == "q":
                break

            number = int(user_input)
            d_code = get_direct_code(number)
            print(f"Число {number} в прямом коде: {d_code}")

            r_code = get_reversed_code(number)
            print(f"Число {number} в обратном коде: {r_code}")

            a_code = get_additional_code(number)
            print(f"Число {number} в дополнительном коде: {a_code}")


        except ValueError:
            print("Ошибка: введите целое число.")
        except KeyboardInterrupt:
            print("\nВыход.")
            break


if name == "main":
    main()