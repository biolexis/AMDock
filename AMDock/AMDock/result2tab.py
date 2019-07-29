import re, os
from math import exp, pow

R = 0.001987207  # kcal/mol*K
T = 298.15  # K


class Result_Analysis():
    def __init__(self, result_file=None, filename=None, protein=None, ha=0):
        self.rfile = result_file
        self.fname = filename
        self.protein = protein
        self.heavy_atoms = ha
        try:
            self.result2pdb()
        except:
            pass
        try:
            self.best()
        except:
            pass

    def energy2ki(self, energy):
        energy = float(energy)
        Ki = exp(energy / (R * T))
        return Ki

    def converter(self, number):
        units = ['M', 'mM', 'uM', 'nM']
        exponente = 0
        base = pow(10, exponente)
        out_number = number * base
        while out_number < 1 or out_number > 10:
            exponente += 1
            base = pow(10, exponente)
            out_number = number * base
        if exponente in [0, 1]:
            rep_number = number
            return rep_number, units[0]
        elif exponente in [2, 3, 4]:
            rep_number = number * 1000
            return rep_number, units[1]
        elif exponente in [5, 6]:
            rep_number = number * 1000000
            return rep_number, units[2]
        elif exponente in [7, 8, 9, 10]:
            rep_number = number * 1000000000
            return rep_number, units[3]
        else:
            rep_number = number
            return rep_number, '-'

    def best(self):
        protein_file = open(self.protein, 'r')
        result_file = open(self.fname, 'r')
        best_file = open('best_pose' + self.fname[9:], 'w')
        best_file.write("REMARK Complex with Best Pose\n")
        for line in protein_file:
            line = line.strip('\n')
            best_file.write(line[:67] + line[13:14].rjust(11) + '\n')
        protein_file.close()
        n = 0
        for line in result_file:
            line = line.strip('\n')
            n += 1
            if n == 1:
                continue
            else:
                if re.search('ENDMDL', line):
                    break
                else:
                    best_file.write(line + '\n')
        protein_file.close()
        result_file.close()
        best_file.close()

    def result2table(self):
        file = open(self.fname, 'r')
        pose = 1
        modes = []
        for line in file:
            line = line.strip("\n")
            if re.search('REMARK ENERGY', line):
                energy = float((line.split()[3]).strip())
                Ki_value = self.energy2ki(energy)
                Ki, unit = self.converter(Ki_value)
                ligand_efficiency = energy / self.heavy_atoms
                modes_info = [pose, energy, '%.2f' % Ki, unit, '%.2f' % ligand_efficiency]
                modes.append(modes_info)
                pose += 1
        return modes

    def result2pdb(self):
        output_file = open(self.fname, 'w')
        models = 1
        if self.rfile.split('.')[-1] == 'dlg':
            output_file.write('REMARK Generado por AMDock from AutoDock4 result' + '\n')
            result = open(self.rfile, 'r')
            for line in result:
                line = line.strip('\n')
                if re.search('MODEL', line[:5]):
                    output_file.write('MODEL' + ('%d' % models).rjust(9) + '\n')
                    models += 1
                elif re.search('ATOM', line[:5]) or re.search('HETATM', line[:6]):
                    output_file.write(line[:67] + line[13:14].rjust(11) + '\n')
                elif re.search('ENDMDL', line[:6]):
                    output_file.write(line + '\n')
                if re.search('USER    Estimated Free Energy of Binding', line[:43]):
                    output_file.write('REMARK ENERGY   =   %s\n' % line.split()[7].strip())
            result.close()
        else:
            output_file.write('REMARK Generado por AMDock from AutoDock Vina result' + '\n')
            result = open(self.rfile, 'r')
            for line in result:
                line = line.strip('\n')
                if re.search('REMARK VINA RESULT', line):
                    output_file.write('REMARK ENERGY   =   %s\n' % line.split()[3].strip())
                if re.search('MODEL', line[:5]):
                    output_file.write('MODEL' + ('%d' % models).rjust(9) + '\n')
                    models += 1
                elif re.search('ATOM', line[:5]) or re.search('HETATM', line[:6]):
                    output_file.write(line[:67] + line[13:14].rjust(11) + '\n')
                elif re.search('ENDMDL', line[:6]):
                    output_file.write(line + '\n')
            result.close()
        output_file.close()


class Scoring2table(Result_Analysis):
    def __init__(self, result_file=None, filename=None, protein=None, ha=0):
        Result_Analysis.__init__(self, result_file, filename, protein, ha)
        self.log_file = result_file
        self.lig_name = os.path.split(result_file)[-1][:-10]
        self.heavy_atoms = ha

    def result2table(self):
        file = open(self.log_file, 'r')
        modes = []
        energy = 0
        for line in file:
            line = line.strip('\n')
            if re.search('Affinity:', line):
                energy = float(line.split()[1])
            elif re.search('Estimated Free Energy of Binding', line):
                energy = float(line.split()[8])

        Ki_value = self.energy2ki(energy)
        Ki, unit = self.converter(Ki_value)
        ligand_efficiency = energy / self.heavy_atoms
        modes_info = [1, energy, '%.2f' % Ki, unit, '%.2f' % ligand_efficiency]
        modes.append(modes_info)

        return modes
