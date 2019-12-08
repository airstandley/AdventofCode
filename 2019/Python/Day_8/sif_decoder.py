import os
import copy


def get_image_data(filepath):
    # Load the image data from file
    data = []
    with open(filepath) as f:
        value = f.read(1)
        while value:
            data.append(int(value))
            value = f.read(1)
    return data


def decode_image_layers(image_data, w=100, h=100):
    # Decode an array of SIF image data into layer data
    index = 0
    max_index = len(image_data)
    layers = []
    while index < max_index:
        layer_data = []
        for row in range(h):
            row_data = []
            for pixel in range(w):
                value = image_data[index]
                row_data.append(value)
                index += 1
                if index >= max_index:
                    break
            layer_data.append(row_data)
            if index >= max_index:
                break
        # print("Layer:", layer_data)
        layers.append(layer_data)
    return layers


def count_occurrences(layer, value):
    # Count how many times a value appears in a layer
    count = 0
    for row in layer:
        for pixel in row:
            if pixel == value:
                count += 1
    return count


def find_verification_layer(layers):
    # Find the layer with the fewests 0s
    verification_layer = None
    min_count = 999999999999
    for layer in layers:
        count = count_occurrences(layer, 0)
        if count < min_count:
            verification_layer = layer
            min_count = count
    return verification_layer


def verify_image(layers):
    verification_layer = find_verification_layer(layers)
    one_count = count_occurrences(verification_layer, 1)
    two_count = count_occurrences(verification_layer, 2)

    return one_count * two_count


def tests():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    layers = decode_image_layers(data, w=3, h=2)
    assert layers[0] == [[1, 2, 3], [4, 5, 6]]
    assert layers[1] == [[7, 8, 9], [0, 1, 2]]


if __name__ == "__main__":
    tests()

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
    image_data = get_image_data(input_file)
    layers = decode_image_layers(image_data, w=25, h=6)
    print(verify_image(layers))


