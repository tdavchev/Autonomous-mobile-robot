import sys, math
from numpy import matrix

rTheta = matrix([[1.0,0.0,0.0],
		         [0.0,1.0,0.0],
		         [0.0,0.0,1.0]])
l = 10.0
pi = 3.1415926535897932384626433832795028841971693993751058
r = 1.0
a = matrix([[0.0],[0.0],[0.0]])
# initializing an empty matrix
speeds = matrix([[0.0 for row in range(0,1)] for col in range(0,3)])


def populate():
	global l, speeds, rTheta, r, a
	print "Task 3.3 Please specify x, y and z positions of the omniwheel drive "
	print "in numbers and you will get the speeds for all three of them."
	print  "Please insert the x direction:"
	ans = raw_input("> ")
	print "x confirmed to be: ", ans
	x = float(ans)
	ans = ''
	print "Please insert the y direction:"
	ans = raw_input("> ")
	print "y confirmed to be: ", ans
	y = float(ans)
	ans = ''
	print "Please insert theta direction:"
	ans = raw_input("> ")
	z = float(ans)
	print "z confirmed to be ", ans
	ans = ''
	J1f = matrix([[x*math.sin(pi/3.0), -y*(math.cos(pi/3.0)), -l*z],
	 		 	  [x*0, -y*(math.cos(pi)), -l*z],
	 		 	  [x*math.sin(-(pi/3)), -y*(math.cos(-(pi/3))), -l*z]])
	iDentity = matrix([[1.0,0.0,0.0],
		         	   [0.0,1.0,0.0],
		         	   [0.0,0.0,1.0]])

	speeds = (1.0/r) * rTheta * J1f * iDentity
	a[0] = speeds.item(0) + speeds.item(1) + speeds.item(2)
	a[1] = speeds.item(3) + speeds.item(4) + speeds.item(5)
	a[2] = speeds.item(6) + speeds.item(7) + speeds.item(8)

def main():
	global a
	populate()
	
	print a

if __name__ == '__main__':
	main()