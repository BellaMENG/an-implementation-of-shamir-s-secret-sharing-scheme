from pyfinite import ffield
import csv


# lookup table for inverse function in ffield with base 8

inverse_lut = {0: 0, 1: 1, 2: 142, 3: 244, 4: 71, 5: 167, 6: 122, 7: 186, 8: 173,
               9: 157, 10: 221, 11: 152, 12: 61, 13: 170, 14: 93, 15: 150, 16: 216,
               17: 114, 18: 192, 19: 88, 20: 224, 21: 62, 22: 76, 23: 102, 24: 144,
               25: 222, 26: 85, 27: 128, 28: 160, 29: 131, 30: 75, 31: 42, 32: 108,
               33: 237, 34: 57, 35: 81, 36: 96, 37: 86, 38: 44, 39: 138, 40: 112,
               41: 208, 42: 31, 43: 74, 44: 38, 45: 139, 46: 51, 47: 110, 48: 72,
               49: 137, 50: 111, 51: 46, 52: 164, 53: 195, 54: 64, 55: 94, 56: 80,
               57: 34, 58: 207, 59: 169, 60: 171, 61: 12, 62: 21, 63: 225, 64: 54,
               65: 95, 66: 248, 67: 213, 68: 146, 69: 78, 70: 166, 71: 4, 72: 48,
               73: 136, 74: 43, 75: 30, 76: 22, 77: 103, 78: 69, 79: 147, 80: 56,
               81: 35, 82: 104, 83: 140, 84: 129, 85: 26, 86: 37, 87: 97, 88: 19,
               89: 193, 90: 203, 91: 99, 92: 151, 93: 14, 94: 55, 95: 65, 96: 36,
               97: 87, 98: 202, 99: 91, 100: 185, 101: 196, 102: 23, 103: 77, 104: 82,
               105: 141, 106: 239, 107: 179, 108: 32, 109: 236, 110: 47, 111: 50, 112: 40,
               113: 209, 114: 17, 115: 217, 116: 233, 117: 251, 118: 218, 119: 121, 120: 219,
               121: 119, 122: 6, 123: 187, 124: 132, 125: 205, 126: 254, 127: 252, 128: 27,
               129: 84, 130: 161, 131: 29, 132: 124, 133: 204, 134: 228, 135: 176, 136: 73,
               137: 49, 138: 39, 139: 45, 140: 83, 141: 105, 142: 2, 143: 245, 144: 24,
               145: 223, 146: 68, 147: 79, 148: 155, 149: 188, 150: 15, 151: 92, 152: 11,
               153: 220, 154: 189, 155: 148, 156: 172, 157: 9, 158: 199, 159: 162, 160: 28,
               161: 130, 162: 159, 163: 198, 164: 52, 165: 194, 166: 70, 167: 5, 168: 206,
               169: 59, 170: 13, 171: 60, 172: 156, 173: 8, 174: 190, 175: 183, 176: 135,
               177: 229, 178: 238, 179: 107, 180: 235, 181: 242, 182: 191, 183: 175, 184: 197,
               185: 100, 186: 7, 187: 123, 188: 149, 189: 154, 190: 174, 191: 182, 192: 18,
               193: 89, 194: 165, 195: 53, 196: 101, 197: 184, 198: 163, 199: 158, 200: 210,
               201: 247, 202: 98, 203: 90, 204: 133, 205: 125, 206: 168, 207: 58, 208: 41,
               209: 113, 210: 200, 211: 246, 212: 249, 213: 67, 214: 215, 215: 214, 216: 16,
               217: 115, 218: 118, 219: 120, 220: 153, 221: 10, 222: 25, 223: 145, 224: 20,
               225: 63, 226: 230, 227: 240, 228: 134, 229: 177, 230: 226, 231: 241, 232: 250,
               233: 116, 234: 243, 235: 180, 236: 109, 237: 33, 238: 178, 239: 106, 240: 227,
               241: 231, 242: 181, 243: 234, 244: 3, 245: 143, 246: 211, 247: 201, 248: 66,
               249: 212, 250: 232, 251: 117, 252: 127, 253: 255, 254: 126, 255: 253}


def find_inverse(i):
    return inverse_lut[i]


def write_to_multi_lut(multiply_table):
    with open("multiply_lut.csv","w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in multiply_table:
            csv_writer.writerow(row)


def write_to_inverse_lut(inverse_table):
    with open("inverse_lut.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(inverse_table)


def write_to_add_lut(add_table):
    with open("add_lut.csv","w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in add_table:
            csv_writer.writerow(row)


def write_to_sub_lut(sub_table):
    with open("sub_lut.csv","w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in sub_table:
            csv_writer.writerow(row)


def create_multi_lut():
    multiply_table = []

    for i in range(2**8):
        row = []
        for j in range(2**8):
            val = F.Multiply(i,j)
            row.append(val)
        multiply_table.append(row)
    return multiply_table


def create_inverse_lut():
    inverse_table = []
    for i in range(2 ** 8):
        val = F.Inverse(i)
        inverse_table.append(val)
    return inverse_table


def create_add_lut():
    add_lut = []
    for i in range(2**8):
        row = []
        for j in range(2**8):
            val = F.Add(i,j)
            row.append(val)
        add_lut.append(row)

    return add_lut


def create_sub_lut():
    sub_lut = []
    for i in range(2**8):
        row = []
        for j in range(2**8):
            val = F.Subtract(i,j)
            row.append(val)
        sub_lut.append(row)

    return sub_lut


if __name__ == "__main__":
    F = ffield.FField(8)
    # write_to_sub_lut(create_sub_lut())
    # write_to_add_lut(create_add_lut())
    # write_to_inverse_lut(create_inverse_lut())
    # multiply_table = create_multi_lut()

    # write_to_multi_lut(multiply_table)
    add_lut = create_add_lut()
    print(F.Inverse(233))
    print(F.Add(9,233))
    print(F.Subtract(9,233))
    print(F.Multiply(9,233))
