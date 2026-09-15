# WGUPS-Routing-Optimization
Python, custom hash table, nearest-neighbor algorithm, delivery constraints

A Python-based package delivery routing application developed to
optimize deliveries while satisfying a variety of time, vehicle,
and package constraints.

This project was originally developed as part of my Computer Science
coursework at Western Governors University.

## Project Overview

The application simulates package delivery using three delivery trucks.
It determines delivery routes while accounting for constraints such as
package deadlines, delayed packages, truck capacity, package grouping,
truck-specific requirements, and address corrections.

The goal was to produce efficient delivery routes while ensuring that
all required delivery constraints were satisfied.

## Technologies and Concepts

- Python
- Object-Oriented Programming
- Data Structures
- Custom Hash Table
- Greedy / Nearest-Neighbor Routing
- Algorithm Design
- Time and Space Complexity Analysis
- File/Data Processing

## Key Features

- Custom hash table implementation for storing and retrieving package data
- Package lookup by package ID
- Greedy routing algorithm based on delivery constraints and distance
- Three-truck delivery simulation
- Package deadline handling
- Delayed package handling
- Truck-specific package restrictions
- Grouped package requirements
- Time-dependent address correction
- Package status tracking based on a requested time
- Total mileage calculation

## Routing Approach

The routing system uses a greedy approach influenced by nearest-neighbor
routing. At each stage of a route, the program evaluates available
packages based on delivery requirements and distance from the truck's
current location.

Nearest-neighbor routing provides an efficient heuristic for this type
of problem, although it does not guarantee a globally optimal route.

## Data Structure

Package information is stored using a custom hash table.

The package ID is used to determine the appropriate bucket, allowing
package records to be efficiently inserted and retrieved. Collisions
are handled by storing multiple records within a bucket.

This provides approximately O(1) average-case lookup performance,
although performance can degrade when collisions occur.

## Delivery Constraints

The routing system accounts for several real-world constraints,
including:

- Delivery deadlines
- Delayed packages
- Maximum truck capacity
- Packages required to travel together
- Packages restricted to specific trucks
- Different truck departure times
- Address corrections that occur during the delivery day

## What I Learned

This project strengthened my understanding of data structures,
algorithm design, object-oriented programming, and optimization.

It also gave me experience translating a set of real-world constraints
into program logic and evaluating the tradeoff between computational
efficiency and finding an optimal solution.

## Future Improvements

Potential improvements include:

- Separating the application into additional modules
- Adding automated unit tests
- Improving route optimization beyond the greedy heuristic
- Adding a graphical user interface
- Improving error handling and input validation
