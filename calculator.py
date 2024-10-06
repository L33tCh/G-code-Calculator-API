def layer_change(line):
    return line.strip() == ';LAYER_CHANGE'


def find_e(line):
    pos = line.find(' E')
    if pos == -1 or line[0:2] != 'G1':
        return 0.0
    value = ''
    start = pos + 2
    end = line.find(' ', start)
    try:
        value = float(line[start:end].strip())
        return float(value)
    except ValueError:
        print('Error: {}[{}:{}] - "{}"'.format(value, start, end, line.strip()))
        return 0.0


def layer_to_stop_at(usage_array, length):
    layers = len(usage_array)
    total = 0.0
    for i in range(layers):
        if total + usage_array[layers - i - 1] >= length:
            return layers - i, total
        total += usage_array[layers - i - 1]
    return 1, sum(usage_array)


def calculate(gcode_data, cut_length=1.1):
    try:
        # Set cut length as the distance between your filament box and the printer.
        # This allows you to bypass having to rewind a spool by rather planning
        # when to cut filament leaving minimal unused when your print completes.
        # Remember that the values in the GCode are   estimates, so set your length
        # accordingly, erring on a side of caution. Lower length here being safer.
        count = 0
        total = 0.0
        filament_used_per_layer = []

        for line in gcode_data.splitlines():
            if layer_change(line):
                found = find_e(line)
                total += found
                filament_used_per_layer.append(total)
                total = 0.0
            found = find_e(line)
            total += found
            count += 1

        stopping_point = layer_to_stop_at(filament_used_per_layer, cut_length * 1000)
        used = round(sum(filament_used_per_layer[0:stopping_point[0]]) / 1000, 2)
        total = round(sum(filament_used_per_layer) / 1000, 2)
        message = 'To plan a cut for a length of %(cut_length)sm, stop at layer '
        message += '%(stopping_point)s to have %(remaining)sm remaining of '
        message += '%(total)sm total. You will have used an estimate of '
        message += '%(used)sm at this point.'
        print(message % {
            'cut_length': cut_length,
            'stopping_point': stopping_point[0],
            'remaining': round(stopping_point[1] / 1000, 2),
            'total': total,
            'used': used,
        })
        message = 'To summarize:\n=============\n'
        message += 'Required excess: \t\t%(cut_length)sm\n'
        message += 'Layer at which to cut: \t%(stopping_point)s of %(layers)s\n\n'
        message += 'Remaining: \t\t\t\t%(remaining)sm\n'
        message += 'Expended: \t\t\t\t%(used)sm\n'
        message += 'Total: \t\t\t\t\t%(total)sm\n'
        print(message % {
            'cut_length': cut_length,
            'stopping_point': stopping_point[0],
            'layers': len(filament_used_per_layer),
            'remaining': round(stopping_point[1] / 1000, 2),
            'total': total,
            'used': used,
        })
        return {
            'cut_length': cut_length,
            'stopping_point': stopping_point[0],
            'layers': len(filament_used_per_layer),
            'remaining': round(stopping_point[1] / 1000, 2),
            'total': total,
            'used': used,
        }
    except Exception as e:
        return {"error": str(e)}
