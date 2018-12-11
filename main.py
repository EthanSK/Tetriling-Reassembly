from copy import deepcopy  # copy 'target' to avoid modifying it
import utils  # it might be helpful to use 'utils.py'
import numpy as np


def Tetris(target, limit_tetris):

    def generate_weight_matrix(original_matrix, last_left_off_coord):
       # weight_matrix = np.zeros((rows,cols))
        row_lower_limit = last_left_off_coord[0]
        col_lower_limit = last_left_off_coord[1]
        for row in range(row_lower_limit, rows):
            for col in range(col_lower_limit, cols):
                update_tile_weight(row, col, original_matrix)
            col_lower_limit = 0

    def update_tile_weight(row, col, original_matrix):
        if is_tile_in_matrix_range(row, col):
            if original_matrix[row][col] == 1:
                weight_matrix[row][col] = 0
                if is_tile_in_matrix_range(row + 1, col):
                    weight_matrix[row][col] += original_matrix[row+1][col]
                if is_tile_in_matrix_range(row, col + 1):
                    weight_matrix[row][col] += original_matrix[row][col+1]
                if is_tile_in_matrix_range(row - 1, col):
                    weight_matrix[row][col] += original_matrix[row-1][col]
                if is_tile_in_matrix_range(row, col-1):
                    weight_matrix[row][col] += original_matrix[row][col-1]

    def update_weights_surrounding_shape(shape_id, start_coord, target_matrix):
        set_tiles_of_shape_to_0(shape_id, start_coord)
        for rel_coord in shape_surrounding_coords[shape_id]:
            #print('shape id: ', shape_id)
            update_tile_weight(
                start_coord[0] + rel_coord[0], start_coord[1] + rel_coord[1], target_matrix)

    def is_tile_in_matrix_range(row_index, col_index):
        if col_index > cols-1 or col_index < 0:
            return False
        if row_index > rows-1 or row_index < 0:
            return False
        return True

    def set_tiles_of_shapes_to_0(shapes_dict):
        dict_items = shapes_dict.items()
        for start_coord, shape_id in dict_items:
            set_tiles_of_shape_to_0(shape_id, start_coord)

    def set_tiles_of_shape_to_0(shape_id, start_coord):
        shape_rel_coords = utils.generate_shape(shape_id)
        for coord in shape_rel_coords:
            weight_matrix[start_coord[0] + coord[0]
                          ][start_coord[1] + coord[1]] = 0

    def coord_and_value_of_first_non_0_value(last_left_off_coord):
        row_lower_limit = last_left_off_coord[0]
        col_lower_limit = last_left_off_coord[1]
        for row in range(row_lower_limit, rows):
            for col in range(col_lower_limit, cols):
                tile_value = weight_matrix[row][col]
                if tile_value != 0:
                    return (row, col), tile_value
            col_lower_limit = 0

    def value_of_tile_at_offset(start_coord, offset):
        row_index = start_coord[0] + offset[0]
        col_index = start_coord[1] + offset[1]
        if is_tile_in_matrix_range(row_index, col_index) == False:
            return -1
        return weight_matrix[row_index][col_index]

    def list_of_shapes_that_fit_inside_cutout():
        result = []
        shape_items = number_of_allowed_shapes.items()
        for shape_id, number_of_instances_of_shape_allowed in shape_items:
            if not (first_non_0_value >= shape_origins_values[shape_id] and number_of_instances_of_shape_allowed != 0):
                continue
            offsets_of_tiles_in_shape = utils.generate_shape(shape_id)
            shape_fails_test = False
            for tile_offset in offsets_of_tiles_in_shape:
                tile_value = value_of_tile_at_offset(
                    first_non_0_coord, tile_offset)
                if tile_value <= 0:
                    shape_fails_test = True
                    break
            if shape_fails_test is False:
                result.append(shape_id)
        return result

    def shape_id_with_lowest_sum():  # has no way of breaking the tie between two equal summed shapes
        lowest_sum_so_far = 9999999999
        lowest_shape_id_so_far = 0
        for shape_id in list_of_shapes_that_fit_inside_cutout_result:
            # calculate sum of shape in weight matrix
            offsets_of_tiles_in_shape = utils.generate_shape(shape_id)
            shape_sum = 0
            for tile_offset in offsets_of_tiles_in_shape:
                tile_value = value_of_tile_at_offset(
                    first_non_0_coord, tile_offset)
                shape_sum = shape_sum + tile_value
            if shape_sum < lowest_sum_so_far:
                lowest_sum_so_far = shape_sum
                lowest_shape_id_so_far = shape_id
        return lowest_shape_id_so_far

    def place_shape_and_update_target_matrix():
        shape_id = shape_id_with_lowest_sum_result
        offsets_of_tiles_in_shape = utils.generate_shape(shape_id)
        start_coord = first_non_0_coord
        for tile_offset in offsets_of_tiles_in_shape:
            updating_target_matrix[start_coord[0] +
                                   tile_offset[0]][start_coord[1] + tile_offset[1]] = 0
            my_solution_matrix_np[start_coord[0] + tile_offset[0]
                                  ][start_coord[1] + tile_offset[1]] = (shape_id, placement_counter)

    def is_matrix_full_of_zeroes(matrix, last_left_off_coord):
        row_lower_limit = last_left_off_coord[0]
        col_lower_limit = last_left_off_coord[1]
        for row in range(row_lower_limit, rows):
            for col in range(col_lower_limit, cols):
                tile_value = matrix[row][col]
                if tile_value != 0:
                    return False
            col_lower_limit = 0
        return True

    shape_origins_values = {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 1,
                            9: 1, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 2, 17: 1, 18: 1, 19: 1}
    shape_surrounding_coords = {
        1: [[-1, 0], [-1, 1], [0, 2], [1, 2], [2, 0], [2, 1], [0, -1], [1, -1]],
        2: [[-1, 0], [0, 1], [1, 1], [2, 1], [4, 0], [3, -1], [2, -1], [1, -1], [0, -1]],
        3: [[-1, 0], [-1, 1], [-1, 2], [-1, 3], [0, 4], [1, 3], [1, 2], [1, 1], [1, 0], [0, -1]],
        4: [[-1, 0], [0, 1], [1, 1], [2, 2], [3, 1], [3, 0], [2, -1], [1, -1], [0, -1]],
        5: [[-1, 0], [0, 1], [1, 1], [2, 0], [2, -1], [2, -2], [1, -3], [0, -2], [0, -1]],
        6: [[0, -1], [-1, 0], [-1, 1], [0, 2], [1, 2], [2, 2], [3, 1], [2, 0], [1, 0]],
        7: [[-1, 0], [-1, 1], [-1, 2], [0, 3], [1, 2], [1, 1], [2, 0], [1, -1], [0, -1]],
        8: [[-1, 0], [0, 1], [1, 1], [2, 1], [3, 0], [3, -1], [2, -2], [1, -1], [0, -1]],
        9: [[0, -1], [-1, 0], [-1, 1], [-1, 2], [0, 3], [1, 3], [2, 2], [1, 1], [1, 0]],
        10: [[-1, 0], [-1, 1], [0, 2], [1, 1], [2, 1], [3, 0], [2, -1], [1, -1], [0, -1]],
        11: [[-1, 0], [0, 1], [0, 2], [1, 3], [2, 2], [2, 1], [2, 0], [1, -1], [0, -1]],
        12: [[-1, 0], [0, 1], [1, 2], [2, 1], [3, 0], [2, -1], [1, -1], [0, -1]],
        13: [[-1, 0], [0, 1], [1, 2], [2, 1], [2, 0], [2, -1], [1, -2], [0, -1]],
        14: [[-1, 0], [0, 1], [1, 1], [2, 1], [3, 0], [2, -1], [1, -2], [0, -1]],
        15: [[-1, 0], [-1, 1], [-1, 2], [0, 3], [1, 2], [2, 1], [1, 0], [0, -1]],
        16: [[-1, 0], [-1, 1], [2, 0], [1, 1], [2, 0], [2, -1], [1, -2], [0, -1]],
        17: [[-1, 0], [0, 1], [1, 2], [2, 2], [3, 1], [2, 0], [1, -1], [0, -1]],
        18: [[-1, 0], [-1, 1], [0, 2], [1, 3], [2, 2], [2, 1], [1, 0], [0, -1]],
        19: [[-1, 0], [0, 1], [1, 1], [2, 0], [3, -1], [2, -2], [1, -2], [0, -1]]

    }

    # main execution
    #target_matrix, number_of_allowed_shapes, perfect_solution_matrix = utils.generate_target(cols, rows, density)
    target_matrix = target
    number_of_allowed_shapes = limit_tetris
    rows = len(target_matrix)
    cols = len(target_matrix[0])
    weight_matrix = np.zeros((rows, cols))
    #initial_number_of_allowed_shapes = deepcopy(number_of_allowed_shapes)
    updating_target_matrix = deepcopy(target_matrix)
    placement_counter = 1

    my_solution_matrix_np = np.empty((), dtype=object)
    my_solution_matrix_np[()] = (0, 0)
    my_solution_matrix_np = np.full(
        (rows, cols), my_solution_matrix_np, dtype=object)

    first_non_0_coord = (0, 0)
    first_non_0_value = 0
#    list_of_possible_shapes_matching_origin_value_result = []
    list_of_shapes_that_fit_inside_cutout_result = []

    loop_counter = -1

    generate_weight_matrix(updating_target_matrix, first_non_0_coord)

    # loop this until whole updating matrix is 0
    while True:
        loop_counter += 1
        if is_matrix_full_of_zeroes(weight_matrix, first_non_0_coord):
            break
        first_non_0_coord, first_non_0_value = coord_and_value_of_first_non_0_value(
            first_non_0_coord)
#        list_of_possible_shapes_matching_origin_value_result = list_of_possible_shapes_matching_origin_value()
        list_of_shapes_that_fit_inside_cutout_result = list_of_shapes_that_fit_inside_cutout()
        if list_of_shapes_that_fit_inside_cutout_result == []:
            updating_target_matrix[first_non_0_coord[0]
                                   ][first_non_0_coord[1]] = 0
            weight_matrix[first_non_0_coord[0]][first_non_0_coord[1]] = 0
            #weight_matrix = np.zeros((rows,cols))
            continue
        shape_id_with_lowest_sum_result = shape_id_with_lowest_sum()
        number_of_allowed_shapes[shape_id_with_lowest_sum_result] -= 1
        place_shape_and_update_target_matrix()
        update_weights_surrounding_shape(
            shape_id_with_lowest_sum_result, first_non_0_coord, updating_target_matrix)
        placement_counter += 1
    my_solution_matrix = my_solution_matrix_np.tolist()
    return my_solution_matrix
