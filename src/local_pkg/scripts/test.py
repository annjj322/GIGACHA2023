import json
import numpy as np
import matplotlib.pyplot as plt
import cubic_spline_planner as cs
class making_map():
    def __init__(self):
        self.path = "/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/right_curve.json"
        self.path_jikjin = "/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/Inha_Songdo/songdo_jikjin_course.json"
        self.x_full = None
        self.y_full = None
        print("started!")

    def divide(self):
        with open(self.path,'r') as f:
            data = json.load(f)

        x_raw = []
        y_raw = []
        x_jik = []
        y_jik = []
        x_full = []
        y_full = []
        
        for i in range(len(data)):
            values = list(data.values())
            x_raw.append(values[i][0])
            y_raw.append(values[i][1])

        with open(self.path_jikjin,'r') as f2:
            data2 = json.load(f2)
        
        for i in range(len(data2)):
            values = list(data2.values())
            x_jik.append(values[i][0])
            y_jik.append(values[i][1])

        for i in range(len(data2)-1):
            x_tmp = np.linspace(x_jik[i], x_jik[i+1], 20, endpoint=False)
            y_tmp = np.linspace(y_jik[i], y_jik[i+1], 20, endpoint=False)

            for i in range(len(x_tmp)):
                x_full.append(x_tmp[i])
                y_full.append(y_tmp[i])

        x_full.append(x_raw[-1])
        y_full.append(y_raw[-1])
        x_full2,y_full2= cs.main(x_raw,y_raw)
        self.x_full = x_full + x_full2
        self.y_full = y_full + y_full2
        
        # # for plot
        #plt.plot(x_raw, y_raw, 'ro', ms = 10)
        #plt.plot(x_full, y_full, 'bo', ms = 1)
        plt.subplots(1)
        plt.plot(x_jik,y_jik,'ro',ms=3) #직진 
        plt.grid()
        plt.subplots(1)
        plt.plot(x_full2,y_full2,'ro',ms=3) #우회전
        plt.grid()
        plt.subplots(1) 
        plt.plot(self.x_full,self.y_full,'bo',ms=1) #합친거
        plt.legend()
        # plt.xlim(50,75)
        # plt.ylim(64,89)
        plt.grid()
        plt.show()

        print("divided!")

    def append(self, i, x_input, y_input):
        with open(self.path, "a") as f:
            f.write('\t"{}": [\n'.format(i))
            f.write('\t\t{},\n'.format(x_input))
            f.write('\t\t{},\n'.format(y_input))
            f.write('\t\t"driving",\n')
            f.write('\t\t20\n')
            f.write('\t],\n')
            print("\nappended : {}\n".format(i))

    def start(self):
        with open(self.path, "w") as f:
            f.write("{\n")

    def end(self):
        with open(self.path, "a") as f:
            f.write("}")

    def main(self):
        self.divide()
        self.start()
        for i in range(len(self.x_full)):
            self.append(i, self.x_full[i], self.y_full[i])
        self.end()

if __name__ == "__main__":
    mm = making_map()
    mm.main()
