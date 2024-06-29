#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GSM TESTING
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gsm
import pmt
from gnuradio import network
import sip



class GSM_TESTING(gr.top_block, Qt.QWidget):

    def __init__(self, ppm_param=0):
        gr.top_block.__init__(self, "GSM TESTING", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GSM TESTING")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "GSM_TESTING")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.ppm_param = ppm_param

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.ppm = ppm = 0
        self.osr = osr = 4
        self.g = g = 43
        self.fc = fc = 939e6
        self.SDCCH = SDCCH = 6
        self.RACH = RACH = 3
        self.PCH = PCH = 5
        self.CHANNEL_UNKNOWN = CHANNEL_UNKNOWN = 0
        self.CCCH = CCCH = 2
        self.BCCH = BCCH = 1
        self.AGCH = AGCH = 4

        ##################################################
        # Blocks
        ##################################################

        self._ppm_range = qtgui.Range(-150, 150, 1, 0, 200)
        self._ppm_win = qtgui.RangeWidget(self._ppm_range, self.set_ppm, "clock_correction [ppm]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._ppm_win)
        self._fc_range = qtgui.Range(925e6, 960e6, 200e3, 939e6, 200)
        self._fc_win = qtgui.RangeWidget(self._fc_range, self.set_fc, "center_frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fc_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            fc, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', '127.0.0.1', '5555', 10000, False)
        self.gsm_universal_ctrl_chans_demapper_0 = gsm.universal_ctrl_chans_demapper(0, [0,0,2,2,2,2,6,6,6,6,0,0,12,12,12,12,16,16,16,16,0,0,22,22,22,22,26,26,26,26,0,0,32,32,32,32,36,36,36,36,0,0,42,42,42,42,46,46,46,46,0,], [0,0,1,1,1,1,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], [0,0,0,0,0,0,6,6,6,6,10,10,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,37,37,37,37,41,41,41,41,0,0,47,47,47,47], [2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
        self.gsm_receiver_0 = gsm.receiver(4, [0], [], False)
        self.gsm_message_printer_0 = gsm.message_printer(pmt.intern(''), False,
            False, False)
        self.gsm_input_0 = gsm.gsm_input(
            ppm=ppm,
            osr=osr,
            fc=fc,
            samp_rate_in=samp_rate,
        )
        self.gsm_control_channels_decoder_0 = gsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = gsm.clock_offset_control(fc, samp_rate, osr)
        self._g_range = qtgui.Range(0, 50, 0.5, 43, 200)
        self._g_win = qtgui.RangeWidget(self._g_range, self.set_g, "gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._g_win)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 939000000, 100, 200, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_clock_offset_control_0, 'ctrl'), (self.gsm_input_0, 'ctrl_in'))
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.gsm_message_printer_0, 'msgs'))
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.network_socket_pdu_0, 'pdus'))
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_universal_ctrl_chans_demapper_0, 'bursts'))
        self.msg_connect((self.gsm_universal_ctrl_chans_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'log'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.gsm_input_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GSM_TESTING")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_ppm_param(self):
        return self.ppm_param

    def set_ppm_param(self, ppm_param):
        self.ppm_param = ppm_param

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc, self.samp_rate)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.gsm_input_0.set_ppm(self.ppm)

    def get_osr(self):
        return self.osr

    def set_osr(self, osr):
        self.osr = osr
        self.gsm_input_0.set_osr(self.osr)

    def get_g(self):
        return self.g

    def set_g(self, g):
        self.g = g

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.gsm_clock_offset_control_0.set_fc(self.fc)
        self.gsm_input_0.set_fc(self.fc)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc, self.samp_rate)

    def get_SDCCH(self):
        return self.SDCCH

    def set_SDCCH(self, SDCCH):
        self.SDCCH = SDCCH

    def get_RACH(self):
        return self.RACH

    def set_RACH(self, RACH):
        self.RACH = RACH

    def get_PCH(self):
        return self.PCH

    def set_PCH(self, PCH):
        self.PCH = PCH

    def get_CHANNEL_UNKNOWN(self):
        return self.CHANNEL_UNKNOWN

    def set_CHANNEL_UNKNOWN(self, CHANNEL_UNKNOWN):
        self.CHANNEL_UNKNOWN = CHANNEL_UNKNOWN

    def get_CCCH(self):
        return self.CCCH

    def set_CCCH(self, CCCH):
        self.CCCH = CCCH

    def get_BCCH(self):
        return self.BCCH

    def set_BCCH(self, BCCH):
        self.BCCH = BCCH

    def get_AGCH(self):
        return self.AGCH

    def set_AGCH(self, AGCH):
        self.AGCH = AGCH



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--ppm-param", dest="ppm_param", type=intx, default=0,
        help="Set ppm [default=%(default)r]")
    return parser


def main(top_block_cls=GSM_TESTING, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ppm_param=options.ppm_param)

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
