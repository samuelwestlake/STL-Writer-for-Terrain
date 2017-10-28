#!/usr/bin/env python3

"""
Samuel Westlake, October 2014.
Writes an ASCII STL file from a grid of height data in ASCII format from Ordinance Survey.
Assumes that the given file has 5 rows of header meta data.
Header rows should include nrows, ncols, xllcorner, yllcorner, cellsize.
samuelwestlake@hotmail.co.uk
"""

import os
import csv
import numpy as np
from triangle import Triangle


def e(n):
    """
    :param n: (float)
    :return: scientific notation of n (str)
    """
    a = "%E" % n
    return a.split("E")[0].rstrip("0").rstrip(".") + "E" + a.split("E")[1]


def get_float(text):
    """
    :param text: message to display when asking for a number (str)
    :return: n, a number given by user (float)
    """
    while True:
        n = input(text)
        try:
            n = float(n)
            return n
        except ValueError:
            print("ValueError: not a number.\n")


def file_path_and_data():
    """
    Asks the user for a path to a csv file and return the file path and data
    :return: path, path to a file, given by the user (str)
    :return: data, data from the given file (list of lists)
    """
    while True:
        file_name = input("Enter path to terrain file:\n")
        if os.path.isfile(file_name):
            delimiter = input("Enter the delimiter char:\n")
            path = os.path.abspath(file_name)
            data = list()
            meta_data = dict()
            with open(path, "r") as csv_file:
                read = csv.reader(csv_file, delimiter=delimiter)
                for i, row in enumerate(read):
                    if row:
                        if i < 5:                               # The first 5 rows contain metadata
                            meta_data[row[0]] = float(row[1])   # Add meta data to dictionary
                        else:
                            data.append(list(map(float, row)))  # Append data as a list of floats
            return path, data, meta_data
        else:
            print(file_name + " not found.")


def setup_out_file(out_path):
    """
    Creates output file and writes the first line
    :param out_path: file path to output file (str)
    :return: None
    """
    out_file = open(out_path, "w")
    out_file.write("solid " + out_path.split("/")[-1].split(".")[0] + "\n")
    out_file.close()


def end_out_file(out_path):
    """
    Writes the last line in the output file
    :param out_path: file path to output file (str)
    :return: None
    """
    out_file = open(out_path, "a")
    out_file.write("endsolid " + out_path.split("/")[-1].split(".")[0] + "\n")
    out_file.close()


def write_to_file(file_path, triangle):
    """
    Writes a triangle into the output file in stl format
    :param file_path: file path to the output file (str)
    :param triangle: triangle to write to file (object)
    :return: None
    """
    out_file = open(file_path, "a")
    v0 = triangle.v0
    v1 = triangle.v1
    v2 = triangle.v2
    ni, nj, nk = triangle.normal_unit_vector()
    out_file.write("    facet normal " + e(ni) + " " + e(nj) + " " + e(nk) + "\n")
    out_file.write("        outer loop\n")
    out_file.write("            vertex " + e(v0[0]) + " " + e(v0[1]) + " " + e(v0[2]) + "\n")
    out_file.write("            vertex " + e(v1[0]) + " " + e(v1[1]) + " " + e(v1[2]) + "\n")
    out_file.write("            vertex " + e(v2[0]) + " " + e(v2[1]) + " " + e(v2[2]) + "\n")
    out_file.write("        endloop\n")
    out_file.write("    endfacet\n")
    out_file.close()


def calc_vertices(i, j, data, cell_size=1.0, offset=(0.0, 0.0)):
    """
    :param i: column index of current data point (int)
    :param j: row index of current data point (int)
    :param data: Terrain height data (list of lists of floats)
    :param cell_size: Real-world distance between points (float)
    :param offset: Coordinates of the lower left data point (tuple of floats)
    :return: x, y, z coordinates of each vertex
    """
    y_max = len(data) - 1
    vx = np.asarray([k * cell_size + offset[0] for k in i])
    vy = np.asarray([(y_max - k) * cell_size + offset[1] for k in j])
    vz = np.asarray([data[n][m] for m, n in zip(i, j)])
    return vx, vy, vz


def main():
    """
    Asks user for an input file
    Converts the series of height data values into triangles
    Writes triangles to file in stl format
    :return: None
    """
    # Ask user for file path and return data:
    in_path, data, meta_data = file_path_and_data()
    # Get useful meta data:
    cell_size = meta_data["cellsize"]
    offset = (meta_data["xllcorner"], meta_data["yllcorner"])
    # Set up output file:
    out_path = os.path.splitext(in_path)[0] + ".stl"
    setup_out_file(out_path)
    # Loop through data and write to file:
    # Each data point and its three right and lower neighbours
    # generate two surface triangles
    print("Writing STL surface...")
    for j0, row in enumerate(data[:-1]):
        for i0, z0 in enumerate(row[:-1]):
            # Triangle 1
            i = [i0, i0 + 1, i0]
            j = [j0, j0 + 1, j0 + 1]
            vx, vy, vz = calc_vertices(i, j, data, cell_size, offset)
            write_to_file(out_path, Triangle(vx, vy, vz))
            # Triangle 2
            i = [i0, i0 + 1, i0 + 1]
            j = [j0, j0, j0 + 1]
            vx, vy, vz = calc_vertices(i, j, data, cell_size, offset)
            write_to_file(out_path, Triangle(vx, vy, vz))
    end_out_file(out_path)
    print("Done.")


main()
