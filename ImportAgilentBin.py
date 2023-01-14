import os.path
import struct

def importAgilentBin(file_path, *vargs):
    # Import data from a binary file from 1st channel
    # time_vector, voltage_vector = importAgilentBin(file_path)
    #
    # Import data from a binary file from any channel
    # time_vector, voltage_vector = importAgilentBin(file_path, channel)
    #
    # In case of errors function will return two empty lists
    
    # Prepare output variables
    voltage_vector = []
    time_vector = []

    # Check if file doesn't exist
    if not os.path.isfile(file_path):
        print('Input filename missing')
        f.close()
        return None
    f = open(file_path, 'rb')
    
    # Read header of the file
    file_cookie = str(f.read(2), 'utf-8')
    file_version = str(f.read(2), 'utf-8')
    file_size = int.from_bytes(f.read(4), 'little')
    n_waveforms = int.from_bytes(f.read(4), 'little')

    # Verify cookie
    if file_cookie != 'AG':
        print('Unrecognised file format')
        f.close()
        return None

    # Determine which waveform to read
    waveform_index = 0
    if len(vargs) == 1 and 1 <= vargs[0] <= n_waveforms:
        waveform_index = vargs[0] - 1
    
    # Read waveform header(s)
    for i in range(n_waveforms):
        header_size = int.from_bytes(f.read(4), 'little')
        waveform_type = int.from_bytes(f.read(4), 'little')
        n_waveforms_buffers = int.from_bytes(f.read(4), 'little')
        n_points = int.from_bytes(f.read(4), 'little')
        count = int.from_bytes(f.read(4), 'little')
        x_display_range = struct.unpack('f', f.read(4))[0]
        x_display_origin = struct.unpack('d', f.read(8))[0]
        x_increment = struct.unpack('d', f.read(8))[0]
        x_origin = struct.unpack('d', f.read(8))[0]
        x_units = int.from_bytes(f.read(4), 'little')
        y_units = int.from_bytes(f.read(4), 'little')
        date_string = str(f.read(16), 'utf-8').replace('\x00', ' ')
        time_string = str(f.read(16), 'utf-8').replace('\x00', ' ')
        frame_string = str(f.read(24), 'utf-8').replace('\x00', ' ')
        waveform_string = str(f.read(16), 'utf-8').replace('\x00', ' ')
        time_tag = float(int.from_bytes(f.read(8), 'little', signed='true'))
        segment_index = int.from_bytes(f.read(4), 'little')
        
        # Generate time vector
        if waveform_index == i:
            for t_i in range(n_points):
                time_vector.append(t_i * x_increment + x_origin)

        # Read voltage vector
        for b_i in range(n_waveforms_buffers):
            # Read waveform buffer header
            b_header_size = int.from_bytes(f.read(4), 'little')
            b_buffer_type = int.from_bytes(f.read(2), 'little')
            b_bytes_per_point = int.from_bytes(f.read(2), 'little')
            b_buffer_size = int.from_bytes(f.read(4), 'little')
            
            # Read voltage vector with buffer type
            if waveform_index == i:
                if b_buffer_type in (1, 2, 3):
                    # PB_DATA_NORMAL
                    # PB_DATA_MIN
                    # PB_DATA_MAX
                    for i in range(int(n_points)):
                        voltage_vector.append(struct.unpack('<f', f.read(4))[0])
                elif b_buffer_type == 4:
                    # PB_DATA_COUNTS
                    for i in range(int(n_points)):
                        voltage_vector.append(int.from_bytes(f.read(4), 'little'))
                elif b_buffer_type == 5:
                    # PB_DATA_LOGIC
                    for i in range(int(n_points)):
                        voltage_vector.append(struct.unpack('?', f.read(1))[0])
                elif b_buffer_type == 6:
                    # PB_DATA_NORMAL
                    for i in range(int(n_points)):
                        voltage_vector.append(struct.unpack('?', f.read(1))[0])
            else:
                f.seek(b_buffer_size, 1)
    f.close()
    return time_vector, voltage_vector


def importAgilentBinDesc(file_path):
    # Import data from a binary file from 1st channel
    # time_vector, voltage_vector = importAgilentBin(file_path)
    #
    # Import data from a binary file from any channel
    # time_vector, voltage_vector = importAgilentBin(file_path, channel)
    #
    # In case of errors function will return two empty lists

    # Check if file doesn't exist
    if not os.path.isfile(file_path):
        print('Input filename missing')
        f.close()
        return None
    f = open(file_path, 'rb')
    
    # Read header of the file
    file_cookie = str(f.read(2), 'utf-8')
    file_version = str(f.read(2), 'utf-8')
    file_size = int.from_bytes(f.read(4), 'little')
    n_waveforms = int.from_bytes(f.read(4), 'little')

    # Verify cookie
    if file_cookie != 'AG':
        print('Unrecognised file format')
        f.close()
        return None

    # Prepare output variables
    desc = []

    # Read waveform header(s)
    for i in range(n_waveforms):
        buff = {
            'header_size': int.from_bytes(f.read(4), 'little'),
            'waveform_type': int.from_bytes(f.read(4), 'little'),
            'n_waveforms_buffers': int.from_bytes(f.read(4), 'little'),
            'n_points': int.from_bytes(f.read(4), 'little'),
            'count': int.from_bytes(f.read(4), 'little'),
            'x_display_range': struct.unpack('f', f.read(4))[0],
            'x_display_origin': struct.unpack('d', f.read(8))[0],
            'x_increment': struct.unpack('d', f.read(8))[0],
            'x_origin': struct.unpack('d', f.read(8))[0],
            'x_units': int.from_bytes(f.read(4), 'little'),
            'y_units': int.from_bytes(f.read(4), 'little'),
            'date_string': str(f.read(16), 'utf-8').replace('\x00', ' '),
            'time_string': str(f.read(16), 'utf-8').replace('\x00', ' '),
            'frame_string': str(f.read(24), 'utf-8').replace('\x00', ' '),
            'waveform_string': str(f.read(16), 'utf-8').replace('\x00', ' '),
            'time_tag': float(int.from_bytes(f.read(8), 'little', signed='true')),
            'segment_index': int.from_bytes(f.read(4), 'little')
        }
        # Save the header data
        desc.append(buff)

        # Read voltage vector
        for b_i in range(buff['n_waveforms_buffers']):
            # Read waveform buffer header
            b_header_size = int.from_bytes(f.read(4), 'little')
            b_buffer_type = int.from_bytes(f.read(2), 'little')
            b_bytes_per_point = int.from_bytes(f.read(2), 'little')
            b_buffer_size = int.from_bytes(f.read(4), 'little')
            f.seek((b_buffer_size), 1)
            #f.seek(b_buffer_size, 1)
    f.close()
    return desc