
import  sys
from    PyQt5.uic           import loadUi
from    PyQt5.QtWidgets     import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QLCDNumber, QStackedWidget, QLineEdit, QMessageBox, QMainWindow 
from    PyQt5.QtGui         import QDoubleValidator, QValidator

import  re
from    ctypes              import c_int, c_char_p, byref, sizeof, c_uint16, c_int32, c_byte
from    ctypes              import c_void_p
from    datetime            import datetime
import  logging
import  struct
from    time                import sleep

import  snap7
from    snap7.util          import *
import  snap7
from    snap7.types         import S7Object, buffer_type, buffer_size, BlocksList
from    snap7.types         import TS7BlockInfo, param_types, cpu_statuses
from    snap7.common        import check_error, load_library, ipv4
from    snap7.exceptions    import Snap7Exception

from    sympy               import symbols, cos, sin, pi, simplify, pprint, tan, expand_trig, sqrt, trigsimp, atan2
from    sympy.matrices      import Matrix

import  numpy as np

import  math


class Window1(QWidget):         # Chế độ điều khiển khớp


    def __init__(self):

        super().__init__()
        loadUi('Window1.ui', self)
                
        self.q_input = [0, 0, 0, 0, 0, 0]
        self.dq_input = [0, 0, 0, 0, 0, 0]     
        self.lineEditQ = [self.lineEditQ1, self.lineEditQ2, self.lineEditQ3, self.lineEditQ4, self.lineEditQ5, self.lineEditQ6]
        self.lineEditdQ = [self.lineEditdQ1, self.lineEditdQ2, self.lineEditdQ3, self.lineEditdQ4, self.lineEditdQ5, self.lineEditdQ6]

        self.lineEditValidator = QDoubleValidator(-1000.000, 1000.000, 3)
        self.lineEditQ1.setValidator(self.lineEditValidator)
        self.lineEditQ2.setValidator(self.lineEditValidator)
        self.lineEditQ3.setValidator(self.lineEditValidator)
        self.lineEditQ4.setValidator(self.lineEditValidator)
        self.lineEditQ5.setValidator(self.lineEditValidator)
        self.lineEditQ6.setValidator(self.lineEditValidator)
        self.lineEditdQ1.setValidator(self.lineEditValidator)
        self.lineEditdQ2.setValidator(self.lineEditValidator)
        self.lineEditdQ3.setValidator(self.lineEditValidator)
        self.lineEditdQ4.setValidator(self.lineEditValidator)
        self.lineEditdQ5.setValidator(self.lineEditValidator)
        self.lineEditdQ6.setValidator(self.lineEditValidator)
        
        self.lineEditQ1.editingFinished.connect(lambda: self.StringtoFloatQ(0))
        self.lineEditQ2.editingFinished.connect(lambda: self.StringtoFloatQ(1))
        self.lineEditQ3.editingFinished.connect(lambda: self.StringtoFloatQ(2))
        self.lineEditQ4.editingFinished.connect(lambda: self.StringtoFloatQ(3))
        self.lineEditQ5.editingFinished.connect(lambda: self.StringtoFloatQ(4))
        self.lineEditQ6.editingFinished.connect(lambda: self.StringtoFloatQ(5))
        self.lineEditdQ1.editingFinished.connect(lambda: self.StringtoFloatdQ(0))
        self.lineEditdQ2.editingFinished.connect(lambda: self.StringtoFloatdQ(1))
        self.lineEditdQ3.editingFinished.connect(lambda: self.StringtoFloatdQ(2))
        self.lineEditdQ4.editingFinished.connect(lambda: self.StringtoFloatdQ(3))
        self.lineEditdQ5.editingFinished.connect(lambda: self.StringtoFloatdQ(4))
        self.lineEditdQ6.editingFinished.connect(lambda: self.StringtoFloatdQ(5))

        self.BackButton.clicked.connect(self.PreviousPage)
        self.ExecuteButton.clicked.connect(self.Execute)


    def PreviousPage(self):
        stackedWidget.setCurrentIndex(0)

                
    def StringtoFloatQ(self,i):   
        q = self.lineEditQ[i].text()
        if q != '':
            q = q.replace(',','.')
            q = float(q)
            self.q_input[i] = q
            #print(self.q_input,type(self.q_input))

    
    def StringtoFloatdQ(self,i):   
        dq = self.lineEditdQ[i].text()
        if dq != '':
            dq = dq.replace(',','.')
            dq = float(dq)
            self.dq_input[i] = dq
            #print(self.dq_input,type(self.dq_input))

    def Execute(self):
        print(self.q_input)
        print(self.dq_input)


        logger = logging.getLogger(__name__)

        # Connect PLC 1

        IP1 = '192.168.0.10'
        RACK = 0
        SLOT = 1
        DB_NUMBER_1 = 100
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        print(plc1.get_cpu_state())

        # Connect PLC 2

        IP2 = '192.168.0.1'
        RACK = 0
        SLOT = 1
        DB_NUMBER_2 = 150
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        print(plc2.get_cpu_state())

        # Write Ouput Servo (q)

        def WriteDBPLC(plc,db_number,offset,number): 
            plc.db_write(db_number, offset, bytearray(struct.pack(">f", number)))

        def ReadDBPLC(plc,db_number,offset):
            data = plc.db_read(db_number,offset,4)
            data = struct.unpack('>f',data)
            print("Value = {}".format(data))
            return data

        WriteDBPLC(plc1,DB_NUMBER_1,0,self.q_input[0]*1250/9)
        WriteDBPLC(plc1,DB_NUMBER_1,4,-self.q_input[1]*1100/9)
        WriteDBPLC(plc1,DB_NUMBER_1,8,self.q_input[2]*400/3)
        WriteDBPLC(plc1,DB_NUMBER_1,12,self.dq_input[0])
        WriteDBPLC(plc1,DB_NUMBER_1,16,self.dq_input[1])
        WriteDBPLC(plc1,DB_NUMBER_1,20,self.dq_input[2])
        WriteDBPLC(plc1,DB_NUMBER_1,24,1)

        WriteDBPLC(plc2,DB_NUMBER_2,0,-self.q_input[3]*710/9)
        WriteDBPLC(plc2,DB_NUMBER_2,4,self.q_input[4]*725/9)
        WriteDBPLC(plc2,DB_NUMBER_2,8,self.q_input[5]*475/9)
        WriteDBPLC(plc2,DB_NUMBER_2,12,self.dq_input[3])
        WriteDBPLC(plc2,DB_NUMBER_2,16,self.dq_input[4])
        WriteDBPLC(plc2,DB_NUMBER_2,20,self.dq_input[5])
        WriteDBPLC(plc2,DB_NUMBER_2,24,1)

        ReadDBPLC(plc1,DB_NUMBER_1,0)
        ReadDBPLC(plc1,DB_NUMBER_1,4)
        ReadDBPLC(plc1,DB_NUMBER_1,8)
        ReadDBPLC(plc1,DB_NUMBER_1,12)
        ReadDBPLC(plc1,DB_NUMBER_1,16)
        ReadDBPLC(plc1,DB_NUMBER_1,20)

        ReadDBPLC(plc2,DB_NUMBER_2,0)
        ReadDBPLC(plc2,DB_NUMBER_2,4)
        ReadDBPLC(plc2,DB_NUMBER_2,8)
        ReadDBPLC(plc2,DB_NUMBER_2,12)
        ReadDBPLC(plc2,DB_NUMBER_2,20)




class Window2(QWidget):         # Chế độ điều khiển theo Bài toán Động học thuận


    def __init__(self):

        super().__init__()
        loadUi('Window2.ui', self)

        self.q_input = [0, 0, 0, 0, 0, 0]
        self.p_output = [0, 0, 0, 0, 0, 0]
        self.lineEditQ = [self.lineEditQ1, self.lineEditQ2, self.lineEditQ3, self.lineEditQ4, self.lineEditQ5, self.lineEditQ6]
        
        self.lineEditValidator = QDoubleValidator(-1000.000, 1000.000, 3)
        self.lineEditQ1.setValidator(self.lineEditValidator)
        self.lineEditQ2.setValidator(self.lineEditValidator)
        self.lineEditQ3.setValidator(self.lineEditValidator)
        self.lineEditQ4.setValidator(self.lineEditValidator)
        self.lineEditQ5.setValidator(self.lineEditValidator)
        self.lineEditQ6.setValidator(self.lineEditValidator)
        
        self.lineEditQ1.editingFinished.connect(lambda: self.StringtoFloat(0))
        self.lineEditQ2.editingFinished.connect(lambda: self.StringtoFloat(1))
        self.lineEditQ3.editingFinished.connect(lambda: self.StringtoFloat(2))
        self.lineEditQ4.editingFinished.connect(lambda: self.StringtoFloat(3))
        self.lineEditQ5.editingFinished.connect(lambda: self.StringtoFloat(4))
        self.lineEditQ6.editingFinished.connect(lambda: self.StringtoFloat(5))
        
        self.BackButton.clicked.connect(self.PreviousPage)
        self.ExecuteButton.clicked.connect(self.Execute)


    def PreviousPage(self):
        stackedWidget.setCurrentIndex(0)


    def StringtoFloat(self,i):   
        q = self.lineEditQ[i].text()
        if q != '':
            q = q.replace(',','.')
            q = float(q)
            self.q_input[i] = q * math.pi/180
            #print(self.q_input,type(self.q_input))

        
    def Execute(self):
        print(self.q_input)

        def DH_Matrix(theta, alpha, a, d):     


            A = np.array([[math.cos(theta),     -math.cos(alpha)*math.sin(theta),     math.sin(alpha)*math.sin(theta),      a*math.cos(theta)    ],
                          [math.sin(theta),     math.cos(alpha)*math.cos(theta),      -math.sin(alpha)*math.cos(theta),     a*math.sin(theta)    ],
                          [0              ,     math.sin(alpha),                      math.cos(alpha),                      d                    ],
                          [0              ,     0,                                    0,                                    1                    ]])

            #A = Matrix([[cos(theta),    -cos(alpha)*sin(theta),     sin(alpha)*sin(theta),      a*cos(theta)    ],
            #            [sin(theta),    cos(alpha)*cos(theta),      -sin(alpha)*cos(theta),     a*sin(theta)    ],
            #            [0         ,    sin(alpha),                 cos(alpha),                 d               ],
            #            [0         ,    0,                          0,                          1               ]])
  
            #A = simplify(A)

            return A

        def Forward_Kinematic(q1,q2,q3,q4,q5,q6):


            pi = math.pi
            alpha1, a1, d1 =    pi/2   ,   0.140   ,   0.405
            alpha2, a2, d2 =    0      ,   0.500   ,   0.000
            alpha3, a3, d3 =    pi/2   ,   0.105   ,   0.000
            alpha4, a4, d4 =    -pi/2  ,   0.000   ,   0.700
            alpha5, a5, d5 =    pi/2   ,   0.000   ,   0.000
            alpha6, a6, d6 =    0      ,   0.000   ,   0.075

            A01 = DH_Matrix(q1, alpha1, a1, d1)             
            A12 = DH_Matrix(q2, alpha2, a2, d2)
            A23 = DH_Matrix(q3, alpha3, a3, d3)
            A34 = DH_Matrix(q4, alpha4, a4, d4)
            A45 = DH_Matrix(q5, alpha5, a5, d5)
            A56 = DH_Matrix(q6, alpha6, a6, d6)
            A02 = np.dot(A01,A12)
            A03 = np.dot(A02,A23)
            A04 = np.dot(A03,A34)
            A05 = np.dot(A04,A45)
            A06 = np.dot(A05,A56)
            # Cu phap nhan ma tran trong sympy : 
            # A02 = A01*A12
            # A03 = A02*A23
            # A04 = A03*A34
            # A05 = A04*A45
            # A06 = A05*A56

            X = round(float(A06[0,3]),3)
            Y = round(float(A06[1,3]),3)
            Z = round(float(A06[2,3]),3)

            r13 = float(A06[0,2])
            r23 = float(A06[1,2])
            r33 = float(A06[2,2])
            r12 = float(A06[0,1])
            r11 = float(A06[0,0])
            beta    = round(math.asin(r13) * 180/math.pi ,3)
            alpha   = round(math.atan2(-r23,r33) * 180/math.pi ,3)
            gamma   = round(math.atan2(-r12,r11) * 180/math.pi ,3)

            P = np.array([X, Y, Z, alpha, beta, gamma])
            #P = np.reshape(P,(6,1))

            return P

        self.p_output = Forward_Kinematic(self.q_input[0],self.q_input[1],self.q_input[2],self.q_input[3],self.q_input[4],self.q_input[5])
        print(self.p_output)
        self.lcdNumberX.display(self.p_output[0])
        self.lcdNumberY.display(self.p_output[1])
        self.lcdNumberZ.display(self.p_output[2])
        self.lcdNumberAlpha.display(self.p_output[3])
        self.lcdNumberBeta.display(self.p_output[4])
        self.lcdNumberGamma.display(self.p_output[5])




        logger = logging.getLogger(__name__)

        # Connect PLC 1

        IP1 = '192.168.0.10'
        RACK = 0
        SLOT = 1
        DB_NUMBER_1 = 100
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        print(plc1.get_cpu_state())

        # Connect PLC 2

        IP2 = '192.168.0.1'
        RACK = 0
        SLOT = 1
        DB_NUMBER_2 = 150
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        print(plc2.get_cpu_state())

        # Write Ouput Servo (q)

        def WriteDBPLC(plc,db_number,offset,number):
            plc.db_write(db_number, offset, bytearray(struct.pack(">f", number)))

        def ReadDBPLC(plc,db_number,offset):
            data = plc.db_read(db_number,offset,4)
            data = struct.unpack('>f',data)
            print("Value = {}".format(data))
            return data

        WriteDBPLC(plc1,DB_NUMBER_1,0,self.q_input[0]*1250/9)
        WriteDBPLC(plc1,DB_NUMBER_1,4,self.q_input[1]*1100/9)
        WriteDBPLC(plc1,DB_NUMBER_1,8,self.q_input[2]*400/3)
        WriteDBPLC(plc1,DB_NUMBER_1,12,1000)
        WriteDBPLC(plc1,DB_NUMBER_1,16,1000)
        WriteDBPLC(plc1,DB_NUMBER_1,20,1000)

        WriteDBPLC(plc2,DB_NUMBER_2,0,self.q_input[3]*710/9)
        WriteDBPLC(plc2,DB_NUMBER_2,4,self.q_input[4]*725/9)
        WriteDBPLC(plc2,DB_NUMBER_2,8,self.q_input[5]*475/9)
        WriteDBPLC(plc2,DB_NUMBER_2,12,2000)
        WriteDBPLC(plc2,DB_NUMBER_2,16,2000)
        WriteDBPLC(plc2,DB_NUMBER_2,20,2000)

        ReadDBPLC(plc1,DB_NUMBER_1,0)
        ReadDBPLC(plc1,DB_NUMBER_1,4)
        ReadDBPLC(plc1,DB_NUMBER_1,8)
        ReadDBPLC(plc1,DB_NUMBER_1,12)
        ReadDBPLC(plc1,DB_NUMBER_1,16)
        ReadDBPLC(plc1,DB_NUMBER_1,20)

        ReadDBPLC(plc2,DB_NUMBER_2,0)
        ReadDBPLC(plc2,DB_NUMBER_2,4)
        ReadDBPLC(plc2,DB_NUMBER_2,8)
        ReadDBPLC(plc2,DB_NUMBER_2,12)
        ReadDBPLC(plc2,DB_NUMBER_2,20)



class Window3(QWidget):         # Chế độ điều khiển theo Bài toán động học ngược


    def __init__(self):

        super().__init__()
        loadUi('Window3.ui', self)

        self.p_input = [0, 0, 0, 0, 0, 0]
        self.q_output = [0, 0, 0, 0, 0, 0]
        self.lineEditP = [self.lineEditX, self.lineEditY, self.lineEditZ, self.lineEditAlpha, self.lineEditBeta, self.lineEditGamma]
        
        self.lineEditValidator = QDoubleValidator(-1000.000, 1000.000, 3)
        self.lineEditX.setValidator(self.lineEditValidator)
        self.lineEditY.setValidator(self.lineEditValidator)
        self.lineEditZ.setValidator(self.lineEditValidator)
        self.lineEditAlpha.setValidator(self.lineEditValidator)
        self.lineEditBeta.setValidator(self.lineEditValidator)
        self.lineEditGamma.setValidator(self.lineEditValidator)
        
        self.lineEditX.editingFinished.connect(lambda: self.StringtoFloat(0))
        self.lineEditY.editingFinished.connect(lambda: self.StringtoFloat(1))
        self.lineEditZ.editingFinished.connect(lambda: self.StringtoFloat(2))
        self.lineEditAlpha.editingFinished.connect(lambda: self.StringtoFloat(3))
        self.lineEditBeta.editingFinished.connect(lambda: self.StringtoFloat(4))
        self.lineEditGamma.editingFinished.connect(lambda: self.StringtoFloat(5))
        
        self.BackButton.clicked.connect(self.PreviousPage)
        self.ExecuteButton.clicked.connect(self.Execute)


    def PreviousPage(self):
        stackedWidget.setCurrentIndex(0)


    def StringtoFloat(self,i):   
        q = self.lineEditP[i].text()
        if q != '':
            q = q.replace(',','.')
            q = float(q)
            self.p_input[i] = q
            #print(self.q_input,type(self.q_input))

       
    def Execute(self):

        print(self.p_input)
        

        def Inverse_Kinematic(X, Y, Z, alpha, beta, gamma):


            pi = math.pi
            alpha1, a1, d1 =    pi/2   ,   0.140   ,   0.405
            alpha2, a2, d2 =    0      ,   0.500   ,   0.000
            alpha3, a3, d3 =    pi/2   ,   0.105   ,   0.000
            alpha4, a4, d4 =    -pi/2  ,   0.000   ,   0.700
            alpha5, a5, d5 =    pi/2   ,   0.000   ,   0.000
            alpha6, a6, d6 =    0      ,   0.000   ,   0.075

            alpha = alpha * math.pi/180
            beta = beta * math.pi/180
            gamma = gamma * math.pi/180
            
            # Ma tran voi 3 goc Cardan
            #
            Cardan_Matrix = np.array([[math.cos(beta)*math.cos(gamma),                                                              -math.cos(beta)*math.sin(gamma),                                                            math.sin(beta),                         X   ],
                                      [math.sin(alpha)*math.sin(beta)*math.cos(gamma) + math.cos(alpha)*math.sin(gamma),            -math.sin(alpha)*math.sin(beta)*math.sin(gamma) + math.cos(alpha)*math.cos(gamma),          -math.sin(alpha)*math.cos(beta),        Y   ],
                                      [-math.cos(alpha)*math.sin(beta)*math.cos(gamma) + math.sin(alpha)*math.sin(gamma),           math.cos(alpha)*math.sin(beta)*math.sin(gamma) + math.sin(alpha)*math.cos(gamma),           math.cos(alpha)*math.cos(beta),         Z   ],
                                      [0,                                                                                           0,                                                                                          0,                                      1   ]])

            #Cardan_Matrix = Matrix([[cos(beta)*cos(gamma),                                          -cos(beta)*sin(gamma),                                          sin(beta),                  X   ],
            #                        [sin(alpha)*sin(beta)*cos(gamma) + cos(alpha)*sin(gamma),       -sin(alpha)*sin(beta)*sin(gamma) + cos(alpha)*cos(gamma),       -sin(alpha)*cos(beta),      Y   ],
            #                        [-cos(alpha)*sin(beta)*cos(gamma) + sin(alpha)*sin(theta),      cos(alpha)*sin(beta)*sin(gamma) + sin(alpha)*cos(gamma),        cos(alpha)*cos(beta),       Z   ],
            #                        [0,                                                             0,                                                              0,                          1   ]])


            # Ma tran voi 3 goc Roll - Pitch - Yall
            #
            #alpha, beta, gamma = roll, pitch, yaw
            #RPY_Matrix =    Matrix([[cos(roll)*cos(pitch),          -sin(roll)*cos(yaw) + cos(roll)*sin(pitch)*sin(yaw),        sin(roll)*sin(yaw) + cos(roll)*sin(pitch)*cos(yaw),         X   ],
            #                        [sin(roll)*cos(pitch),          cos(roll)*cos(yaw) + sin(roll)*sin(pitch)*sin(yaw),         -cos(roll)*sin(yaw) + sin(roll)*sin(pitch)*cos(yaw),        Y   ],
            #                        [-sin(pitch),                   cos(pitch)*sin(yaw),                                        cos(pitch)*cos(yaw),                                        Z   ],
            #                        [0,                             0,                                                          0,                                                          1   ]])


            # Ma tran voi 3 goc Euler
            #
            #alpha, beta, gamma = psi, theta, phi
            #Euler_Matrix =   Matrix([[cos(psi)*cos(phi) - sin(psi)*cos(theta)*sin(phi),         -cos(psi)*sin(phi) - sin(psi)*cos(theta)*cos(phi),          sin(psi)*sin(theta),            X   ],
            #                         [sin(psi)*cos(phi) + cos(psi)*cos(theta)*sin(phi),         -sin(psi)*sin(phi) + cos(psi)*cos(theta)*cos(phi),          -cos(psi)*sin(theta),           Y   ],
            #                         [sin(theta)*sin(phi),                                      sin(theta)*cos(phi),                                        cos(theta),                     Z   ],
            #                         [0,                                                        0,                                                          0,                              1   ]])


            nx = float(Cardan_Matrix[0,0])
            ny = float(Cardan_Matrix[1,0])
            nz = float(Cardan_Matrix[2,0])
            ox = float(Cardan_Matrix[0,1])
            oy = float(Cardan_Matrix[1,1])
            oz = float(Cardan_Matrix[2,1])
            ax = float(Cardan_Matrix[0,2])
            ay = float(Cardan_Matrix[1,2])
            az = float(Cardan_Matrix[2,2])
            px = float(Cardan_Matrix[0,3])
            py = float(Cardan_Matrix[1,3])
            pz = float(Cardan_Matrix[2,3])

            #   R_sao = np.array([[nx   ,   ox  ,   ax  ],
            #                     [ny   ,   oy  ,   ay  ],
            #                     [nz   ,   oz  ,   az  ]])
            #   r_sao = np.array([[px   ,   py  ,   pz  ]])
            #   r_sao = np.reshape(r_sao,(1,3))
            #

            rpx = px - ax*d6                # rp = r04 (Xem lai do an tinh toan Dong hoc nguoc)
            rpy = py - ay*d6
            rpz = pz - az*d6
            #r_p = np.array([[rpx, rpy, rpz]])
            #r_p = np.reshape(r_p,(1,3))
    

            # q1
            q1 = math.atan2(py-ay*d6 , px-ax*d6)

            # q2
            A = rpx*math.cos(q1) + rpy*math.sin(q1) - a1
            B = rpz -d1
            F = A*A + B*B + a2*a2 - a3*a3 - d4*d4
            D = 2*B*a2
            H = 2*A*a2
            r2 = math.sqrt(D*D + H*H)
            PHI = math.atan2(H,D)
            S_q2_PHI = F / r2                 # q2_PHI  = q2 + PHI
            C_q2_phi = math.sqrt(1 - S_q2_PHI*S_q2_PHI)
            q2 = math.atan2(S_q2_PHI,C_q2_phi) - PHI

            # q3
            s23 = ((A - a2*math.cos(q2))*d4 + (B - a2*math.sin(q2))*a3) / (d4*d4 + a3*a3)
            c23 = ((A - a2*math.cos(q2))*a3 + (B - a2*math.sin(q2))*d4) / (d4*d4 + a3*a3)
            q23 = math.atan2(s23,c23)
            q3 = q23 - q2

            # Ma tran R36 tinh tu Ma tran 3 goc Cardan va q1, q2, q3
            R11 = nx*math.cos(q1)*math.cos(q2+q3) + ny*math.sin(q1)*math.cos(q2+q3) + nz*math.sin(q2+q3)
            R21 = nx*math.sin(q1) - ny*math.cos(q1)
            R31 = nx*math.cos(q1)*math.sin(q2+q3) + ny*math.sin(q1)*math.sin(q2+q3) - nz*math.cos(q2+q3)
            R12 = ox*math.cos(q1)*math.cos(q2+q3) + oy*math.sin(q1)*math.cos(q2+q3) + oz*math.sin(q2+q3)
            R22 = ox*math.sin(q1) - oy*math.cos(q1)
            R32 = ox*math.cos(q1)*math.sin(q2+q3) + oy*math.sin(q1)*math.sin(q2+q3) - oz*math.cos(q2+q3)
            R13 = ax*math.cos(q1)*math.cos(q2+q3) + ay*math.sin(q1)*math.cos(q2+q3) + az*math.sin(q2+q3)
            R23 = ax*math.sin(q1) -ay*math.cos(q1)
            R33 = ax*math.cos(q1)*math.sin(q2+q3) + ay*math.sin(q1)*math.sin(q2+q3) - az*math.cos(q2+q3)
            #R36 = Matrix([[R11  ,   R12 ,   R13],
            #              [R21  ,   R22 ,   R23],
            #              [R31  ,   R32 ,   R33]])

            # q5, q4, q6
            s5 = math.sqrt(R13*R13 + R23*R23)
            c5 = R33
            q5 = math.atan2(s5,c5)
            Condition1 = abs(q5) > 1e-3
            Condition2 = R33 > 0    # cosq5 = R33
            if Condition1 == True :
                q4 = math.atan2(R23,R13)
                q6 = math.atan2(R32,-R31)
            elif Condition2 == True :
                q5 = 0.000
                q4 = 0.000
                q6 = math.atan2(R21,R11)
            else :
                q5 = -pi
                q4 = 0.000
                q6 = math.atan2(R12,R22)
    
            q1 = round(q1 * 180/math.pi ,3)
            q2 = round(q2 * 180/math.pi ,3)
            q3 = round(q3 * 180/math.pi ,3)
            q4 = round(q4 * 180/math.pi ,3)
            q5 = round(q5 * 180/math.pi ,3)
            q6 = round(q6 * 180/math.pi ,3)

            Q = np.array([q1, q2, q3, q4, q5, q6])
            #Q = np.reshape(Q,(6,1))

            return Q

        self.q_output = Inverse_Kinematic(self.p_input[0],self.p_input[1],self.p_input[2],self.p_input[3],self.p_input[4],self.p_input[5])
        print(self.q_output)
        self.lcdNumberQ1.display(self.q_output[0])
        self.lcdNumberQ2.display(self.q_output[1])
        self.lcdNumberQ3.display(self.q_output[2])
        self.lcdNumberQ4.display(self.q_output[3])
        self.lcdNumberQ5.display(self.q_output[4])
        self.lcdNumberQ6.display(self.q_output[5])



        logger = logging.getLogger(__name__)

        # Connect PLC 1

        IP1 = '192.168.0.10'
        RACK = 0
        SLOT = 1
        DB_NUMBER_1 = 100
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        plc1 = snap7.client.Client()
        plc1.connect(IP1,RACK,SLOT)
        print(plc1.get_cpu_state())

        # Connect PLC 2

        IP2 = '192.168.0.1'
        RACK = 0
        SLOT = 1
        DB_NUMBER_2 = 150
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        plc2 = snap7.client.Client()
        plc2.connect(IP2,RACK,SLOT)
        print(plc2.get_cpu_state())

        # Write Ouput Servo (q)

        def WriteDBPLC(plc,db_number,offset,number):
            plc.db_write(db_number, offset, bytearray(struct.pack(">f", number)))

        def ReadDBPLC(plc,db_number,offset):
            data = plc.db_read(db_number,offset,4)
            data = struct.unpack('>f',data)
            print("Value = {}".format(data))
            return data

        WriteDBPLC(plc1,DB_NUMBER_1,0,self.q_output[0])
        WriteDBPLC(plc1,DB_NUMBER_1,4,self.q_output[1])
        WriteDBPLC(plc1,DB_NUMBER_1,8,self.q_output[2])
        WriteDBPLC(plc1,DB_NUMBER_1,12,10000)
        WriteDBPLC(plc1,DB_NUMBER_1,16,10000)
        WriteDBPLC(plc1,DB_NUMBER_1,20,10000)

        WriteDBPLC(plc2,DB_NUMBER_2,0,self.q_output[3])
        WriteDBPLC(plc2,DB_NUMBER_2,4,self.q_output[4])
        WriteDBPLC(plc2,DB_NUMBER_2,8,self.q_output[5])
        WriteDBPLC(plc2,DB_NUMBER_2,12,10000)
        WriteDBPLC(plc2,DB_NUMBER_2,16,10000)
        WriteDBPLC(plc2,DB_NUMBER_2,20,10000)

        ReadDBPLC(plc1,DB_NUMBER_1,0)
        ReadDBPLC(plc1,DB_NUMBER_1,4)
        ReadDBPLC(plc1,DB_NUMBER_1,8)
        ReadDBPLC(plc1,DB_NUMBER_1,12)
        ReadDBPLC(plc1,DB_NUMBER_1,16)
        ReadDBPLC(plc1,DB_NUMBER_1,20)

        ReadDBPLC(plc2,DB_NUMBER_2,0)
        ReadDBPLC(plc2,DB_NUMBER_2,4)
        ReadDBPLC(plc2,DB_NUMBER_2,8)
        ReadDBPLC(plc2,DB_NUMBER_2,12)
        ReadDBPLC(plc2,DB_NUMBER_2,20)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('MainWindow.ui', self)
        self.commandLinkButton1.clicked.connect(self.gotoWindow1)
        self.commandLinkButton2.clicked.connect(self.gotoWindow2)
        self.commandLinkButton3.clicked.connect(self.gotoWindow3)
        self.commandLinkButton4.clicked.connect(self.gotoWindow4)

    def gotoWindow1(self):
        stackedWidget.setCurrentIndex(1)
    def gotoWindow2(self):
        stackedWidget.setCurrentIndex(2)
    def gotoWindow3(self):
        stackedWidget.setCurrentIndex(3)
    def gotoWindow4(self):
        stackedWidget.setCurrentIndex(4)

    

app = QApplication(sys.argv)
stackedWidget = QStackedWidget()
stackedWidget.addWidget(MainWindow())
stackedWidget.addWidget(Window1())
stackedWidget.addWidget(Window2())
stackedWidget.addWidget(Window3())
#stackedWidget.addWidget(Window4())

stackedWidget.setFixedWidth(1200)
stackedWidget.setFixedHeight(900)
stackedWidget.show()
sys.exit(app.exec_())























