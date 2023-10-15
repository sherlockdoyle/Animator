"""Implementations of different display managers. This currently supports Qt (4 and 5), Tkinter (a slow and a fast
version), OpenCV, and Matplotlib. The slower Tkinter version and OpenCV does not support transparency. The best display
manager will be automatically selected."""
from __future__ import annotations

import time
from typing import Any

from animator import skia
from animator.display.DisplayManager import DisplayManager
from animator.util.env import inside_notebook

# in browser
if inside_notebook():
    from base64 import b64encode

    from IPython.display import HTML, clear_output, display

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'html'


class DM_html(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.img: skia.Image = skia.Image.fromarray(self.scene.frame, copy=False)
        self.prefix = (
            '<div style="display:flex;justify-content:center;align-items:center">'
            f'<img style="max-width:100%;max-height:100%"id="{self.winname}"src="data:image/png;base64,'
        )
        self.suffix = '"></div>'
        self.show_frame()

    def frame_b64(self) -> str:
        return b64encode(self.img.encodeToData().bytes()).decode('utf-8')

    def show_frame(self) -> bool:
        display(HTML(self.prefix + self.frame_b64() + self.suffix))
        clear_output(True)
        return True


# qt
try:
    from PyQt4 import QtCore, QtGui

    QtWidgets = QtGui
    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'qt'
except ImportError:
    try:
        from PyQt5 import QtCore, QtGui, QtWidgets

        if DisplayManager.display_method is None:
            DisplayManager.display_method = 'qt'
    except ImportError:

        class QtWidgets:  # dummy class
            class QMainWindow:
                pass


class DM_qt(DisplayManager):
    class Window(QtWidgets.QMainWindow):
        def __init__(self, manager: DM_qt):
            super().__init__()
            self._manager: DM_qt = manager

            self.setWindowTitle(manager.winname)
            screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()
            self.setGeometry(
                screen_center.x() - manager.width // 2,
                screen_center.y() - manager.height // 2,
                manager.width,
                manager.height,
            )
            self.setFixedSize(manager.width, manager.height)

            r, g, b, _ = manager.scene.bgcolor
            self.setStyleSheet(f'background-color:rgb({r * 255},{g * 255},{b * 255});border:none')

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.app = QtWidgets.QApplication([])
        self.window = DM_qt.Window(self)

    def show_frame(self) -> bool:
        if self.running:
            self.window.pixmap.setPixmap(
                QtGui.QPixmap(
                    QtGui.QImage(self.scene.frame.data, self.width, self.height, QtGui.QImage.Format_RGBA8888)
                )
            )
            time.sleep(self.waittime())
            self.app.processEvents()
        return self.running

    def close(self) -> None:
        self.window.close()


# tk
try:
    import tkinter as tk

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'tk'
    try:
        # tk is very slow with images, so we try to achieve a better framerate by directly calling the C functions from
        # the tk8.6 library, if available. Even this is slow, so neither of the tk display managers waits between
        # frames.
        import ctypes
        import ctypes.util

        import _tkinter
        import numpy as np

        libname = ctypes.util.find_library(f'tk{_tkinter.TK_VERSION}')
        if libname is None:
            raise ImportError
        libtk = ctypes.cdll.LoadLibrary(libname)
        Tcl_Interp_p = ctypes.c_void_p
        c_uchar_p = ctypes.POINTER(ctypes.c_ubyte)

        class Tk_PhotoImageBlock(ctypes.Structure):
            _fields_ = [
                ('pixelPtr', c_uchar_p),
                ('width', ctypes.c_int),
                ('height', ctypes.c_int),
                ('pitch', ctypes.c_int),
                ('pixelSize', ctypes.c_int),
                ('offset', ctypes.c_int * 4),
            ]

        Tk_FindPhoto = libtk.Tk_FindPhoto
        Tk_FindPhoto.argtypes = [Tcl_Interp_p, ctypes.c_char_p]
        Tk_FindPhoto.restype = ctypes.c_void_p

        Tk_PhotoPutBlock = libtk.Tk_PhotoPutBlock
        Tk_PhotoPutBlock.argtypes = [
            Tcl_Interp_p,
            ctypes.c_void_p,
            ctypes.POINTER(Tk_PhotoImageBlock),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        Tk_PhotoPutBlock.restype = None

        # tk recalculates valid regions (blits) after a PhotoPutBlock call with COMPOSITE_SET rule. This is normally
        # fast, but if we have random transparent pixels, it (also PhotoBlank) can be very slow. So we use PhotoPutBlock
        # with the following block of pixels and COMPOSITE_OVERLAY rule to clear the image.
        _clear_data = np.array([0, 255], dtype=np.uint8)
        _clear_block = Tk_PhotoImageBlock(
            pixelPtr=_clear_data.ctypes.data_as(c_uchar_p),
            width=1,
            height=1,
            pitch=2,
            pixelSize=12,
            offset=(0, 0, 0, 1),
        )
        if DisplayManager.display_method == 'tk':  # upgrade
            DisplayManager.display_method = 'tkf'
    except:
        # in case of error, just use the slow tk display manager
        pass
except ImportError:
    pass


class DM_tk(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.frame_prefix = f'P6 {self.width} {self.height} 255 '.encode('utf-8')
        self.root = tk.Tk()
        self.root.title(self.winname)
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.resizable(False, False)

        def close() -> None:
            self.running = False
            self.close()

        self.root.protocol('WM_DELETE_WINDOW', close)
        self.root.bind('<Escape>', lambda _: close())

        canvas = tk.Canvas(self.root, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        r, g, b, _ = self.scene.bgcolor
        canvas.configure(background=f'#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}')
        self.image = tk.PhotoImage(width=self.width, height=self.height)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
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
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.interp = ctypes.cast(self.image.tk.interpaddr(), Tcl_Interp_p)
        self.handle = Tk_FindPhoto(self.interp, self.image.name.encode('utf-8'))
        self.block = Tk_PhotoImageBlock(
            width=self.width, height=self.height, pitch=self.width * 4, pixelSize=4, offset=(0, 1, 2, 3)
        )

    def show_frame(self) -> bool:
        if self.running:
            Tk_PhotoPutBlock(
                self.interp, self.handle, ctypes.byref(_clear_block), 0, 0, self.width, self.height, 0
            )  # fastest way to clear the image
            self.block.pixelPtr = self.scene.frame.ctypes.data_as(c_uchar_p)
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
            if (
                cv2.waitKey(int(self.waittime() * 1000)) & 0xFF == 27
                or cv2.getWindowProperty(self.winname, cv2.WND_PROP_AUTOSIZE) < 0
            ):
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
    from matplotlib import backend_bases
    from matplotlib import pyplot as plt

    if DisplayManager.display_method is None:
        DisplayManager.display_method = 'plt'
except ImportError:
    pass


class DM_plt(DisplayManager):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._default_toolbar = matplotlib.rcParams['toolbar']
        matplotlib.rcParams['toolbar'] = 'None'
        dpi = matplotlib.rcParams['figure.dpi']
        self.fig = plt.figure(self.winname, figsize=(self.width / dpi, self.height / dpi))
        self.fig.patch.set_facecolor(self.scene.bgcolor)
        self.fig.subplots_adjust(0, 0, 1, 1)

        def close(event: backend_bases.KeyEvent) -> None:
            if event.key == 'escape':
                self.close()

        self.fig.canvas.mpl_connect('key_press_event', close)
        backend = plt.get_backend().lower()
        if backend.startswith('qt'):
            window = self.fig.canvas.window()
            window.setFixedSize(window.size())
        elif backend.startswith('tk'):
            self.fig.canvas.manager.window.resizable(False, False)
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
        self.running = False
