import wx
from wx import glcanvas
from OpenGL.GL import *
import OpenGL.GL.shaders
from pyrr import Matrix44, matrix44, Vector3
import time, sys
from Geometries import Geometries

vertex_shader = """
# version 330
in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;
uniform mat4 model;
uniform mat4 vp;

void main(){
    gl_Position = vp * model * vec4(positions, 1.0);
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
        self.size = (1120, 630)
        self.aspect_ratio = self.size[0] / self.size[1]
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)
        self.init = False
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.rotate = False
        self.rot_y = Matrix44.identity()
        self.show_triangle = False
        self.show_quad = False
        self.show_cube = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):

        self.mesh = Geometries()

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        glClearColor(0.1, 0.15, 0.1, 1.0)

        view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
        projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)

        vp = matrix44.multiply(view, projection)

        glUseProgram(shader)
        glEnable(GL_DEPTH_TEST)

        vp_loc = glGetUniformLocation(shader, "vp")
        glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)

        self.model_loc = glGetUniformLocation(shader, "model")

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.rotate:
            ct = time.clock()
            self.rot_y = Matrix44.from_y_rotation(ct)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.rot_y)
            self.Refresh()
        else:
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.rot_y)

        if self.show_triangle:
            self.mesh.bind_triangle()
            glDrawArrays(GL_TRIANGLES, 0, self.mesh.tv_count)
        elif self.show_quad:
            self.mesh.bind_quad()
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.mesh.qv_count)
        elif self.show_cube:
            self.mesh.bind_cube()
            glDrawElements(GL_TRIANGLES, self.mesh.ci_count, GL_UNSIGNED_INT, None)

        self.SwapBuffers()


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("#626D58")

        self.canvas = OpenGLCanvas(self)
        self.rot_btn = wx.Button(self, -1, label="Start/Stop \nrotation", pos=(1130, 10), size=(100, 50))
        self.rot_btn.BackgroundColour = [125, 125, 125]
        self.rot_btn.ForegroundColour = [255, 255, 255]
        self.rad_btn1 = wx.RadioButton(self, -1, label="Show Triangle", pos=(1130, 80))
        self.rad_btn2 = wx.RadioButton(self, -1, label="Show Quad", pos=(1130, 100))
        self.rad_btn3 = wx.RadioButton(self, -1, label="Show Cube", pos=(1130, 120))

        self.Bind(wx.EVT_BUTTON, self.rotate, self.rot_btn)
        self.Bind(wx.EVT_RADIOBUTTON, self.triangle, self.rad_btn1)
        self.Bind(wx.EVT_RADIOBUTTON, self.quad, self.rad_btn2)
        self.Bind(wx.EVT_RADIOBUTTON, self.cube, self.rad_btn3)

    def triangle(self, event):
        self.canvas.show_triangle = True
        self.canvas.show_quad = False
        self.canvas.show_cube = False
        self.canvas.Refresh()

    def quad(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = True
        self.canvas.show_cube = False
        self.canvas.Refresh()

    def cube(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = False
        self.canvas.show_cube = True
        self.canvas.Refresh()

    def rotate(self, event):
        if not self.canvas.rotate:
            self.canvas.rotate = True
            self.canvas.Refresh()
        else:
            self.canvas.rotate = False


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title="My wx frame", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel = MyPanel(self)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()





