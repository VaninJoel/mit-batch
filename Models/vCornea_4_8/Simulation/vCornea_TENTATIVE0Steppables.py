#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Simulation version 4.7a1
# 
# ----- ADDITIONS -----
#       Good progress in determining Basal cell homeostasis with STEM cell at limbus
#       TODO connect the Wing cells and analyze the system
# 
#       TODO Plot tissue structure
#       TODO Parameterizing for homeostasis
#                  
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

from cc3d.cpp.PlayerPython import * 
from cc3d import CompuCellSetup
from cc3d.core.PySteppables import *
import numpy as np
import random


# GLOBAL PARAMETERS
RANDOM_SEED = random.seed(17)

#---- Time Scales ---
HOURtoMCS  = 10
DAYtoMCS   = 240
WEEKtoMCS  = 1680
MONTHtoMCS = 7300
YEARtoMCS  = 87600

#---- Spatial Scales ---
UMtoVOXEL  = 2

DEATHCOUNT = 0


class ConstraintInitializerSteppable(SteppableBasePy):

# Static Parameters for simulation initiation

#   CELLS PARMETERS
    #---STEM---
    InitSTEM_LambdaSurface  = 10
    InitSTEM_TargetSurface  = 25
    STEM_HalfMaxValue       = 65
    InitSTEM_LambdaChemo    = 500

    #---BASAL---
    InitBASAL_LambdaSurface = 5
    InitBASAL_TargetSurface = 25
    InitBASAL_LambdaChemo   = 125
    InitBASAL_Division      = 27
    BASAL_HalfMaxValue      = 15
    
    #---WING---
    InitWING_LambdaSurface  = 2
    InitWING_TargetSurface  = 24

    #---SUPERFICIAL---
    DeathTimeScaler         = 1
    DeathVolumeScaler       = 0.1
    InitSUPER_LambdaSurface = 2
    InitSUPER_TargetSurface = 25
    InitSUPER_TargetVolume  = 25

#   PLOTS
    CellCount         = True
    XHypTracker       = False
    SloughTracker     = False
    PressureTracker   = True
    VolumeTracker     = False
    TearSeenByCell    = False
    CenterBiasPlot    = False
    CenterBias        = False
    DivisionTracker   = True


# Fields
    MovementBias = object()
    MovementBiasValue = 1

    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

        if self.PressureTracker:
            self.track_cell_level_scalar_attribute(field_name='Pressure', attribute_name='Pressure')
        if self.VolumeTracker:
            self.track_cell_level_scalar_attribute(field_name='Volume', attribute_name='Volume')
        if self.TearSeenByCell:
            self.track_cell_level_scalar_attribute(field_name='Tear', attribute_name='Tear')
        if self.CenterBias:
            self.track_cell_level_scalar_attribute(field_name='CenterBias', attribute_name='CenterBias')
        if self.DivisionTracker:
            self.track_cell_level_scalar_attribute(field_name='DivisionCount', attribute_name='DivisionCount')


    def start(self):        
          
        # # Creating space for KERATO
        # x_loc = [5, 20, 36, 52, 66, 84]
        # for x in x_loc:
        #     for i in range(1,10):
        # cell = self.cell_field[3, 15, 0]
        # self.delete_cell(cell)         
        #         cell = self.cell_field[x+i, 6, 0]
        #         self.delete_cell(cell)                
        #         cell = self.cell_field[x+i, 7, 0]
        #         self.delete_cell(cell)
        #         cell = self.cell_field[x+i, 8, 0]
        #         self.delete_cell(cell)
    #   Test no cell  
        # for cell in self.cell_list_by_type(self.WING):
        #     self.delete_cell(cell)
        # for cell in self.cell_list_by_type(self.SUPER):
        #     self.delete_cell(cell)
        # for cell in self.cell_list_by_type(self.BASAL):
        #     self.delete_cell(cell)
                
        #     self.cell_field[x+1:x+7, 6:8, 0] = self.new_cell(self.KERATO)

        # cell = self.cell_field[3, 15, 0]
        # self.delete_cell(cell) 
        # self.cell_field[0:3, 12:20, 0] = self.new_cell(self.STEM)
        # for i in range(0, 20):
        #     for j in range(7, 12):
        #         self.cell_field[i, j, 0] = self.new_cell(self.LIMB)

        # for i in range(20, 23):
                           
        #     self.delete_cell(self.cell_field[i, 12, 0])
        #     # self.delete_cell(self.cell_field[i, j, 0])
        #     self.cell_field[i, 12-5, 0] = self.new_cell(self.MEMB)


        # self.delete_cell(self.cell_field[3, 11, 0])
        # self.delete_cell(self.cell_field[3, 10, 0])
        # self.delete_cell(self.cell_field[3, 9, 0])

        # self.delete_cell(self.cell_field[2, 11, 0])
        # self.delete_cell(self.cell_field[2, 10, 0])
        # self.delete_cell(self.cell_field[2, 9, 0])
        # self.delete_cell(self.cell_field[1, 11, 0])
        # self.delete_cell(self.cell_field[1, 10, 0])
        # self.delete_cell(self.cell_field[1, 9, 0])
        # self.delete_cell(self.cell_field[0, 11, 0])
        # self.delete_cell(self.cell_field[0, 10, 0])
        # self.delete_cell(self.cell_field[0, 9, 0])

        # self.cell_field[1, 9, 0] = self.new_cell(self.STEM)

        # self.cell_field[4, 12, 0] = self.new_cell(self.LIMB)
        # self.cell_field[4, 13, 0] = self.new_cell(self.LIMB)
        # self.cell_field[5, 12, 0] = self.new_cell(self.LIMB)
        # self.cell_field[5, 13, 0] = self.new_cell(self.LIMB)
        # self.cell_field[6, 12, 0] = self.new_cell(self.LIMB)
        # self.cell_field[6, 13, 0] = self.new_cell(self.LIMB)
        # self.cell_field[6, 14, 0] = self.new_cell(self.LIMB)
        # self.cell_field[7, 12, 0] = self.new_cell(self.LIMB)

        # self.cell_field[0:200, 0:7, 0] = self.new_cell(self.STROMA)

        # for i in range(20, 33):
        #     j = 12                
        #     self.delete_cell(self.cell_field[i, j, 0])
        #     # self.delete_cell(self.cell_field[i, j, 0])
        #     self.cell_field[i, j-5, 0] = self.new_cell(self.MEMB)

        # for i in range(20, 33):
        #     for j in range(12, 15):                
        #         self.delete_cell(self.cell_field[i, j, 0])
        #         # self.delete_cell(self.cell_field[i, j, 0])
        #         self.cell_field[i, j-5, 0] = self.new_cell(self.MEMB)

        # for i in range(27, 30):
        #     for j in range(14, 15):

        #         self.cell_field[i, j, 0] = self.new_cell(self.MEMB)
        #         self.delete_cell(self.cell_field[i, 9, 0])

                # self.cell_field[i+5, j+1, 0] = self.new_cell(self.MEMB)
                # self.delete_cell(self.cell_field[i+5, 10, 0])

                # self.cell_field[i+5, j+1, 0] = self.new_cell(self.MEMB)
                # self.delete_cell(self.cell_field[i+5, 10, 0])


        # for i in range(27, 30):
        #     for j in range(14, 15):
        #         self.cell_field[i, j, 0] = self.new_cell(self.MEMB)
              



        # self.cell_field[4:13, 12:18, 0] = self.new_cell(self.STEM)
        # self.delete_cell(self.cell_field[12, 15, 0])
        # self.cell_field[12:20, 12:18, 0] = self.new_cell(self.STEM)
        # self.delete_cell(self.cell_field[9, 19, 0])
        # self.delete_cell(self.cell_field[5, 22, 0])
        # self.delete_cell(self.cell_field[9, 22, 0])
        # self.delete_cell(self.cell_field[0, 7, 0])
        # self.cell_field[0, 7, 0] = self.new_cell(self.LIMB)
        # self.delete_cell(self.cell_field[1, 7, 0])
        # self.cell_field[1, 7, 0] = self.new_cell(self.LIMB)
        # self.delete_cell(self.cell_field[2, 7, 0])
        # self.cell_field[2, 7, 0] = self.new_cell(self.LIMB)
        # self.delete_cell(self.cell_field[3, 7, 0])
        # self.cell_field[3, 7, 0] = self.new_cell(self.LIMB)

        # for i in range(0, 21):
        #     self.delete_cell(self.cell_field[1+i, 7, 0])
            # for j in range(7,13):
            #     self.delete_cell(self.cell_field[i, j, 0])
                # self.cell_field[i, j, 0] = self.new_cell(self.LIMB)   
        # print(cellsinthelimbus)  
         
        # BASAL MOVEMENT BIAS
        self.MovementBias =self.get_field_secretor("BASALMVBIAS")

        # STROMA
        for cell in self.cell_list_by_type(self.STROMA):

            cell.targetVolume = 5000
            cell.lambdaVolume = 60.0          
          
        # MEMBANE    
        for cell in self.cell_list_by_type(self.MEMB):
            
            cell.targetVolume = 1
            cell.lambdaVolume = 1000.0
            cell.lambdaSurface = 1.0
            cell.targetSurface = 100.0

        # LIMB    
        for cell in self.cell_list_by_type(self.LIMB):
            
            cell.targetVolume = 1
            cell.lambdaVolume = 1000.0
            cell.lambdaSurface = 1.0
            cell.targetSurface = 100.0

        # KERATO    
        for cell in self.cell_list_by_type(self.KERATO):

            cell.targetVolume = 35
            cell.lambdaVolume = 2.0
            # cell.lambdaSurface = 2.0
            # cell.targetSurface = 35.0

        # STEM
        for cell in self.cell_list_by_type(self.STEM):

            cell.targetVolume = 50
            cell.lambdaVolume = 12.0
            cell.lambdaSurface = self.InitSTEM_LambdaSurface
            cell.targetSurface = self.InitSTEM_TargetSurface
            cell.dict["LambdaChemo"] = self.InitSTEM_LambdaChemo
            ChemotaxisData = self.chemotaxisPlugin.addChemotaxisData(cell, "BASALMVBIAS")
            ChemotaxisData.setLambda(cell.dict["LambdaChemo"])
           
        # BASAL   
        for cell in self.cell_list_by_type(self.BASAL):

            cell.targetVolume = 45
            cell.lambdaVolume = 12.0
            cell.lambdaSurface = self.InitBASAL_LambdaSurface
            cell.targetSurface = self.InitBASAL_TargetSurface

            cell.dict['DivisionCount'] = random.randint(0, self.InitBASAL_Division)
            cell.dict["LambdaChemo"] = self.InitBASAL_LambdaChemo
            ChemotaxisData = self.chemotaxisPlugin.addChemotaxisData(cell, "BASALMVBIAS")            
            ChemotaxisData.setLambda(cell.dict["LambdaChemo"])

        # WING  
        for cell in self.cell_list_by_type(self.WING):

            cell.targetVolume = 25
            cell.lambdaVolume = 12.0
            cell.lambdaSurface = 2.0
            cell.targetSurface = 24.0
            
        # SUPERFICIAL  
        for cell in self.cell_list_by_type(self.SUPER):

            cell.targetVolume = 25
            cell.lambdaVolume = 1.0
            cell.lambdaSurface = self.InitSUPER_LambdaSurface
            cell.targetSurface = self.InitSUPER_TargetSurface
            cell.dict['Slough'] = 0.0
    
        
    def step(self, mcs):
        
        TEAR_FIELD = self.get_field_secretor("TEAR")
        x = 0   

        # for cell in self.cell_list_by_type(self.WING):
        #     self.delete_cell(cell)
        # for cell in self.cell_list_by_type(self.SUPER):
        #     self.delete_cell(cell)


        # ---- CELL PARAMETERS UPDATE ----
        
        # for cell in self.cell_list_by_type(self.TYPENAME_1, self.TYPENAME_2, ...):
          
        
        
        for cell in self.cell_list_by_type(self.BASAL, self.STEM, self.WING, self.SUPER):           
            cell.dict['Pressure'] = abs(cell.pressure)
            cell.dict['Volume'] = cell.volume
            cell.dict['Tear'] = TEAR_FIELD.amountSeenByCell(cell)
            # UPTAKE OF FIELD
            TEAR_FIELD.uptakeInsideCell(cell, 0.8, 0.01)
            cell.dict['TEAR_Uptake'] = TEAR_FIELD.uptakeInsideCellTotalCount(cell, 0.8, 0.01).tot_amount            
       
        # ---- FIELD PARAMETERS UPDATE ----
        for cell in self.cell_list_by_type(self.MEMB): 
            self.MovementBias.secreteOutsideCellAtBoundary(cell, self.MovementBiasValue)
            
 
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

        self.BASAL_HalfMaxValue = ConstraintInitializerSteppable.BASAL_HalfMaxValue
        self.STEM_HalfMaxValue = ConstraintInitializerSteppable.STEM_HalfMaxValue

    def step(self, mcs):              
        
               
        # ---- BASAL ----
        for cell in self.cell_list_by_type(self.BASAL):

            # GROWTH THROUGH TEAR 
        #     # cell.targetVolume += (cell.dict['Tear']**4/(18**4 + cell.dict['Tear']**4)) Hill Promoter Tear 

            # GROWTH CONTACT INHIBITION             
            cell.targetVolume += ((1) * (self.BASAL_HalfMaxValue**4/(self.BASAL_HalfMaxValue**4 + cell.dict['Pressure']**4))) # Hill Inhibitor Pressure        

        # ---- STEM ----
        for cell in self.cell_list_by_type(self.STEM):

            # GROWTH THROUGH TEAR 
        #     # cell.targetVolume += (cell.dict['Tear']**4/(18**4 + cell.dict['Tear']**4)) Hill Promoter Tear 

            # GROWTH CONTACT INHIBITION             
            cell.targetVolume += ((1) * (self.STEM_HalfMaxValue**4/(self.STEM_HalfMaxValue**4 + cell.dict['Pressure']**4))) # Hill Inhibitor Pressure        

class MitosisSteppable(MitosisSteppableBase):
    
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]

        #---BASAL---            
        for cell in self.cell_list_by_type(self.BASAL):
            if cell.volume>50:
                cells_to_divide.append(cell)

        #---STEM---
        for cell in self.cell_list_by_type(self.STEM):
            if cell.volume>75:
                cells_to_divide.append(cell)


        for cell in cells_to_divide:
            # STEM 
            if cell.type == self.STEM:
                self.set_parent_child_position_flag(1)
                # self.divide_cell_orientation_vector_based(cell,1,0,0) # Orientation for Stem division
                self.divide_cell_random_orientation(cell)

            # Basal cell constraints in division    
            else:
                if cell.dict['DivisionCount'] > 0:
                    cell.dict['DivisionCount'] -= 1                 
                    self.divide_cell_random_orientation(cell)
                else:
                    cell.type = self.WING # Differentiation Due to Last Division
                    cell.lambdaSurface = ConstraintInitializerSteppable.InitWING_LambdaSurface
                    cell.targetSurface = ConstraintInitializerSteppable.InitWING_TargetSurface                     
                    self.divide_cell_random_orientation(cell)    
                
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        
        self.parent_cell.targetVolume /= 2.0            
        self.clone_parent_2_child()            

class DeathSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self, frequency)

        # WOUND EVENT 
        self.injuryType = ''    # A for Abrasion
        self.injury     = False      
        self.injuryTime = 500   # MCS 

        # INJURY AREA
        self.x_center = 160 # 160 Abrasion
        self.y_center = 45  # 45  Abrasion
        self.radius   = 15  # 15  Abrasion

        # DEATH SCALER 
        self.deathTimeScaler    = ConstraintInitializerSteppable.DeathTimeScaler
        self.deathVolumeScalar  = ConstraintInitializerSteppable.DeathVolumeScaler                
        self.sloughScalar       = 50 
       
    
    def step(self, mcs):
        global DEATHCOUNT
        # print('Cell count ' ,len(self.cell_list), "at ", mcs)     
     
        # --- Basal cell death rate ---
        if self.injury:

            # if (mcs > 10 and mcs < 300): # sustained injury         
            if (mcs == self.injuryTime): 

                # ---- PRODUCTION OF TEAR ----
                # self.get_xml_element('Tear_GlbDiff').cdata = 6 # GlobalDiffusion change

                cells_to_kill = set()
                for i in np.arange(-self.radius,  self.radius, 1.0):
                    y_position = self.y_center + i
                    if not (self.y_center + i < 0 or self.y_center + i> self.dim.y):
                        for j in np.arange(-np.sqrt(self.radius**2-i**2), np.sqrt(self.radius**2-i**2),1.0):
                            x_position = self.x_center + j
                            if not (self.x_center + j < 0 or self.x_center + j> self.dim.x):
                                cell = self.cell_field[x_position, y_position, 0]
                                if cell:
                                    cells_to_kill.add(cell.id)
                # print(cells_to_kill)
                # print("###############\n", "Cell that will die on injury", len(cells_to_kill))

                if self.injuryType == 'A':
                    # --- ABRASION ---    
                    for cellid in cells_to_kill:
                        cell = self.fetch_cell_by_id(cellid)                
                        self.delete_cell(cell)
                else:
                    # --- CHEMICAL ---    
                    for cellid in cells_to_kill:
                        cell = self.fetch_cell_by_id(cellid)                
                        cell.targetVolume = 0
                        cell.lambdaVolume = 1000
                        
            # ---- PRODUCTION OF TEAR ----           
            # if (mcs > (self.injuryTime + HOURtoMCS * 1)):
            #     self.get_xml_element('Tear_GlbDiff').cdata = 1                
                

        # --- Constant Cell Death Rate ---          
        deathsum = 0
        # CONSTANT DEATH RATE (Cell type dependent)            
        for cell in self.cell_list_by_type(self.SUPER):          
            # print('volume',cell.volume)
            NEIGHBOR_DICT = self.get_cell_neighbor_data_list(cell).neighbor_count_by_type()  # Checking Neighbors                        
            
            if (self.MEDIUM in NEIGHBOR_DICT.keys()) : # Only cells at the edge has basal death for now            
                # cell.targetVolume -= (1/(WEEKtoMCS)) * 25 * (random.random()) # adding a stochastic death rate
                cell.targetVolume -= (1/(WEEKtoMCS)) * self.sloughScalar 
                cell.lambdaVolume = 100                            

            if cell.volume < 15: # Minimum Cell Size Before Slough | if no slogh cell will disapear in 672 MCS ~3 days(2.8)
                
                cell.dict['Slough'] = (1 - np.exp(1/(-(HOURtoMCS*self.deathTimeScaler)*(cell.volume*self.deathVolumeScalar))))
              
                if (random.random() < cell.dict['Slough']):
                    deathsum += 1
                    self.delete_cell(cell)
        DEATHCOUNT = deathsum
        # PlotSteppable.hack(deathsum)  

    def getDeath(self):
        return self.death

class DifferentiationSteppable(SteppableBasePy):
    def __init__(self, frequency=1):      
        SteppableBasePy.__init__(self, frequency)      
        

    def start(self):
       pass
   
    def step(self, mcs): 

        if mcs > 10:
            # SUPER CELL
            for cell in self.cell_list_by_type(self.SUPER):
                # PARAMETERS
                NEIGHBOR_DICT = self.get_cell_neighbor_data_list(cell).neighbor_count_by_type()
                        
            # WING CELL
            for cell in self.cell_list_by_type(self.WING):
                # PARAMETERS
                NEIGHBOR_DICT = self.get_cell_neighbor_data_list(cell).neighbor_count_by_type()
                            
                # DIFFERENTIATION RULES
                if (self.MEDIUM in NEIGHBOR_DICT.keys()) and (self.WING in NEIGHBOR_DICT.keys()):
                    cell.type = self.SUPER
                    self.initializeDifferentiatedCell(cell)
                    # Tear based Differention
                # elif (cell.dict['Tear']> 1) and (self.SUPER in NEIGHBOR_DICT.keys()): # Amount seen by cell = cell.dict['Tear']
                #     cell.type = self.SUPER
                # elif (self.TEAR in NEIGHBOR_DICT.keys()) and (self.WING in NEIGHBOR_DICT.keys()): # Old version
                    # cell.type = self.SUPER
                    
            # BASAL CELL   
            for cell in self.cell_list_by_type(self.BASAL):
                # PARAMETERS
                NEIGHBOR_DICT = self.get_cell_neighbor_data_list(cell).neighbor_count_by_type()
                # GROWTH RULES
                
                # DIFFERENTIATION RULES
                if not(self.MEMB in NEIGHBOR_DICT.keys()):
                    cell.type = self.WING
                    self.initializeDifferentiatedCell(cell)  
                            
            # STEM CELL
            for cell in self.cell_list_by_type(self.STEM): 
                
                # PARAMETERS
                NEIGHBOR_DICT = self.get_cell_neighbor_data_list(cell).neighbor_count_by_type()                        
                # GROWTH RULES
                # if (self.TAC in NEIGHBOR_DICT.keys()):
                #     cell.targetVolume = 30
                # DIFFERENTIATION RULES
                if (self.LIMB not in NEIGHBOR_DICT.keys()):
                    cell.type = self.BASAL                
                    self.initializeDifferentiatedCell(cell)
                    

    def initializeDifferentiatedCell(self, cell):   
        
        # --- BASAL ---
        if cell.type == self.BASAL:
            cell.lambdaSurface = ConstraintInitializerSteppable.InitBASAL_LambdaSurface
            cell.targetSurface = ConstraintInitializerSteppable.InitBASAL_TargetSurface
            cell.dict["LambdaChemo"] = ConstraintInitializerSteppable.InitBASAL_LambdaChemo
            cell.dict['DivisionCount'] = ConstraintInitializerSteppable.InitBASAL_Division
            ChemotaxisData = self.chemotaxisPlugin.addChemotaxisData(cell, "BASALMVBIAS")            
            ChemotaxisData.setLambda(cell.dict["LambdaChemo"])

        # --- STEM ---
        elif cell.type == self.STEM:
            cell.lambdaSurface = ConstraintInitializerSteppable.InitSTEM_LambdaSurface
            cell.targetSurface = ConstraintInitializerSteppable.InitSTEM_TargetSurface
            cell.dict["LambdaChemo"] = ConstraintInitializerSteppable.InitSTEM_LambdaChemo
            ChemotaxisData = self.chemotaxisPlugin.addChemotaxisData(cell, "BASALMVBIAS")            
            ChemotaxisData.setLambda(cell.dict["LambdaChemo"])

        # --- WING ---
        elif cell.type == self.WING:
            cell.lambdaSurface = ConstraintInitializerSteppable.InitWING_LambdaSurface
            cell.targetSurface = ConstraintInitializerSteppable.InitWING_TargetSurface
            cell.dict["LambdaChemo"] = 0

        # --- SUPER ---
        elif cell.type == self.SUPER:
            cell.lambdaSurface = ConstraintInitializerSteppable.InitSUPER_LambdaSurface
            cell.targetSurface = ConstraintInitializerSteppable.InitSUPER_TargetSurface
            cell.dict["LambdaChemo"] = 0
        
        # print(ConstraintInitializerSteppable.InitBASAL_LambdaSurface)

        # if (cell.type == self.STEM):
        #     ConstraintInitializerSteppable.InitSTEM_LambdaSurface


        
class PlotSteppable(SteppableBasePy):

    def __init__(self, frequency=1):      
        SteppableBasePy.__init__(self, frequency) 

        self.cellCount = ConstraintInitializerSteppable.CellCount
        self.xhypTracker = ConstraintInitializerSteppable.XHypTracker
        self.sloughTracker = ConstraintInitializerSteppable.SloughTracker
        self.centerBiasPlot = ConstraintInitializerSteppable.CenterBiasPlot

    def start(self):

        # ---- Cell Count Plot ----
        if self.cellCount:
        
            self.plot_cell_count = self.add_new_plot_window(title='Cell Count by Type',
                                                            x_axis_title='Time (Hours)',
                                                            y_axis_title='Number of Cells',
                                                            x_scale_type='linear', y_scale_type='linear',
                                                            grid=True, config_options={'legend':True})

            self.plot_cell_count.add_plot("Superficial", style='Lines', color='cyan')
            self.plot_cell_count.add_plot("Wing", style='Lines', color='blue')
            self.plot_cell_count.add_plot("Basal", style='Lines', color='pink')
            self.plot_cell_count.add_plot("Stem", style='Lines', color='red')

        # ---- Slough Tracker Plot ----
        if self.sloughTracker:
            
            self.plot_slough_tracker = self.add_new_plot_window(title='Slough Tracker Tracker',
                                                            x_axis_title='Time (Hour)',
                                                            y_axis_title='Volume(Cyan and Red) / # Cells(Green)',
                                                            x_scale_type='linear', y_scale_type='linear',
                                                            grid=True, config_options={'legend':True})

            self.plot_slough_tracker.add_plot("Wing", style='Dots', color='blue')
            self.plot_slough_tracker.add_plot("Individual Volume", style='Dots', color='Cyan')
            self.plot_slough_tracker.add_plot("Average Vol", style='lines', color='red')
            self.plot_slough_tracker.add_plot("Slough Count", style='lines', color='green')
        
        # ---- Chemochine Center Movement Bias Plot ----
        if self.centerBiasPlot:
            
            self.plot_center_bias = self.add_new_plot_window(title='Chemochine Center Movement Bias',
                                                            x_axis_title='Time (Hour)',
                                                            y_axis_title='Strenth of the Signal',
                                                            x_scale_type='linear', y_scale_type='linear',
                                                            grid=True, config_options={'legend':True})

            self.plot_center_bias.add_plot("Wing", style='Dots', color='blue')
            self.plot_center_bias.add_plot("Individual Volume", style='Dots', color='Cyan')
            self.plot_center_bias.add_plot("Average Vol", style='lines', color='red')
            self.plot_center_bias.add_plot("Slough Count", style='lines', color='green')


    def step(self, mcs):

        # ---- Cell Count Plot ----
        if self.cellCount:
            self.plot_cell_count.add_data_point("Superficial", mcs/HOURtoMCS, len(self.cell_list_by_type(self.SUPER)))
            self.plot_cell_count.add_data_point("Wing", mcs/HOURtoMCS, len(self.cell_list_by_type(self.WING)))
            self.plot_cell_count.add_data_point("Basal", mcs/HOURtoMCS, len(self.cell_list_by_type(self.BASAL)))
            self.plot_cell_count.add_data_point("Stem", mcs/HOURtoMCS, len(self.cell_list_by_type(self.STEM)))


        # ---- Slough Tracker Plot ----
        if self.sloughTracker:
            if mcs%10 == 0:

                listVol = []
               
                for cell in self.cell_list_by_type(self.SUPER):
                    listVol.append(cell.volume)

                SumVol = sum(listVol)

                listMinVol = [i for i in listVol if i <= 15]

                for i in listMinVol:
                    self.plot_slough_tracker.add_data_point("Individual Volume", mcs/HOURtoMCS, i)
                  
                AvrVol = SumVol/len(self.cell_list_by_type(self.SUPER))
               
                self.plot_slough_tracker.add_data_point("Average Vol", mcs/HOURtoMCS, AvrVol)
            self.plot_slough_tracker.add_data_point("Slough Count", mcs/HOURtoMCS, DEATHCOUNT)

      

    
    