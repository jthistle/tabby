
import synth.sf2.decode as decode
from .sfmodulator import SFModulator
from .definitions import SFGeneralController, SFGenerator, SFTransform


class Modulator:
    def __init__(self, src, dest, amount, amt_src, trans):
        self.src = src
        self.dest = dest
        self.amount = amount
        self.amt_src = amt_src
        self.trans = trans

    @classmethod
    def from_default_def(cls, src: int, dest: SFGenerator, amount: int, amt_src: int, trans: int):
        return cls(SFModulator(src), dest, amount, SFModulator(amt_src), SFTransform(0))

    @classmethod
    def from_raw(cls, mod):
        # Soundfont 2.01 spec, 8.2
        mod_src_oper = decode.WORD(mod[:2])
        mod_dest_oper = decode.WORD(mod[2:4])
        mod_amount = decode.SHORT(mod[4:6])

        mod_amt_src_oper = decode.WORD(mod[6:8])
        mod_trans_oper = decode.WORD(mod[8:10])

        src_oper_real = SFModulator(mod_src_oper)
        amt_src_oper_real = SFModulator(mod_amt_src_oper)

        # "Modulators with sfModAmtSrcOper set to ‘link’ are ignored."
        if amt_src_oper_real.is_general_controller and amt_src_oper_real.controller == SFGeneralController.link:
            return None

        generator = None
        if mod_dest_oper & 0b10000000:
            # is a link to a generator
            generator = mod_dest_oper ^ 0b10000000
        else:
            # is a sfgenerator enum type
            generator = SFGenerator(mod_dest_oper)

        mod_trans_real = SFTransform(mod_trans_oper)

        return cls(src_oper_real, generator, mod_amount, amt_src_oper_real, mod_trans_real)

    def __eq__(self, b):
        """
        A Modulator is defined as identical to another modulator if its source, destination, amount source, and transform are the same in both modulators.
        """
        return (
                self.src == b.src
            and self.dest == b.dest
            and self.amt_src == b.amt_src
            and self.trans == b.trans
        )

    def __str__(self):
        return "Modulator, \n- source {} \n- dest {} \n- amount {} \n- amount source {} \n- transform {}".format(
            self.src, self.dest, self.amount, self.amt_src, self.trans
        )

