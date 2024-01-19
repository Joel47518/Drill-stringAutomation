import math

rad = math.radians
cos = math.cos
acos = math.acos
sin = math.sin
asin = math.asin
tan = math.tan
atan = math.atan
pi = math.pi


class trajectory:
    """
    A class for building a 2D and 3D build and hold well profile.

    """
    all = []

    def __init__(self, KOP=0.0, inc=0.0, bur=1.0, Target_TVD=0.0, Target_East=0.0, \
                 Target_North=0.0, RTable=0.0, Bearing=90.0, Cumm_Vert=0.0, \
                 Cumm_East=0.0, Cumm_North=0.0, Cord_East=0.0, Cord_North=0.0, \
                 Cord_Vert=0.0, Cumm_MD=0.0, MD=10, init_MD=0.0, I1=0.0, I2=0.0):
        self.MD = MD
        self.init_MD = init_MD
        self.I1 = I1
        self.I2 = I2
        self.KOP = KOP
        self.inc = inc
        self.bur = bur
        self.Target_TVD = Target_TVD
        self.Bearing = Bearing
        self.Cord_East = Cord_East
        self.Cord_North = Cord_North
        self.Cord_Vert = Cord_Vert
        self.Cumm_Vert = Cumm_Vert
        self.Cumm_East = Cumm_East
        self.Cumm_North = Cumm_North
        self.Cumm_MD = self.MD + self.init_MD
        '''NB: The TVD is from the Rotary Table to Target'''
        self.Target_East = Target_East
        self.Target_North = Target_North
        self.RTable = RTable
        self.MD_Build = self.inc / (self.bur / 100)
        self.Rad_Build = (180 / pi) * (self.MD_Build / (self.inc))

        self.TVD_Build = self.Rad_Build * sin(rad(self.inc))
        self.DEP_Build = self.Rad_Build * (1 - cos(rad(self.inc)))
        self.TVD_fTarget = self.Target_TVD - self.RTable - self.KOP - self.TVD_Build
        self.MD_Hold = self.TVD_fTarget / cos(rad(self.inc))
        self.DEP_fTarget = tan(rad(self.inc)) * self.TVD_fTarget
        self.Departure = self.DEP_fTarget + self.DEP_Build
        self.Rig_East = self.Target_East - ((self.Departure * 0.3048) * sin(rad(90)))
        self.Rig_North = self.Target_North
        self.Rig_Vert = self.RTable
        self.Total_MD = self.MD_Hold + self.MD_Build + self.RTable + self.KOP

        trajectory.all.append(self)

    def print(self):
        print("Target_TVD  : ", self.Target_TVD)
        print("Target_East  : ", self.Target_East)
        print("Target_North  : ", self.Target_North)
        print("RTable : ", self.RTable)
        print("Rad_Build : ", self.Rad_Build)
        print("MD_Build  : ", self.MD_Build)
        print("TVD_Build  : ", self.TVD_Build)
        print("DEP_Build  : ", self.DEP_Build)
        print("TVD_fTarget  : ", self.TVD_fTarget)
        print("DEP_fTarget  : ", self.DEP_fTarget)
        print("Departure  : ", self.Departure)
        print("Rig_East : ", self.Rig_East)
        print("Rig_North  : ", self.Rig_North)
        print("Rig_Vert  : ", self.Rig_Vert)
        print("MD_Hold   : ", self.MD_Hold)

    def cordinates(self, MD=10, init_MD=0.0, I1=0.0, I2=0.0, Cumm_Vert=0.0, Cumm_East=0.0, \
                   Cumm_North=0.0, Bearing=90.0, inc=0.0, init_East=0.0, init_North=0.0, \
                   init_Vert=0.0, Cord_East=0.0, Cord_North=0.0, Cord_Vert=0.0):
        self.init_MD = init_MD
        self.MD = MD
        self.I1 = I1
        self.I2 = I2
        self.Cord_East = Cord_East
        self.Cord_North = Cord_North
        self.Cord_Vert = Cord_Vert
        self.Cumm_Vert = Cumm_Vert
        self.Cumm_East = Cumm_East
        self.Cumm_North = Cumm_North
        self.Bearing = Bearing
        self.init_East = init_East
        self.init_North = init_North
        self.init_Vert = init_Vert

        if self.init_MD < self.KOP + self.RTable:
            self.Chg_MD = self.KOP + self.RTable - self.init_MD

            if self.Chg_MD < self.MD:
                self.MD = self.Chg_MD

            self.Cumm_MD = self.MD + self.init_MD

            self.Cord_East = self.init_East
            self.Cord_North = self.init_North
            self.Cord_Vert = self.init_Vert + self.MD

            self.init_MD = self.Cord_Vert
            self.init_East = self.Cord_East
            self.init_North = self.Cord_North
            self.init_Vert = self.Cord_Vert
            # # # self.Cumm_MD


        else:
            if self.KOP + self.RTable <= self.init_MD <= self.KOP + self.RTable + \
                    self.MD_Build:
                self.I2 = self.I1 + self.MD * (self.bur / 100)
                B = rad(acos(cos(rad(self.I1))) * cos(rad(self.I2)) + sin(rad(self.I1)) * \
                        sin(rad(self.I2)) * cos(rad(0)))
                RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
                TVD_Chg = (self.MD / 2) * (cos(rad(self.I1)) + cos(rad(self.I2))) * RF
                self.Cord_Vert = TVD_Chg + self.init_Vert

                East_Current = (self.MD / 2) * sin(rad(self.I1)) * sin(rad(self.Bearing)) + \
                               sin(rad(self.I2)) * sin(rad(self.Bearing)) * RF
                North_Current = (self.MD / 2) * (sin(rad(self.I1)) * cos(rad(self.Bearing)) + \
                                                 sin(rad(self.I2)) * cos(rad(self.Bearing))) * RF
                self.Cord_East = East_Current * 0.3048 + self.init_East  ####
                self.Cord_North = North_Current * 0.3048 + self.init_North

                self.init_MD += self.MD
                self.init_East = self.Cord_East
                self.init_North = self.Cord_North
                self.init_Vert = self.Cord_Vert


            elif self.init_MD <= self.Total_MD:

                self.I2 = self.I1

                B = rad(acos(cos(rad(self.I1))) * cos(rad(self.I2)) + sin(rad(self.I1)) * \
                        sin(rad(self.I2)) * cos(rad(0)))
                RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
                TVD_Chg = (self.MD / 2) * (cos(rad(self.I1)) + cos(rad(self.I2))) * RF
                self.Cord_Vert = TVD_Chg + self.init_Vert

                East_Current = (self.MD / 2) * sin(rad(self.I1)) * sin(rad(self.Bearing)) + \
                               sin(rad(self.I2)) * sin(rad(self.Bearing)) * RF
                North_Current = (self.MD / 2) * (sin(rad(self.I1)) * cos(rad(self.Bearing)) + \
                                                 sin(rad(self.I2)) * cos(rad(self.Bearing))) * RF
                self.Cord_East = East_Current * 0.3048 + self.init_East  ####
                self.Cord_North = North_Current * 0.3048 + self.init_North

                self.init_MD += self.MD
                self.init_East = self.Cord_East
                self.init_North = self.Cord_North
                self.init_Vert = self.Cord_Vert

##                #self.MD = self.Rad_Build*(pi/180)*self.I2
##                self.TVD_Build =self.Rad_Build*sin(rad(self.I2))
##                self.Cumm_MD = self.MD + self.init_MD
##                self.Cumm_Vert = self.Cord_Vert
##                self.init_East = self.Cord_East
##                self.init_North = self.init_North
##
##                #self.I1= self.I2

    def build_hold_drop(self, MD=10, init_MD=0.0, I1=0.0, I2=0.0, Cumm_Vert=0.0, Cumm_East=0.0, \
                   Cumm_North=0.0, Bearing=90.0, inc=0.0, init_East=0.0, init_North=0.0, \
                   init_Vert=0.0, Cord_East=0.0, Cord_North=0.0, Cord_Vert=0.0):
        self.init_MD = init_MD
        self.MD = MD
        self.I1 = I1
        self.I2 = I2
        self.Cord_East = Cord_East
        self.Cord_North = Cord_North
        self.Cord_Vert = Cord_Vert
        self.Cumm_Vert = Cumm_Vert
        self.Cumm_East = Cumm_East
        self.Cumm_North = Cumm_North
        self.Bearing = Bearing
        self.init_East = init_East
        self.init_North = init_North
        self.init_Vert = init_Vert

        if self.init_MD < self.KOP + self.RTable:
            self.Chg_MD = self.KOP + self.RTable - self.init_MD

            if self.Chg_MD < self.MD:
                self.MD = self.Chg_MD

            self.Cumm_MD = self.MD + self.init_MD

            self.Cord_East = self.init_East
            self.Cord_North = self.init_North
            self.Cord_Vert = self.init_Vert + self.MD

            self.init_MD = self.Cord_Vert
            self.init_East = self.Cord_East
            self.init_North = self.Cord_North
            self.init_Vert = self.Cord_Vert
            # # # self.Cumm_MD


        else:
            if self.KOP + self.RTable <= self.init_MD <= self.KOP + self.RTable + \
                    self.MD_Build:
                self.I2 = self.I1 + self.MD * (self.bur / 100)
                B = rad(acos(cos(rad(self.I1))) * cos(rad(self.I2)) + sin(rad(self.I1)) * \
                        sin(rad(self.I2)) * cos(rad(0)))
                RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
                TVD_Chg = (self.MD / 2) * (cos(rad(self.I1)) + cos(rad(self.I2))) * RF
                self.Cord_Vert = TVD_Chg + self.init_Vert

                East_Current = (self.MD / 2) * sin(rad(self.I1)) * sin(rad(self.Bearing)) + \
                               sin(rad(self.I2)) * sin(rad(self.Bearing)) * RF
                North_Current = (self.MD / 2) * (sin(rad(self.I1)) * cos(rad(self.Bearing)) + \
                                                 sin(rad(self.I2)) * cos(rad(self.Bearing))) * RF
                self.Cord_East = East_Current * 0.3048 + self.init_East  ####
                self.Cord_North = North_Current * 0.3048 + self.init_North

                self.init_MD += self.MD
                self.init_East = self.Cord_East
                self.init_North = self.Cord_North
                self.init_Vert = self.Cord_Vert


            elif self.init_MD <= self.Total_MD:

                self.I2 = self.I1

                B = rad(acos(cos(rad(self.I1))) * cos(rad(self.I2)) + sin(rad(self.I1)) * \
                        sin(rad(self.I2)) * cos(rad(0)))
                RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
                TVD_Chg = (self.MD / 2) * (cos(rad(self.I1)) + cos(rad(self.I2))) * RF
                self.Cord_Vert = TVD_Chg + self.init_Vert

                East_Current = (self.MD / 2) * sin(rad(self.I1)) * sin(rad(self.Bearing)) + \
                               sin(rad(self.I2)) * sin(rad(self.Bearing)) * RF
                North_Current = (self.MD / 2) * (sin(rad(self.I1)) * cos(rad(self.Bearing)) + \
                                                 sin(rad(self.I2)) * cos(rad(self.Bearing))) * RF
                self.Cord_East = East_Current * 0.3048 + self.init_East  ####
                self.Cord_North = North_Current * 0.3048 + self.init_North

                self.init_MD += self.MD
                self.init_East = self.Cord_East
                self.init_North = self.Cord_North
                self.init_Vert = self.Cord_Vert

#
# import math
# import matplotlib.pyplot as plt
#
# rad = math.radians
# cos = math.cos
# acos = math.acos
# sin = math.sin
# asin = math.asin
# tan = math.tan
# atan = math.atan
# pi = math.pi
#
# kop = 1500  # 2500
# RTable = 100
# init_MD = 0
# MD = 10
# Target_TVD = 6000  # 10000
# init_East = 0
# init_North = 0
# init_Vert = 0
# North = []
# East = []
# Vert = []
#
# inc = 20
# bur = 1.10  # 1.2
#
# MD_Build = inc / (bur / 100)
# Rad_Build = (180 / pi) * (MD_Build / (inc))
# TVD_Build = Rad_Build * sin(rad(inc))
# TVD_fTarget = Target_TVD - RTable - kop - TVD_Build
# MD_Hold = TVD_fTarget / cos(rad(inc))
# Total_MD = MD_Hold + MD_Build + RTable + kop
#
# I1 = 0
# Bearing = 90
#
# while init_MD < kop + RTable + MD_Build:
#     # Vertical section
#     if init_MD < kop + RTable:
#         # Chg_MD = kop + RTable - init_MD
#         # if Chg_MD < MD:
#         #     MD = Chg_MD
#         Cumm_MD = MD + init_MD
#
#         Cord_East = init_East
#         Cord_North = init_North
#         Cord_Vert = init_Vert + MD
#
#         East.append(Cord_East)
#         North.append(Cord_North)
#         Vert.append(Cord_Vert)
#
#         init_MD = Cord_Vert
#         init_East = Cord_East
#         init_North = Cord_North
#         init_Vert = Cord_Vert
#
#     elif kop + RTable <= init_MD <= kop + RTable + MD_Build:
#         I2 = I1 + MD * (bur / 100)
#         B = rad(acos(cos(rad(I1))) * cos(rad(I2)) + sin(rad(I1)) *
#                 sin(rad(I2)) * cos(rad(0)))
#         RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
#         TVD_Chg = (MD / 2) * (cos(rad(I1)) + cos(rad(I2))) * RF
#         Cord_Vert = TVD_Chg + init_Vert
#
#         East_Current = (MD / 2) * sin(rad(I1)) * sin(rad(Bearing)) + \
#                        sin(rad(I2)) * sin(rad(Bearing)) * RF
#         North_Current = (MD / 2) * (sin(rad(I1)) * cos(rad(Bearing)) +
#                                     sin(rad(I2)) * cos(rad(Bearing))) * RF
#         Cord_East = East_Current * 0.3048 + init_East  ####
#         Cord_North = North_Current * 0.3048 + init_North
#
#         East.append(Cord_East)
#         North.append(Cord_North)
#         Vert.append(Cord_Vert)
#
#         init_MD += MD
#         init_East = Cord_East
#         init_North = Cord_North
#         init_Vert = Cord_Vert
#
#         I1 = I2
#
#     elif init_MD <= Total_MD:
#         I2 = I1  # at the hold section inclination is zero
#         B = rad(acos(cos(rad(I1))) * cos(rad(I2)) + sin(rad(I1)) * \
#                 sin(rad(I2)) * cos(rad(0)))
#         RF = 1 + ((B ** 2) / 12) + ((B ** 4) / 120) + ((17 * (B ** 6)) / 20160)
#         TVD_Chg = (MD / 2) * (cos(rad(I1)) + cos(rad(I2))) * RF
#         Cord_Vert = TVD_Chg + init_Vert
#
#         East_Current = (MD / 2) * sin(rad(I1)) * sin(rad(Bearing)) + \
#                        sin(rad(I2)) * sin(rad(Bearing)) * RF
#         North_Current = (MD / 2) * (sin(rad(I1)) * cos(rad(Bearing)) + \
#                                     sin(rad(I2)) * cos(rad(Bearing))) * RF
#         Cord_East = East_Current * 0.3048 + init_East  ####
#         Cord_North = North_Current * 0.3048 + init_North
#
#         East.append(Cord_East)
#         North.append(Cord_North)
#         Vert.append(Cord_Vert)
#
#         init_MD += MD
#         init_East = Cord_East
#         init_North = Cord_North
#         init_Vert = Cord_Vert
#
# ax = plt.axes(projection='3d')
# ax.invert_zaxis()
# ax.plot3D(East, North, Vert)
# plt.show()
