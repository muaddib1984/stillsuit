#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Siggen Oz39
# Author: muaddib
# Description: radio head for passing I/Q to other flowgraphs
# GNU Radio version: 3.9.4.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading




class siggen_oz39(gr.top_block):

    def __init__(self, control_ip='127.0.0.1', control_port=8000, rf_bw=20e6, rf_freq=750e6, rf_gain=1, samp_rate=20e6, zmq_out_ip='127.0.0.1', zmq_out_port=5000):
        gr.top_block.__init__(self, "Siggen Oz39", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.control_ip = control_ip
        self.control_port = control_port
        self.rf_bw = rf_bw
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate
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
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (rf_bw/2)*.8,
                1e6,
                window.WIN_HAMMING,
                6.76))
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(rf_gain, 1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_add_xx_0, 0))


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
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.rf_bw/2)*.8, 1e6, window.WIN_HAMMING, 6.76))

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.blocks_multiply_const_xx_0.set_k(self.rf_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.rf_bw/2)*.8, 1e6, window.WIN_HAMMING, 6.76))

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
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(1)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    parser.add_argument(
        "-o", "--zmq-out-ip", dest="zmq_out_ip", type=str, default='127.0.0.1',
        help="Set ZMQ OUT IP ADDR [default=%(default)r]")
    return parser


def main(top_block_cls=siggen_oz39, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(control_ip=options.control_ip, control_port=options.control_port, rf_bw=options.rf_bw, rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate, zmq_out_ip=options.zmq_out_ip)

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
