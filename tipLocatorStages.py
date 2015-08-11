'''
Generic stages class that inherits equipment and will be inherited by all stages
'''

## Imports
# Built in modules

# Custom modules
import tipLocatorEquipment # Allows stages to inherit equipment

# Generic class stages that inherit from equipment
class stages(tipLocatorEquipment.equipment):
    def __init__(self):
        print('Stages Initialized')
        tipLocatorEquipment.equipment.__init__(self)