from interpolation import lagrange_interpolation


if __name__ == "__main__":
    points = []
    x_values = [1,2,5]
    y_values = [204, 99, 61]
    points.append(x_values)
    points.append(y_values)
    print(lagrange_interpolation(points))
