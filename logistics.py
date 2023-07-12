class Costs:
    
    def __init__(self):
        self.pricelist = {
            "x_rays": (8.0, 10.0),
            "ct_scan": (40.0, 75.0),
            "cytologic": (15.0, 20),
            "bronchoscopesis": (15.0, 20),
            "fna": (90.0, 110.0),
            "pet_scan": (750.0, 800.0),
            "fna_and_pet_scan": (840.0, 910.0),
            "mri_brain": (120.0, 150.0),
            "ro_bones": (8.0, 10.0),
            "scintigraphy": (240.0, 260.0),
        }
        
        self.delay = {
            "x_rays": (2, 4),
            "ct_scan": (7, 45),
            "cytologic": (3, 4),
            "bronchoscopesis": (2, 4),
            "fna": (5, 30),
            "pet_scan": (5, 60),
            "fna_and_pet_scan": (10, 90),
            "mri_brain": (5, 15),
            "ro_bones": (2, 4),
            "scintigraphy": (3, 7),
        }
