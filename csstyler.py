import sys
import re


def read_css_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except:
        raise IOError('The file does not exist')

def write_css_file(filename, source):
    try:
        with open(filename, 'w+') as file:
            file.write(source)
    except:
        raise IOError('Error writing the file')

def hexa_to_rgba(source):
    rgx = re.compile(r'#[\da-fA-F]{8}')
    hits = re.findall(rgx, source)
    for hit in hits:
        red = int(hit[1:3], 16)
        green = int(hit[3:5], 16)
        blue = int(hit[5:7], 16)
        alpha = round(int(hit[7:], 16) / 255, 3)
        rgba = 'rgba({}, {}, {}, {})'.format(red, green, blue, alpha)
        source = source.replace(hit, rgba)
    return source

def rgba_to_hexa(source):
    rgx = re.compile(r'rgba\( *(?:\d{1,3} *, *){3}(?:0.\d{0,17}|0|1|1\.0) *\)')
    hits = re.findall(rgx, source)
    for hit in hits:
        truncated = hit.replace('rgba(', '').replace(')', '')
        divided = truncated.split(',')
        hred = format(int(divided[0]), 'x').zfill(2)
        hgreen = format(int(divided[1]), 'x').zfill(2)
        hblue = format(int(divided[2]), 'x').zfill(2)
        halpha = format(int(float(divided[3]) * 255), 'x').zfill(2)
        hrgba = '#' + hred + hgreen + hblue + halpha
        source = source.replace(hit, hrgba)            
    return source

def hex_to_rgb(source):
    rgx = re.compile(r'#[\da-fA-F]{6}')
    hits = re.findall(rgx, source)
    for hit in hits:
        red = int(hit[1:3], 16)
        green = int(hit[3:5], 16)
        blue = int(hit[5:], 16)
        rgb = 'rgb({}, {}, {})'.format(red, green, blue)
        source = source.replace(hit, rgb)
    return source

def rgb_to_hex(source):
    rgx = re.compile(r'rgb\( *(?:\d{1,3} *, *){2}(?:\d{1,3}) *\)')
    hits = re.findall(rgx, source)
    for hit in hits:
        truncated = hit.replace('rgb(', '').replace(')', '')
        divided = truncated.split(',')
        hred = format(int(divided[0]), 'x').zfill(2)
        hgreen = format(int(divided[1]), 'x').zfill(2)
        hblue = format(int(divided[2]), 'x').zfill(2)
        hrgb = '#' + hred + hgreen + hblue
        source = source.replace(hit, hrgb)            
    return source


def main():
    print(len(sys.argv) )
    if (len(sys.argv) < 2):
        raise IOError('No input file specified')
        sys.exit()
    if (not sys.argv[1].lower().endswith('.css')):
        raise IOError('Invalid input file')
        sys.exit()
    if (len(sys.argv) == 2):
        raise IOError('No styling option specified')
        sys.exit()
    if (len(sys.argv) == 3 and sys.argv[2].lower().endswith('.css')):
        raise IOError('No styling option specified')
        sys.exit()
    separate_output = True
    if (len(sys.argv) > 2 and not sys.argv[2].lower().endswith('.css')):
        separate_output = False
    source = read_css_file(sys.argv[1])
    options = sys.argv[3:] if separate_output else sys.argv[2:]
    if ('rgba-to-hexa' in options):
        source = rgba_to_hexa(source)
    elif ('hexa-to-rgba' in options):
        source = hexa_to_rgba(source)
    if ('rgb-to-hex' in options):
        source = rgb_to_hex(source)
    elif ('hex-to-rgb' in options):
        source = hex_to_rgb(source)
    filename = sys.argv[2] if separate_output else sys.argv[1]
    write_css_file(filename, source)

if __name__ == '__main__':
    main()

