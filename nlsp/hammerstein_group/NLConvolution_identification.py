import sumpf
import nlsp
import common.plot as plot

def nonlinearconvolution_identification(input_sweep, output_sweep):
    if isinstance(input_sweep ,(sumpf.Signal)):
        ip_s = input_sweep
        ip = sumpf.modules.FourierTransform(signal=input_sweep).GetSpectrum()
    else:
        ip_s = sumpf.modules.InverseFourierTransform(spectrum=input_sweep).GetSignal()
        ip = input_sweep
    if isinstance(output_sweep ,(sumpf.Signal)):
        op = sumpf.modules.FourierTransform(signal=output_sweep).GetSpectrum()
    else:
        op = output_sweep
    spec_inversion = sumpf.modules.RegularizedSpectrumInversion(spectrum=ip).GetOutput()
    mul = sumpf.modules.MultiplySpectrums(spectrum1=spec_inversion, spectrum2=op).GetOutput()
    it = sumpf.modules.InverseFourierTransform(spectrum=mul).GetSignal()
    direct_ir = sumpf.modules.CutSignal(signal=it,start=0,stop=2**12).GetOutput()
    merger = sumpf.modules.MergeSignals(on_length_conflict=sumpf.modules.MergeSignals.FILL_WITH_ZEROS)
    merger.AddInput(direct_ir)
    for i in range(4):
        split_harm = sumpf.modules.FindHarmonicImpulseResponse(impulse_response=it,
                                                               harmonic_order=i+2).GetHarmonicImpulseResponse()
        resampler = sumpf.modules.ResampleSignal(signal=split_harm, samplingrate=ip_s.GetSamplingRate()).GetOutput()
        merger.AddInput(resampler)
    harm_spec = sumpf.modules.FourierTransform(signal=merger.GetOutput()).GetSpectrum()
    harmonics = []
    for i in range(len(harm_spec.GetChannels())):
        split =  sumpf.modules.SplitSpectrum(data=harm_spec,channels=[i]).GetOutput()
        harmonics.append(split)
    H = []
    H.append(harmonics[0] + 3*harmonics[2] +5*harmonics[4])
    H.append(sumpf.modules.AmplifySpectrum(input=harmonics[1],factor=2j).GetOutput() +
             sumpf.modules.AmplifySpectrum(input=harmonics[3],factor=8j).GetOutput())
    H.append(-4*harmonics[2] - 20*harmonics[4])
    H.append(sumpf.modules.AmplifySpectrum(input=harmonics[3],factor=-8j).GetOutput())
    H.append(16*harmonics[4])
    h = []
    for kernel in H:
        ift = sumpf.modules.InverseFourierTransform(spectrum=kernel).GetSignal()
        h.append(ift)
    return h
