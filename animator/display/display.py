"""Classes for displaying for animator. This currently supports Qt (4 and 5), Tkinter (a slow and a fast version),
cv2 and matplotlib. cv2 and the slower version of Tkinter does not support the alpha channel. The best of these are
selected based on the availability of the libraries."""
from __future__ import annotations

import time
from typing import Any

from .DisplayManager import DisplayManager
from .. import skia
from ..util.env import inside_ipython_notebook

# in browser
if inside_ipython_notebook():
    from IPython.display import display, HTML, clear_output
    import base64

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'html'


class DM_html(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.img: skia.Image = skia.Image.fromarray(self.scene.frame, copy=False)
        self.prefix = "<div style='display:flex;justify-content:center;align-items:center'><img " \
                      f"style='max-width:100%;max-height:100%;'id='{self.winname}'src='data:image/png;base64,"
        self.suffix = "'></div>"
        display(HTML(self.prefix + self.frame_b64() + self.suffix))
        clear_output(True)

    def show_frame(self) -> bool:
        display(HTML(self.prefix + self.frame_b64() + self.suffix))
        clear_output(True)
        return True

    def frame_b64(self) -> str:
        return base64.b64encode(self.img.encodeToData(skia.EncodedImageFormat.kPNG, 100).bytes()).decode('utf8')


# qt
try:
    from PyQt4 import QtGui, QtCore

    QtWidgets = QtGui
    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'qt'
except ImportError:
    try:
        from PyQt5 import QtGui, QtCore, QtWidgets

        if DisplayManager.display_method is None:
            DisplayManager.display_method = 'qt'
    except ImportError:
        pass


class DM_qt(DisplayManager):
    class Viewer(QtWidgets.QMainWindow):
        def __init__(self, manager: DM_qt):
            super().__init__()
            self._manager: DM_qt = manager
            self.setWindowTitle(manager.winname)
            screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()
            self.setGeometry(screen_center.x() - manager.width / 2, screen_center.y() - manager.height / 2,
                             manager.width, manager.height)
            self.setFixedSize(manager.width, manager.height)
            r, g, b, _ = manager.scene.bgcolor
            self.setStyleSheet(f'background-color:rgb({r * 255},{g * 255},{b * 255});border:none;')
            self._gview = QtWidgets.QGraphicsView(self)
            self._gview.resize(manager.width, manager.height)
            self._gscene = QtWidgets.QGraphicsScene()
            self.pixmap = QtWidgets.QGraphicsPixmapItem()
            self._gscene.addItem(self.pixmap)
            self._gview.setScene(self._gscene)
            self.show()

        def closeEvent(self, event: QtGui.QCloseEvent) -> None:
            self._manager.running = False
            self._manager.close()
            super().closeEvent(event)

        def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Escape:
                self._manager.running = False
                self._manager.close()
            super().keyPressEvent(event)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.app = QtWidgets.QApplication([])
        self.viewer = DM_qt.Viewer(self)

    def show_frame(self) -> bool:
        if self.running:
            self.viewer.pixmap.setPixmap(QtGui.QPixmap(QtGui.QImage(self.scene.frame.data, self.width, self.height,
                                                                    QtGui.QImage.Format_RGBA8888)))
            time.sleep(self.waittime())
            self.app.processEvents()
        return self.running

    def close(self) -> None:
        self.viewer.close()


# tk
try:
    import tkinter as tk

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'tk'
    try:
        # tk is very slow with image manipulations. This block tries to achieve small speedup by directly calling some
        # functions from the tk8.6 library, if available. Since this is still slow, neither of the two tk alternatives
        # waits/sleeps between frames.
        import ctypes
        import ctypes.util
        import numpy

        libtk = ctypes.cdll.LoadLibrary(ctypes.util.find_library('tk8.6'))
        Tcl_Interp_p = ctypes.c_void_p
        c_uchar_p = ctypes.POINTER(ctypes.c_ubyte)


        class Tk_PhotoImageBlock(ctypes.Structure):
            _fields_ = [('pixelPtr', c_uchar_p),
                        ('width', ctypes.c_int),
                        ('height', ctypes.c_int),
                        ('pitch', ctypes.c_int),
                        ('pixelSize', ctypes.c_int),
                        ('offset', ctypes.c_int * 4)]


        Tk_FindPhoto = libtk.Tk_FindPhoto
        Tk_FindPhoto.argtypes = [Tcl_Interp_p, ctypes.c_char_p]
        Tk_FindPhoto.restype = ctypes.c_void_p

        Tk_PhotoPutBlock = libtk.Tk_PhotoPutBlock
        Tk_PhotoPutBlock.argtypes = [Tcl_Interp_p, ctypes.c_void_p, ctypes.POINTER(Tk_PhotoImageBlock), ctypes.c_int,
                                     ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        Tk_PhotoPutBlock.restype = None

        # tk recalculates valid regions after a PhotoPutBlock with COMPOSITE_SET operation. This is normally fast, but
        # if we have random alpha pixels, this and PhotoBlank, both are very slow. Instead a PhotoPutBlock with the
        # following block and COMPOSITE_OVERLAY is a faster way to clear the image.
        _clear_frame_data = numpy.array([0, 255], dtype=numpy.uint8)
        _clear_frame_block = Tk_PhotoImageBlock(pixelPtr=ctypes.cast(_clear_frame_data.ctypes.data, c_uchar_p), width=1,
                                                height=1, pitch=2, pixelSize=2, offset=(0, 0, 0, 1))

        if DisplayManager.display_method == 'tk':  # upgrade
            DisplayManager.display_method = 'tkf'
    except:
        pass
except ImportError:
    pass


class DM_tk(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.frame_prefix = bytes(f'P6 {self.width} {self.height} 255 ', 'utf-8')
        self.root = tk.Tk()
        self.root.title(self.winname)
        self.root.resizable(False, False)

        def close() -> None:
            self.running = False
            self.close()

        self.root.bind('<Escape>', lambda _: close())
        self.root.protocol('WM_DELETE_WINDOW', close)
        canvas = tk.Canvas(self.root, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        r, g, b, _ = self.scene.bgcolor
        canvas.configure(background=f'#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}')
        self.image = tk.PhotoImage(width=self.width, height=self.height)
        canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        canvas.pack()

    def show_frame(self) -> bool:
        if self.running:
            self.image.put(self.frame_prefix + self.scene.frame[:, :, :3].tobytes())
            self.root.update_idletasks()
            self.root.update()
        return self.running

    def close(self) -> None:
        try:
            self.root.destroy()
        except tk.TclError:
            pass


class DM_tkf(DM_tk, DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.interp = ctypes.cast(self.image.tk.interpaddr(), Tcl_Interp_p)
        self.handle = Tk_FindPhoto(self.interp, self.image.name.encode('utf-8'))
        self.block = Tk_PhotoImageBlock(width=self.width, height=self.height, pitch=4 * self.width, pixelSize=4,
                                        offset=(0, 1, 2, 3))

    def show_frame(self) -> bool:
        if self.running:
            Tk_PhotoPutBlock(self.interp, self.handle, ctypes.byref(_clear_frame_block), 0, 0, self.width, self.height,
                             0)  # fastest way to clear the image
            self.block.pixelPtr = ctypes.cast(self.scene.frame.ctypes.data, c_uchar_p)
            Tk_PhotoPutBlock(self.interp, self.handle, ctypes.byref(self.block), 0, 0, self.width, self.height, 0)
            self.root.update_idletasks()
            self.root.update()
        return self.running

    def close(self) -> None:
        DM_tk.close(self)


# cv2
try:
    import cv2

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'cv2'
except ImportError:
    pass


class DM_cv2(DisplayManager):
    def show_frame(self) -> bool:
        if self.running:
            cv2.imshow(self.winname, cv2.cvtColor(self.scene.frame, cv2.COLOR_RGBA2BGR))
            if cv2.waitKey(int(self.waittime() * 1000)) & 0xff == 27 or cv2.getWindowProperty(self.winname,
                                                                                              cv2.WND_PROP_AUTOSIZE) < 0:
                self.running = False
                self.close()
        return self.running

    def close(self) -> None:
        try:
            cv2.destroyWindow(self.winname)
        except cv2.error:
            pass


# plt
try:
    import matplotlib
    from matplotlib import backend_bases, pyplot as plt

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'plt'
except ImportError:
    pass


class DM_plt(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._default_toolbar = matplotlib.rcParams['toolbar']
        matplotlib.rcParams['toolbar'] = 'None'
        dpi = float(matplotlib.rcParams['figure.dpi'])
        self.fig = plt.figure(num=self.winname, figsize=(self.width / dpi, self.height / dpi))
        self.fig.patch.set_facecolor(self.scene.bgcolor)
        self.fig.subplots_adjust(0, 0, 1, 1)

        def close(event: Any) -> None:
            if event.key == 'escape':
                self.close()

        self.fig.canvas.mpl_connect('key_press_event', close)
        backend = plt.get_backend().lower()
        if backend.startswith('tk'):
            self.fig.canvas.manager.window.resizable(False, False)
        elif backend.startswith('qt'):
            window = self.fig.canvas.window()
            window.setFixedSize(window.size())
        self.img = plt.imshow(self.scene.frame, interpolation='nearest')
        plt.axis('off')
        plt.ion()
        plt.show()

    def show_frame(self) -> bool:
        if plt.fignum_exists(self.fig.number):
            self.img.set_data(self.scene.frame)
            self.fig.canvas.draw_idle()
            self.fig.canvas.start_event_loop(self.waittime())
            return True
        return False

    def close(self) -> None:
        plt.close(self.fig.number)
        matplotlib.rcParams['toolbar'] = self._default_toolbar
