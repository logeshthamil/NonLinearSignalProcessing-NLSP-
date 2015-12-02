import sumpf
import common

class ClippingHammersteinGroupModel(object):
    def __init__(self, signal=None, thresholds_list=None, filters=None, amplificationfactor=None):

        if amplificationfactor is None:
            self.__amplificationfactor = 1.0
        else:
            self.__amplificationfactor = amplificationfactor

        self.__clipping = []
        self.__ffts = []
        self.__filterspec = []
        self.__iffts = []
        self.__sums = [None] * len(filters)

        self.__inputstage = sumpf.modules.AmplifySignal(factor=self.__amplificationfactor)
        self.__inputstage.SetInput(input=signal)
        for spectrum,threshold in zip(filters,thresholds_list):
            # c = common.ClipSignal(thresholds=threshold)
            c = sumpf.modules.ClipSignal(thresholds=threshold)
            t = sumpf.modules.FourierTransform()
            f = sumpf.modules.MultiplySpectrums(spectrum2=spectrum)
            i = sumpf.modules.InverseFourierTransform()
            sumpf.connect(self.__inputstage.GetOutput, c.SetInput)
            sumpf.connect(c.GetOutput, t.SetSignal)
            sumpf.connect(t.GetSpectrum, f.SetInput1)
            sumpf.connect(f.GetOutput, i.SetSpectrum)
            self.__clipping.append(c)
            self.__ffts.append(t)
            self.__filterspec.append(f)
            self.__iffts.append(i)
        for i in reversed(range(len(self.__filterspec)-1)):
            a = sumpf.modules.AddSignals()
#            print "connecting ifft %i to adder %i" % (i, i)
            sumpf.connect(self.__iffts[i].GetSignal, a.SetInput1)
            if i == len(self.__filterspec)-2:
#                print "connecting ifft %i to adder %i" % (i+1, i)
                sumpf.connect(self.__iffts[i+1].GetSignal, a.SetInput2)
            else:
#                print "connecting adder %i to adder %i" % (i+1, i)
                sumpf.connect(self.__sums[i+1].GetOutput, a.SetInput2)
            self.__sums[i] = a

        # make the input and output methods of the signal processing chain available
        self.SetInput = self.__inputstage.SetInput
        self.GetOutput = self.__sums[0].GetOutput

    def SetParameters(self, thresholds_list, filters):
        pairs = []
        for i, t in enumerate(thresholds_list):
            pairs.append((self.__clipping[i].SetThresholds, t))
        for i, f in enumerate(filters):
            pairs.append((self.__filterspec[i].SetInput2, f))
        sumpf.set_multiple_values(pairs)

class ClippingHammersteinGroupModelWithCascadedLinearity(object):
      def __init__(self, signal=None, thresholds_list=None, nonlinearfilters=None, amplificationfactor=None,  linearfilter=None):

        if amplificationfactor is None:
            self.__amplificationfactor = 1.0
        else:
            self.__amplificationfactor = amplificationfactor

        self.__clipping = []
        self.__ffts = []
        self.__filterspec = []
        self.__linearfilterspec = []
        self.__iffts = []
        self.__sums = [None] * len(nonlinearfilters)

        self.__inputstages = sumpf.modules.AmplifySignal(factor=self.__amplificationfactor)
        self.__inputstages.SetInput(input=signal)
        for spectrum,threshold in zip(nonlinearfilters,thresholds_list):
            # c = common.ClipSignal(thresholds=threshold)
            c = sumpf.modules.ClipSignal(thresholds=threshold)
            t = sumpf.modules.FourierTransform()
            f = sumpf.modules.MultiplySpectrums(spectrum2=spectrum)
            i = sumpf.modules.InverseFourierTransform()
            sumpf.connect(self.__inputstages.GetOutput, c.SetInput)
            sumpf.connect(c.GetOutput, t.SetSignal)
            sumpf.connect(t.GetSpectrum, f.SetInput1)
            sumpf.connect(f.GetOutput, i.SetSpectrum)
            self.__clipping.append(c)
            self.__ffts.append(t)
            self.__filterspec.append(f)
            self.__iffts.append(i)
        for i in reversed(range(len(self.__filterspec)-1)):
            a = sumpf.modules.AddSignals()
#            print "connecting ifft %i to adder %i" % (i, i)
            sumpf.connect(self.__iffts[i].GetSignal, a.SetInput1)
            if i == len(self.__filterspec)-2:
#                print "connecting ifft %i to adder %i" % (i+1, i)
                sumpf.connect(self.__iffts[i+1].GetSignal, a.SetInput2)
            else:
#                print "connecting adder %i to adder %i" % (i+1, i)
                sumpf.connect(self.__sums[i+1].GetOutput, a.SetInput2)
            self.__sums[i] = a
        self.SetInput = self.__inputstages.SetInput
        self.__lt = sumpf.modules.FourierTransform()
        self.__lf = sumpf.modules.MultiplySpectrums(spectrum2=linearfilter)
        self.__li = sumpf.modules.InverseFourierTransform()
        sumpf.connect(self.__sums[0].GetOutput, self.__lt.SetSignal)
        sumpf.connect(self.__lt.GetSpectrum, self.__lf.SetInput1)
        sumpf.connect(self.__lf.GetOutput, self.__li.SetSpectrum)
        self.__linearfilterspec.append(self.__lf)

        # make the input and output methods of the signal processing chain available
        self.GetOutput = self.__li.GetSignal

      def SetParameters(self, thresholds_list, nonlinearfilters, linearfilter):
        pairs = []
        for i, t in enumerate(thresholds_list):
            pairs.append((self.__clipping[i].SetThresholds, t))
        for i, f in enumerate(nonlinearfilters):
            pairs.append((self.__filterspec[i].SetInput2, f))
        pairs.append((self.__linearfilterspec.SetInput2, linearfilter))
        sumpf.set_multiple_values(pairs)
