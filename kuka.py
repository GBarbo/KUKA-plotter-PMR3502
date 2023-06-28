# Reads a CSV file and returns a KUKA script
# PMR3502 - 2023 - Poli-USP

import csv

def read_csv_file(filename):
    # Reads csv returs list

    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def str_to_flt(list_of_lists):
    # Returns list values as floats

    result = []
    for line in list_of_lists:
        floats = [line[0]] + [float(value) if value != '' else value for value in line[1:-1]] + [line[-1]]
        result.append(floats)
    return result

def roundList(list):
    # Rounds each float on the list

    for line in list:
        for i in range(1,7):
            if line[i] != '': line[i] = round(float(line[i]),3)
    return list

def global_to_relative(path):
    # Reads csv file and returns relative position change after each movement

    file = read_csv_file(path)
    title = file[0][0]

    file = file[1:]
    file_n = file[:]
    file = str_to_flt(file) 
    file_n = str_to_flt(file_n)

    last_circle = False

    for i in range(len(file_n)):
        if file[i][0] == 'c' and i != 0:
            if last_circle == False: 
                file_n[i][1] = file[i-1][3]-file[i][1]
                file_n[i][2] = file[i-1][4]-file[i][2]
            else: 
                file_n[i][1] = file[i-1][5]-file[i][1]
                file_n[i][2] = file[i-1][6]-file[i][2]
            file_n[i][3] = file[i][3]-file[i][1]
            file_n[i][4] = file[i][4]-file[i][2]
            file_n[i][5] = file[i][5]-file[i][1]
            file_n[i][6] = file[i][6]-file[i][2]

            last_circle = True
            
        elif file[i][0] == 'l' and i != 0:
            if last_circle == False: 
                file_n[i][1] = file[i-1][3]-file[i][1]
                file_n[i][2] = file[i-1][4]-file[i][2]
            else: 
                file_n[i][1] = file[i-1][5]-file[i][1]
                file_n[i][2] = file[i-1][6]-file[i][2]
            file_n[i][3] = file[i][3]-file[i][1]
            file_n[i][4] = file[i][4]-file[i][2]

            last_circle = False
        
        else: 
            if file[i][0] == 'l':
                file_n[i][3] = file[i][3]-file[i][1]
                file_n[i][4] = file[i][4]-file[i][2]
            else: 
                file_n[i][3] = file[i][3]-file[i][1]
                file_n[i][4] = file[i][4]-file[i][2]
                file_n[i][5] = file[i][5]-file[i][1]
                file_n[i][6] = file[i][6]-file[i][2]

    return roundList(file_n),title

def csvToKUKA(list,title):
    # Takes in csv with relative movements and function title 
    # Prints function in KUKA function that plots the drawing
    # Arguments of KUKA function: S = Scale, MESA = frame, P = Starting point

    file = list

    print(f'DEF {title}(P,S,MESA:IN)')

    print('POS P, E, M')
    print('REAL S')
    print('FRAME MESA')

    print('P.Z = P.Z - 30')
    print('LIN MESA:P')


    for line in file:
        # Proceeds to print relative movement for each circle arc or line

        if line[0] == 'c':      # Circle arc
            sp = line[1],line[2]    # Start point
            mp = line[3],line[4]    # Middle point
            ep = line[5],line[6]    # End point
            ang = line[7]           # Arc angle

            if line[8] == '1':      # Leave paper to go to starting point
                         
                print('P.Z = P.Z + 30')
                print('LIN MESA:P')
                print('WAIT SEC 1')

                if float(sp[0]) >= 0: print(f'P.X = P.X + {sp[0]}*S')
                else: print(f'P.X = P.X - {abs(float(sp[0]))}*S')
                if float(sp[1]) >= 0: print(f'P.Y = P.Y + {sp[1]}*S')
                else: print(f'P.Y = P.Y - {abs(float(sp[1]))}*S')
                
                print('LIN MESA:P')
                print('WAIT SEC 1')

                print('P.Z = P.Z - 30')
                print('LIN MESA:P')
                print('WAIT SEC 1')

                print('M = P')
                if float(mp[0]) >= 0: print(f'M.X = P.X + {mp[0]}*S')
                else: print(f'M.X = P.X - {abs(float(mp[0]))}*S')
                if float(mp[1]) >= 0: print(f'M.Y = P.Y + {mp[1]}*S')
                else: print(f'M.Y = P.Y - {abs(float(mp[1]))}*S')

                print('E = P')
                if float(ep[0]) >= 0: print(f'E.X = P.X + {ep[0]}*S')
                else: print(f'E.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) >= 0: print(f'E.Y = P.Y + {ep[1]}*S')
                else: print(f'E.Y = P.Y - {abs(float(ep[1]))}*S')

                print(f'CIRC MESA:M,MESA:E,CA {float(ang)}') 

                # Actualize ending point as next feature's starting point
                if float(ep[0]) >= 0: print(f'P.X = P.X + {ep[0]}*S')
                else: print(f'P.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) >= 0: print(f'P.Y = P.Y + {ep[1]}*S')
                else: print(f'P.Y = P.Y - {abs(float(ep[1]))}*S')
                
            else:
                print('M = P')
                if float(mp[0]) >= 0: print(f'M.X = P.X + {mp[0]}*S')
                else: print(f'M.X = P.X - {abs(float(mp[0]))}*S')
                if float(mp[1]) >= 0: print(f'M.Y = P.Y + {mp[1]}*S')
                else: print(f'M.Y = P.Y - {abs(float(mp[1]))}*S')

                print('E = P')
                if float(ep[0]) >= 0: print(f'E.X = P.X + {ep[0]}*S')
                else: print(f'E.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) >= 0: print(f'E.Y = P.Y + {ep[1]}*S')
                else: print(f'E.Y = P.Y - {abs(float(ep[1]))}*S')

                print(f'CIRC MESA:M,MESA:E,CA {float(ang)}')

                # Actualize ending point as next feature's starting point
                if float(ep[0]) >= 0: print(f'P.X = P.X + {ep[0]}*S')
                else: print(f'P.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) >= 0: print(f'P.Y = P.Y + {ep[1]}*S')
                else: print(f'P.Y = P.Y - {abs(float(ep[1]))}*S')

        else:   # Line
            sp = line[1],line[2]    # Start point
            ep = line[3],line[4]    # End point
            
            if line[8] == '1':      # Leave paper to go to starting point
                print('P.Z = P.Z + 30')
                print('LIN MESA:P')
                print('WAIT SEC 1')

                if not(sp[0] == 0.0 and sp[1] == 0.0):      # For clearer code
                    if float(sp[0]) > 0: print(f'P.X = P.X + {sp[0]}*S')
                    elif float(sp[0]) < 0: print(f'P.X = P.X - {abs(float(sp[0]))}*S')
                    if float(sp[1]) > 0: print(f'P.Y = P.Y + {sp[1]}*S')
                    elif float(sp[1]) < 0: print(f'P.Y = P.Y - {abs(float(sp[1]))}*S')
                
                print('LIN MESA:P')
                print('WAIT SEC 1')

                print('P.Z = P.Z - 30')
                print('LIN MESA:P')
                print('WAIT SEC 1')

                if float(ep[0]) > 0: print(f'P.X = P.X + {ep[0]}*S')
                elif float(ep[0]) < 0: print(f'P.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) > 0: print(f'P.Y = P.Y + {ep[1]}*S')
                elif float(ep[1]) < 0: print(f'P.Y = P.Y - {abs(float(ep[1]))}*S')
                
                print('LIN MESA:P')

            else:
                if not(sp[0] == 0.0 and sp[1] == 0.0):
                    if float(sp[0]) > 0: print(f'P.X = P.X + {sp[0]}*S')
                    elif float(sp[0]) < 0: print(f'P.X = P.X - {abs(float(sp[0]))}*S')
                    if float(sp[1]) > 0: print(f'P.Y = P.Y + {sp[1]}*S')
                    elif float(sp[1]) < 0: print(f'P.Y = P.Y - {abs(float(sp[1]))}*S')

                if float(ep[0]) > 0: print(f'P.X = P.X + {ep[0]}*S')
                elif float(ep[0]) < 0: print(f'P.X = P.X - {abs(float(ep[0]))}*S')
                if float(ep[1]) > 0: print(f'P.Y = P.Y + {ep[1]}*S')
                elif float(ep[1]) < 0: print(f'P.Y = P.Y - {abs(float(ep[1]))}*S')

                print('LIN MESA:P')
   
    print(f'P.Z = P.Z + 30')
    print(f'LIN MESA:P')
    print('END')

path = "/Users/giovanni/Desktop/KUKA-plotter-PMR3502/urso.csv"
urso = global_to_relative(path)
csvToKUKA(urso[0],urso[1])

