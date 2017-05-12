from OpenGL.GL import *
import numpy


class Geometries:
    def __init__(self):
        # The triangle vertex array object
        # triangle   vertices        colors
        triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                     0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                     0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

        self.tv_count = int(len(triangle) / 6)  # triangle vertex count = 3

        triangle = numpy.array(triangle, dtype=numpy.float32)

        self.vao_triangle = glGenVertexArrays(1)
        glBindVertexArray(self.vao_triangle)
        vbo_triangle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle)
        glBufferData(GL_ARRAY_BUFFER, len(triangle) * 4, triangle, GL_STATIC_DRAW)
        # vertex attribute pointers
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # color attribute pointers
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        # The quad vertex array object
        # quad   vertices        colors
        quad = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                 0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
                 0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

        self.qv_count = int(len(quad) / 6)  # quad vertex count = 4

        quad = numpy.array(quad, dtype=numpy.float32)

        self.vao_quad = glGenVertexArrays(1)
        glBindVertexArray(self.vao_quad)
        vbo_quad = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_quad)
        glBufferData(GL_ARRAY_BUFFER, len(quad) * 4, quad, GL_STATIC_DRAW)
        # vertex attribute pointers
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # color attribute pointers
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        # The cube vertex array object
        # cube   vertices         colors
        cube = [-0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
                 0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
                 0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                 0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                 0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
                -0.5,  0.5, -0.5, 1.0, 1.0, 1.0,

                 0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                 0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
                 0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                 0.5, -0.5,  0.5, 1.0, 1.0, 1.0,

                -0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
                -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                -0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
                -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                 0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                 0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
                -0.5, -0.5,  0.5, 1.0, 1.0, 1.0,

                 0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
                -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
                -0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                 0.5,  0.5,  0.5, 1.0, 1.0, 1.0]

        cube = numpy.array(cube, dtype=numpy.float32)

        indices = [0,  1,  2,  2,  3,  0,
                   4,  5,  6,  6,  7,  4,
                   8,  9, 10, 10, 11,  8,
                  12, 13, 14, 14, 15, 12,
                  16, 17, 18, 18, 19, 16,
                  20, 21, 22, 22, 23, 20]

        self.ci_count = len(indices)  # cube indices count

        indices = numpy.array(indices, dtype=numpy.uint32)

        self.vao_cube = glGenVertexArrays(1)
        glBindVertexArray(self.vao_cube)
        vbo_cube = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_cube)
        glBufferData(GL_ARRAY_BUFFER, len(cube) * 4, cube, GL_STATIC_DRAW)

        cube_ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)
        # vertex attribute pointers
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # color attribute pointers
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    def bind_triangle(self):
        glBindVertexArray(self.vao_triangle)

    def bind_quad(self):
        glBindVertexArray(self.vao_quad)

    def bind_cube(self):
        glBindVertexArray(self.vao_cube)


