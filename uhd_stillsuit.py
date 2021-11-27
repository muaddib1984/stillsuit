#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Uhd Stillsuit
# Author: muaddib
# Description: radio head for passing I/Q to other flowgraphs
# GNU Radio version: 3.9.4.0

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading




class uhd_stillsuit(gr.top_block):

    def __init__(self, control_ip='127.0.0.1', control_port=8000, rf_bw=20e6, rf_freq=750e6, rf_gain=50.0, samp_rate=20e6, uhd_address="", uhd_args="", zmq_out_ip='127.0.0.1', zmq_out_port=5000):
        gr.top_block.__init__(self, "Uhd Stillsuit", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.control_ip = control_ip
        self.control_port = control_port
        self.rf_bw = rf_bw
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate
        self.uhd_address = uhd_address
        self.uhd_args = uhd_args
        self.zmq_out_ip = zmq_out_ip
        self.zmq_out_port = zmq_out_port

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, "tcp://"+str(zmq_out_ip)+":"+str(zmq_out_port), 100, True, -1, '')
        self.xmlrpc_serv_ip = SimpleXMLRPCServer(('127.0.0.1', control_port), allow_none=True)
        self.xmlrpc_serv_ip.register_instance(self)
        self.xmlrpc_serv_ip_thread = threading.Thread(target=self.xmlrpc_serv_ip.serve_forever)
        self.xmlrpc_serv_ip_thread.daemon = True
        self.xmlrpc_serv_ip_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join((uhd_address, uhd_args)),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(rf_freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(rf_bw, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(rf_gain, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.zeromq_pub_sink_0_0, 0))


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
        self.uhd_usrp_source_0.set_bandwidth(self.rf_bw, 0)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.uhd_usrp_source_0.set_center_freq(self.rf_freq, 0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.uhd_usrp_source_0.set_gain(self.rf_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_uhd_address(self):
        return self.uhd_address

    def set_uhd_address(self, uhd_address):
        self.uhd_address = uhd_address

    def get_uhd_args(self):
        return self.uhd_args

    def set_uhd_args(self, uhd_args):
        self.uhd_args = uhd_args

    def get_zmq_out_ip(self):
        return self.zmq_out_ip

    def set_zmq_out_ip(self, zmq_out_ip):
        self.zmq_out_ip = zmq_out_ip

    def get_zmq_out_port(self):
        return self.zmq_out_port

    def set_zmq_out_port(self, zmq_out_port):
        self.zmq_out_port = zmq_out_port



def argument_parser():
    description = 'radio head for passing I/Q to other flowgraphs'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-x", "--control-ip", dest="control_ip", type=str, default='127.0.0.1',
        help="Set XMLRPC SERVER IP [default=%(default)r]")
    parser.add_argument(
        "-X", "--control-port", dest="control_port", type=intx, default=8000,
        help="Set XMLRPC SERVER PORT [default=%(default)r]")
    parser.add_argument(
        "-b", "--rf-bw", dest="rf_bw", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set RF BANDWITDH [default=%(default)r]")
    parser.add_argument(
        "-f", "--rf-freq", dest="rf_freq", type=eng_float, default=eng_notation.num_to_str(float(750e6)),
        help="Set RF FREQUENCY [default=%(default)r]")
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(50.0)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    parser.add_argument(
        "-I", "--uhd-address", dest="uhd_address", type=str, default="",
        help="Set UHD Device Address (example: 'serial=ABCD1234' or 'addr=192.168.1.2') [default=%(default)r]")
    parser.add_argument(
        "-A", "--uhd-args", dest="uhd_args", type=str, default="",
        help="Set UHD ARGS (example: 'rcv_frame_size=8192,num_rcv_frames=128') [default=%(default)r]")
    parser.add_argument(
        "-o", "--zmq-out-ip", dest="zmq_out_ip", type=str, default='127.0.0.1',
        help="Set ZMQ OUT IP ADDR [default=%(default)r]")
    return parser


def main(top_block_cls=uhd_stillsuit, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(control_ip=options.control_ip, control_port=options.control_port, rf_bw=options.rf_bw, rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate, uhd_address=options.uhd_address, uhd_args=options.uhd_args, zmq_out_ip=options.zmq_out_ip)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
