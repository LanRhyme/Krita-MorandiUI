from .qt_compat import *
import configparser
import os

input_path = '/home/lanrhyme/.local/share/krita/color-schemes/Morandi.colors'
output_path = '/home/lanrhyme/.local/share/krita/color-schemes/Noctalia.colors'

config = configparser.ConfigParser()
config.optionxform = str  # Preserve case
config.read(input_path)

# Noctalia RGB mappings
BG = '33,32,28'        # #21201c
BG_ALT = '44,43,38'    # #2c2b26
FG = '243,243,242'     # #f3f3f2
FG_INACTIVE = '159,159,159' # #9f9f9f
HIGHLIGHT = '141,135,104'   # #8d8768

# Update General
if 'General' in config:
    config['General']['ColorScheme'] = 'Noctalia'
    config['General']['Name'] = 'Noctalia'

# Update colors for all sections
sections_to_update = ['Colors:Button', 'Colors:Complementary', 'Colors:Header', 'Colors:Selection', 'Colors:Tooltip', 'Colors:View', 'Colors:Window']

for section in sections_to_update:
    if section in config:
        # Backgrounds
        if section == 'Colors:Selection':
            config[section]['BackgroundNormal'] = HIGHLIGHT
            config[section]['BackgroundAlternate'] = HIGHLIGHT
            config[section]['ForegroundNormal'] = BG
            config[section]['ForegroundActive'] = BG
        else:
            config[section]['BackgroundNormal'] = BG
            config[section]['BackgroundAlternate'] = BG_ALT
            config[section]['ForegroundNormal'] = FG
            config[section]['ForegroundActive'] = HIGHLIGHT
            config[section]['ForegroundInactive'] = FG_INACTIVE
            config[section]['DecorationFocus'] = HIGHLIGHT
            config[section]['DecorationHover'] = HIGHLIGHT

# Update WM
if 'WM' in config:
    config['WM']['activeBackground'] = BG
    config['WM']['activeForeground'] = FG
    config['WM']['inactiveBackground'] = BG_ALT
    config['WM']['inactiveForeground'] = FG_INACTIVE

with open(output_path, 'w') as f:
    config.write(f)

print(f"Successfully generated {output_path}")
