'''
Generic stages class that inherits equipment and will be inherited by all stages
'''

# Imports
import tipLocatorEquipment # Allows stages to inherit equipment

class stages(tipLocatorEquipment.equipment):
    def __init__(self):
        print('Stages Initialized')
        tipLocatorEquipment.equipment.__init__(self)