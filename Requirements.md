Feature:
As a researcher, I want to compute the Fourier transform of the position expectation value, so that I can determine the frequency of the oscillation.
Scenario: Dominant frequency recovered from a known signal
GIVEN the file "data/expec.t" contains a position expectation value sampled at 0.1 fs intervals over 10 fs
      And the signal contains a dominant oscillation at 0.25 fs^-1
WHEN the researcher computes the Fourier transform of the position column
THEN the resulting spectrum has its peak at 0.25 fs^-1 within tolerance 0.01
      And the peak amplitude exceeds the noise floor by at least a factor of 10

Feature:
As a researcher I want to plot the position expectation value over time, so that I can confirm the simulation produced a clean oscillation before running downstream analysis.
Background: Given the file "data/expec.t" contains columns "time" and "position" sampled at 0.1 fs intervals over 10 fs
Scenario: Plot is produced and saved
WHEN the researcher plots the position column against time
THEN a file "results/expec_plot.png" is written
      And the file is a valid PNG with non-zero size

Scenario: Plot reflects the underlying data range
Given the position values lie within [-1.0, 1.0]
WHEN the researcher plots the position column against time
THEN the y-axis limits cover the range [-1.0, 1.0] with at most 10% padding
      And the x-axis limits cover [0, 1000] fs

Feature:
As a researcher I want to apply an exponential damping function to the position expectation value before computing its Fourier transform so that spectral leakage is reduced and only physically meaningful peaks remain visible in the spectrum.
Background: Given the file "data/expec.t" contains a position expectation value sampled at 0.1 fs intervals over 10 fs
Scenario: Damping function is applied correctly in the time domain
GIVEN a damping time constant of 2 fs
WHEN the researcher applies exponential damping to the position column
THEN each sample at time t is multiplied by exp(-t / 2 fs)
      And the first sample is unchanged
      And the last sample is multiplied by exp(-5) within tolerance 1e-12

Scenario: Damping reduces the discontinuity at the signal boundary
GIVEN the undamped signal has value 0.8 at the final time step
WHEN exponential damping with time constant 2 fs is applied
THEN the final value of the damped signal is below 0.01
      And the damped signal is monotonically smaller in magnitude than the original
