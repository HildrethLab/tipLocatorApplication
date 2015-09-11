'''
Generic stages class that inherits equipment and will be inherited by all stages
'''

## Imports
# Built in modules

# Custom modules
import TLEquipment # Allows stages to inherit equipment

# Generic class stages that inherit from equipment
class Stages(TLEquipment.Equipment):
    def __init__(self):
        # print('Stages Initialized')
        TLEquipment.Equipment.__init__(self)