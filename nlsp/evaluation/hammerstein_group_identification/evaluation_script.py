import sumpf
import nlsp

sampling_rate = 48000.0
start_freq = 20.0
stop_freq = 20000.0
length = 2**16
fade_out = 0.05
fade_in = 0.05
branches = 5
distribution = sumpf.modules.NoiseGenerator.GaussianDistribution(mean=0.0,standard_deviation=1.0)
iden_method = [nlsp.nonlinearconvolution_powerseries_spectralinversion,nlsp.nonlinearconvolution_powerseries_temporalreversal,
               nlsp.nonlinearconvolution_chebyshev_temporalreversal,nlsp.nonlinearconvolution_chebyshev_spectralinversion]

Plot = False
Save = False

sine = nlsp.NovakSweepGenerator_Sine(sampling_rate=sampling_rate, length=length, start_frequency=start_freq,
                                   stop_frequency=stop_freq, fade_out= fade_out,fade_in=fade_in)
cos = nlsp.NovakSweepGenerator_Cosine(sampling_rate=sampling_rate, length=length, start_frequency=start_freq,
                                   stop_frequency=stop_freq, fade_out= fade_out,fade_in=fade_in)
wgn = nlsp.WhiteGaussianGenerator(sampling_rate=sampling_rate, length=length, start_frequency=start_freq,
                                   stop_frequency=stop_freq, distribution=distribution)
excitation = [sine,sine,cos,cos]

print sine.GetSweepParameter(),sine.GetLength(),len(sine.GetOutput())

for method,input_generator in zip(iden_method,excitation):
    print method,input_generator
    # nlsp.audio_evaluation(input_generator,branches,method,Plot)
    nlsp.hgmwithfilter_evaluation(input_generator,branches,method,Plot)
    nlsp.hgmwithoverlapfilter_evaluation(input_generator,branches,method,Plot)
    nlsp.linearmodel_evaluation(input_generator,branches,method,Plot)
    nlsp.hgmwithreversedfilter_evaluation(input_generator,branches,method,Plot)
    nlsp.hgmwithamplifiedfilter_evaluation(input_generator,branches,method,Plot)

    nlsp.hardclipping_evaluation(input_generator,branches,method,Plot)
    nlsp.softclipping_evaluation(input_generator,branches,method,Plot)
    nlsp.doublehgm_same_evaluation(input_generator,branches,method,Plot)

    nlsp.differentlength_evaluation(input_generator,branches,method,Plot)
    nlsp.differentbranches_evaluation(input_generator,branches,method,Plot)
    nlsp.computationtime_evaluation(input_generator,branches,method,Plot)

    nlsp.robustness_excitation_evaluation(input_generator,branches,method,Plot)
    nlsp.robustness_noise_evaluation(input_generator,branches,method,Plot)

    # nlsp.loudspeakermodel_evaluation("Sweep18","Speech2",branches,method,Plot,Save)
    # nlsp.distortionbox_evaluation("Sweep18","Speech1",branches,method,Plot,Save)



