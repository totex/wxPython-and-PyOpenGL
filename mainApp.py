import wx
from wx import glcanvas
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

vertex_shader = """
# version 330
in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;

void main(){
    gl_Position = vec4(positions, 1.0);
    newColor = colors;
}
"""

fragment_shader = """
# version 330
in vec3 newColor;
out vec4 outColor;

void main(){
    outColor = vec4(newColor, 1.0);
}
"""


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(1120, 630))
        self.init = False
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):
        # triangle   vertices      colors
        triangle = [-0.5,-0.5,0.0, 1.0,0.0,0.0,
                     0.5,-0.5,0.0, 0.0,1.0,0.0,
                     0.0, 0.5,0.0, 0.0,0.0,1.0]

        triangle = numpy.array(triangle, dtype=numpy.float32)

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, len(triangle)*4, triangle, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glClearColor(0.1, 0.15, 0.1, 1.0)

        glUseProgram(shader)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        self.SwapBuffers()


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.canvas = OpenGLCanvas(self)


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title="My wx frame", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)

        self.panel = MyPanel(self)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()





