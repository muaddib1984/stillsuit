#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Stillsuit Simple Controller Nofft
# Author: muaddib
# Description: remote visualizatino for space folder application
# GNU Radio version: 3.10.2.0-rc1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import threading
import numpy as np



from gnuradio import qtgui

class stillsuit_simple_controller_nofft(gr.top_block, Qt.QWidget):

    def __init__(self, control_ip='127.0.0.1', control_port=8002, rf_bw=10e6, rf_freq=750e6, rf_gain=20.0, samp_rate=20e6, zmq_in_ip='127.0.0.1', zmq_in_port=5001):
        gr.top_block.__init__(self, "Stillsuit Simple Controller Nofft", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Stillsuit Simple Controller Nofft")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "stillsuit_simple_controller_nofft")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.control_ip = control_ip
        self.control_port = control_port
        self.rf_bw = rf_bw
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate
        self.zmq_in_ip = zmq_in_ip
        self.zmq_in_port = zmq_in_port

        ##################################################
        # Variables
        ##################################################
        self.samp_ratio = samp_ratio = samp_rate/1E6
        self.samp_rate_gui = samp_rate_gui = 2e6
        self.vec_per_sec = vec_per_sec = 4
        self.rf_gain_gui = rf_gain_gui = 50
        self.rf_freq_gui = rf_freq_gui = 750e6
        self.rf_bw_gui = rf_bw_gui = samp_rate_gui*.8
        self.fft_length = fft_length = 256 * int(pow(2, np.ceil(np.log(samp_ratio)/np.log(2))))

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_gui_range = Range(200e3, 40e6, 1e3, 2e6, 200)
        self._samp_rate_gui_win = RangeWidget(self._samp_rate_gui_range, self.set_samp_rate_gui, "Sample Rate", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_gui_win)
        self.xmlrpc_serv_ip = SimpleXMLRPCServer(('127.0.0.1', control_port), allow_none=True)
        self.xmlrpc_serv_ip.register_instance(self)
        self.xmlrpc_serv_ip_thread = threading.Thread(target=self.xmlrpc_serv_ip.serve_forever)
        self.xmlrpc_serv_ip_thread.daemon = True
        self.xmlrpc_serv_ip_thread.start()
        self.xmlrpc_client_0_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self.xmlrpc_client_0 = ServerProxy('http://'+'127.0.0.1'+':8000')
        self._rf_gain_gui_range = Range(0, 80, 1, 50, 200)
        self._rf_gain_gui_win = RangeWidget(self._rf_gain_gui_range, self.set_rf_gain_gui, "RF GAIN", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_gain_gui_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rf_freq_gui_range = Range(64e6, 6e9, 100e3, 750e6, 200)
        self._rf_freq_gui_win = RangeWidget(self._rf_freq_gui_range, self.set_rf_freq_gui, "RF FREQ", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_freq_gui_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rf_bw_gui_range = Range(200e3, 40e6, 1e3, samp_rate_gui*.8, 200)
        self._rf_bw_gui_win = RangeWidget(self._rf_bw_gui_range, self.set_rf_bw_gui, "Bandwidth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_bw_gui_win)



    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "stillsuit_simple_controller_nofft")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_control_ip(self):
        return self.control_ip

    def set_control_ip(self, control_ip):
        self.control_ip = control_ip

    def get_control_port(self):
        return self.control_port

    def set_control_port(self, control_port):
        self.control_port = control_port

    def get_rf_bw(self):
        return self.rf_bw

    def set_rf_bw(self, rf_bw):
        self.rf_bw = rf_bw

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_ratio(self.samp_rate/1E6)

    def get_zmq_in_ip(self):
        return self.zmq_in_ip

    def set_zmq_in_ip(self, zmq_in_ip):
        self.zmq_in_ip = zmq_in_ip

    def get_zmq_in_port(self):
        return self.zmq_in_port

    def set_zmq_in_port(self, zmq_in_port):
        self.zmq_in_port = zmq_in_port

    def get_samp_ratio(self):
        return self.samp_ratio

    def set_samp_ratio(self, samp_ratio):
        self.samp_ratio = samp_ratio
        self.set_fft_length(256 * int(pow(2, np.ceil(np.log(self.samp_ratio)/np.log(2)))))

    def get_samp_rate_gui(self):
        return self.samp_rate_gui

    def set_samp_rate_gui(self, samp_rate_gui):
        self.samp_rate_gui = samp_rate_gui
        self.set_rf_bw_gui(self.samp_rate_gui*.8)
        self.xmlrpc_client_0_0_0_0.set_samp_rate(self.samp_rate_gui)

    def get_vec_per_sec(self):
        return self.vec_per_sec

    def set_vec_per_sec(self, vec_per_sec):
        self.vec_per_sec = vec_per_sec

    def get_rf_gain_gui(self):
        return self.rf_gain_gui

    def set_rf_gain_gui(self, rf_gain_gui):
        self.rf_gain_gui = rf_gain_gui
        self.xmlrpc_client_0.set_rf_gain(self.rf_gain_gui)

    def get_rf_freq_gui(self):
        return self.rf_freq_gui

    def set_rf_freq_gui(self, rf_freq_gui):
        self.rf_freq_gui = rf_freq_gui
        self.xmlrpc_client_0_0.set_rf_freq(self.rf_freq_gui)

    def get_rf_bw_gui(self):
        return self.rf_bw_gui

    def set_rf_bw_gui(self, rf_bw_gui):
        self.rf_bw_gui = rf_bw_gui
        self.xmlrpc_client_0_0_0.set_rf_bw(self.rf_bw_gui)

    def get_fft_length(self):
        return self.fft_length

    def set_fft_length(self, fft_length):
        self.fft_length = fft_length



def argument_parser():
    description = 'remote visualizatino for space folder application'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-x", "--control-ip", dest="control_ip", type=str, default='127.0.0.1',
        help="Set XMLRPC SERVER IP [default=%(default)r]")
    parser.add_argument(
        "-X", "--control-port", dest="control_port", type=intx, default=8002,
        help="Set XMLRPC SERVER PORT [default=%(default)r]")
    parser.add_argument(
        "-b", "--rf-bw", dest="rf_bw", type=eng_float, default=eng_notation.num_to_str(float(10e6)),
        help="Set RF BANDWITDH [default=%(default)r]")
    parser.add_argument(
        "-f", "--rf-freq", dest="rf_freq", type=eng_float, default=eng_notation.num_to_str(float(750e6)),
        help="Set RF FREQUENCY [default=%(default)r]")
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(20.0)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    parser.add_argument(
        "-z", "--zmq-in-ip", dest="zmq_in_ip", type=str, default='127.0.0.1',
        help="Set ZMQ IN IP ADDR [default=%(default)r]")
    return parser


def main(top_block_cls=stillsuit_simple_controller_nofft, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(control_ip=options.control_ip, control_port=options.control_port, rf_bw=options.rf_bw, rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate, zmq_in_ip=options.zmq_in_ip)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
