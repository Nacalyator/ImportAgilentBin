# ImportAgilentBin
## Import data and file description (header) from Agilent binary data files

### importAgilentBin(file_path[, num_of_channel])
Takes one (path to the file) or two (path to the file and number of channel) arguments.
Returns two list with time and voltage data.

### importAgilentBinDesc('test.bin')
Takes one (path to the file) argument.
Returns list with dictionaries, which amount equals to number of channel.

Usage
```
import ImportAgilentBin as IAB

time_vector, voltage_vector = IAB.importAgilentBin('test.bin'[, num_of_channel])
desc = IAB.importAgilentBinDesc('test.bin')
```

### Aknowledgments
This module based on the code of [Matlab](https://www.mathworks.com/matlabcentral/fileexchange/11854-agilent-scope-waveform-bin-file-binary-reader)

Additional information about headers is available [here](https://github.com/FaustinCarter/agilent_read_binary)
