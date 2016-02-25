import sumpf
import nlsp
import time
import itertools
import nlsp.common.plots as plot

def differentlength_evaluation(input_generator,branches,iden_method,Plot):
    """
    Evaluation of System Identification method by hgm virtual nl system
    nonlinear system - virtual hammerstein group model with power series polynomials as nl function and bandpass filters
                        as linear functions
    inputsignal - signal signal
    plot - the original filter spectrum and the identified filter spectrum, the reference output and identified output
    expectation - utmost similarity between the two spectrums
    """
    length = [2**17,2**18,2**19]
    for signal_length in length:
        input_generator.SetLength(signal_length)
        print input_generator.GetLength()
        input_signal = input_generator.GetOutput()
        filter_spec_tofind = nlsp.log_bpfilter(branches=branches,input=input_signal)
        ref_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nlsp.nl_branches(nlsp.function_factory.power_series,branches),
                                                     filter_irs=filter_spec_tofind,
                                                     max_harmonics=range(1,branches+1))

        found_filter_spec, nl_functions = iden_method(input_generator,ref_nlsystem.GetOutput(),branches)
        iden_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nl_functions,
                                                     filter_irs=found_filter_spec,
                                                     max_harmonics=range(1,branches+1))

        if Plot is True:
            plot.relabelandplotphase(sumpf.modules.FourierTransform(ref_nlsystem.GetOutput()).GetSpectrum(),"Reference Output",False)
            plot.relabelandplotphase(sumpf.modules.FourierTransform(iden_nlsystem.GetOutput()).GetSpectrum(),"Identified Output",True)
        print "SNR between Reference and Identified output : %r, input length: %r" %(nlsp.snr(ref_nlsystem.GetOutput(),
                                                                                     iden_nlsystem.GetOutput()),len(input_signal))

def differentbranches_evaluation(input_generator,branches,iden_method,Plot):
    for branches in range(3,branches+2):
        input_signal = input_generator.GetOutput()

        filter_spec_tofind = nlsp.log_bpfilter(branches=branches,input=input_signal)
        ref_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nlsp.nl_branches(nlsp.function_factory.power_series,branches),
                                                     filter_irs=filter_spec_tofind,
                                                     max_harmonics=range(1,branches+1))

        found_filter_spec, nl_functions = iden_method(input_generator,ref_nlsystem.GetOutput(),branches)
        iden_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nl_functions,
                                                     filter_irs=found_filter_spec,
                                                     max_harmonics=range(1,branches+1))

        if Plot is True:
            plot.relabelandplotphase(sumpf.modules.FourierTransform(ref_nlsystem.GetOutput()).GetSpectrum(),"Reference Output",False)
            plot.relabelandplotphase(sumpf.modules.FourierTransform(iden_nlsystem.GetOutput()).GetSpectrum(),"Identified Output",True)
        print "SNR between Reference and Identified output : %r, with number of branches: %r" %(nlsp.snr(ref_nlsystem.GetOutput(),
                                                                                     iden_nlsystem.GetOutput()),branches)

def computationtime_evaluation(input_generator,branches,iden_method,Plot):

    inputgenerator = input_generator
    branch = reversed(range(2,branches+1))
    length = reversed([2**17,2**18,2**19])
    for branches,signal_length in itertools.product(branch,length):

        simulation_time_start = time.clock()
        inputgenerator.SetLength(signal_length)
        input_signal = inputgenerator.GetOutput()
        filter_spec_tofind = nlsp.log_bpfilter(branches=branches,input=input_signal)
        nl_func = nlsp.nl_branches(nlsp.function_factory.power_series,branches)
        ref_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nl_func,
                                                     filter_irs=filter_spec_tofind,
                                                     max_harmonics=range(1,branches+1))

        identification_time_start = time.clock()
        found_filter_spec, nl_functions = iden_method(input_generator,ref_nlsystem.GetOutput(),branches)
        identification_time_stop = time.clock()
        iden_nlsystem = nlsp.HammersteinGroupModel_up(input_signal=input_signal,
                                                     nonlinear_functions=nl_functions,
                                                     filter_irs=found_filter_spec,
                                                     max_harmonics=range(1,branches+1))
        iden_nlsystem.GetOutput()
        simulation_time_stop = time.clock()
        simulation_time = simulation_time_stop - simulation_time_start
        identification_time = identification_time_stop - identification_time_start

        print "Signal length: %r, branches: %r, simulation time: %r, identification time: %r" %(signal_length,branches,
                                                                                                simulation_time,
                                                                                                identification_time)
