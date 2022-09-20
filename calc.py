def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return ''.join(result)
 
 
def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0 : pick]
 
    while pick < len(divident):
 
        if tmp[0] == '1':
         tmp = xor(divisor, tmp) + divident[pick]
 
        else: 
            tmp = xor('0'*pick, tmp) + divident[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
 
    
    return tmp


if __name__ == "__main__":
    divident = "10010101"
    divisor = "011010"
    print(divident + " % " + divisor + " = " + mod2div(divident, divisor))