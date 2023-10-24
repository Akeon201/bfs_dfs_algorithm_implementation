# Homework 1: Breadth-First and Depth-First Pathfinding
# Author: Kenyon Leblanc

import csv  # Used in load_graph for reading csv
import os  # Check directory files

# Global variable for dfs search
dfs_marked_vertices = []


def bfs_search(graph, start_node: str, end_node: str):
    """
    Breadth-first Search algorithm
    :param graph: Dictionary object from load_graph()
    :param start_node: Node you want to start at
    :param end_node: Node you want to stop at
    :return: List sorted with index 0 as starting node
    """
    # Initialize queue list and marked_vertex list
    queue = [[start_node]]
    marked_vertices = []

    # Loop while queue has paths
    while queue:
        # Dequeue next path
        path = queue.pop(0)

        # End node is found at end of path
        if path[-1] == end_node:
            return path

        # Loop through all connected nodes
        for vertex in graph[path[-1]]:
            # Skip blank string entries
            if vertex == "":
                break
            # Skip over visited nodes
            if vertex not in marked_vertices:
                # Add vertex to visited
                marked_vertices.append(vertex)
                # Create new list consisting of current path and new neighboring node
                new_edge = list(path) + [vertex]
                # Add new pathway to queue
                queue.append(new_edge)
    # Vertex already searched
    return None


def check_starting_node(graph, start_node: str):
    """
    Check to make sure node are valid.
    :param graph: Loaded graph
    :param start_node: User input for starting node
    :return: valid start node
    """
    while start_node not in graph:
        print("Not a valid starting node, please try again.")
        start_node = input("Enter starting node: ")

    return start_node


def check_ending_node(graph, end_node: str):
    """
    Check to make sure node are valid.
    :param graph: Loaded graph
    :param end_node: User input for starting node
    :return: valid end node
    """
    while end_node not in graph:
        print("Not a valid ending node, please try again.")
        end_node = input("Enter ending node: ")

    return end_node


def check_valid_file(file_name):
    """
    Check if file provided by user input is valid
    :param file_name: file name w/ extension
    :return: valid file name
    """
    # Current directory
    directory = os.getcwd()
    # List of files from cwd
    listed_directory = os.listdir(directory)
    # Continue loop until valid file name is given
    while file_name not in listed_directory:
        print("File not found, please try again.")
        file_name = input("Please enter file name with extension: ")

    return file_name



def custom_sort(x):
    """
    Key function for sorted function. Used in load_graph.
    :param x:
    :return:
    """

    if x == "":
        return str('inf')

    try:
        return str(x)
    except ValueError:
        return x


def dfs_search(graph, start_node: str, end_node: str, stack=None):
    """
    Depth-First Search algorithm
    :param graph: Dictionary object from load_graph()
    :param start_node: Node you want to start at
    :param end_node: Node you want to stop at
    :param stack: Used in recursion
    :return: List sorted with index 0 as starting node
    """
    # Initialize stack for first function call
    if stack is None:
        stack = []

    # Add node to stack
    stack.append(start_node)

    # Return stack if path to end_node is found
    if end_node in graph[start_node]:
        stack.append(end_node)
        return stack
    if start_node == end_node:
        return stack

    # Loop through each connected vertices
    for next_node in graph[start_node]:
        # Break out of loop if "" is found.
        if next_node == "":
            break
        # Skip if cycle is found or if in marked list
        if next_node not in stack and next_node not in dfs_marked_vertices:
            # Add vertex to marked vertices list
            dfs_marked_vertices.append(next_node)
            # Continue recursive search
            valid_path = dfs_search(graph, next_node, end_node, stack)
            # If valid path is found then stop searching and return path
            if valid_path:
                return valid_path
    # Dead end
    return None


def load_graph(file_name):
    """
    Given a file name, will attempt to open a csv file to build a connected graph.
    :param file_name: Name of the file without file extension.
    :return: Dictionary object with each node being a key, and the values being a set of edges.
    """
    # Dictionary will be used to load graph
    graph = {}
    try:
        with open(file_name, "r") as open_file:
            reader = csv.reader(open_file, delimiter=",")
            # Each row in file
            for row in reader:
                # Skip first row if it contains From,To entries
                if row[1] == "To":
                    continue
                edge = sorted(row[1:], key=custom_sort)  # Sort in case edges are out of order
                graph[row[0]] = edge
        return graph
    except Exception as e:
        print(f"{type(e).__name__} occurred: {e}")
        exit(1)


def print_graph(loaded_graph):
    """
    Print graph to terminal window.
    :param loaded_graph: Dictionary object returned from load_graph function
    """
    for key, value in graph.items():
        print(f'{key} {value}')


if __name__ == '__main__':
    arrow = " -> "

    # Gather file name and load graph
    file_name = input("Please enter file name with extension: ")
    file_name = check_valid_file(file_name)
    print("Loading...")
    graph = load_graph(file_name)
    # print_graph(graph)

    # Collect start/end node
    graph_keys = list(graph.keys())
    start = input(f"Enter starting node({graph_keys[0]}-{graph_keys[-1]}): ")
    start = check_starting_node(graph, start)
    end = input(f"Enter ending node({graph_keys[0]}-{graph_keys[-1]}): ")
    end = check_ending_node(graph, end)

    # Perform bfs search
    answer = bfs_search(graph, start, end)
    if answer is not None:
        result = arrow.join(answer)
        print("\nBreadth-first search")
        print(result)
    else:
        print("No Path was found")

    # Perform dfs search
    answer = dfs_search(graph, start, end)
    if answer is not None:
        result = arrow.join(answer)
        print("\nDepth-first search")
        print(result)
    else:
        print("No path was found")

    exit(0)
