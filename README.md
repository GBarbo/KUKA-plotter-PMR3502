# KUKA - PMR3502-2023

Instructions for a KUKA robotic manipulator pen plotter as part of the discipline [PMR3502-2023](https://edisciplinas.usp.br/course/view.php?id=109453).

## Usage

1. Make a csv file containing the function name on the first line and the lines and circular arcs as following:
- "l,spx,spy,epx,epy" if a line;
- "c,spx,spy,mpx,mpy,epx,epy,ang" if a circular arc;
- ang is the angle of the circular arc
- spx,spy are the global coordinates of the starting point, mpx,mpy of the middle point and epx,epy of the end point;
- Also indicate whether the last line/circle needs to start in a point other than the last dranw, with an "1" at the 8th position of the line.
2. Open the file kuka.py and substitute the "path" variable to the path where the csv file is located. The script should print the KUKA function once run.
3. Paste the printed function on the src file and call it when necessary specifying (i) the starting point P, (ii) the scale S and (iii) the frame MESA, as following:
```PLTURSO(P,S,MESA)```
