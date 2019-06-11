#!/usr/bin/python
import math, sys, os, time

#chmod +x manage.py


sudoPassword = '6RS'
chuckCalibrateCommand = 'chuck checkCalibration --update-off'
chuckReboot = 'sudo reboot'

chargeDistance = 1.65 #Added distance to account for distance to perform the Charging command

xInput = sys.argv[1] #Input value for x-coordinate for the charger from the GRM
yInput = sys.argv[2] #Input value for y-coordinate for the charger from the GRM
tInput = sys.argv[3] #Input value for orientation for the charger from the GRM
print(xInput)
print(yInput)
print(tInput)

chargeAngle = float(tInput) + 90 #GRM specifies angle 90 degrees diffeent from what the Chuck move command use

#Based on the charger distance and oriantation trigonometry is used to determine how to position the robot for charging 
theta = math.radians(float(tInput)) 

xAdd = math.sin(theta)*chargeDistance*(-1)
yAdd = math.cos(theta)*chargeDistance*(-1)

#Add x and y value to create new coordinates for the charging distance 
newX = float(xInput) + xAdd
newY = float(yInput) + yAdd


print(newX)
print(newY)

print(chargeAngle)

chuckMoveCommand = 'chuck move --x {} --y {} --theta {}'.format(newX,newY,chargeAngle)

print(chuckMoveCommand)


#Call bash command to move the Chuck to the correct location in fron of the Charger 
#os.system('echo %s|sudo -S %s' % (sudoPassword, chuckMoveCommand))
os.system(chuckMoveCommand)


print("Preparing to start Calibration...")
time.sleep(3)

#Call the command to run the calibration on the Chuck
#os.system('echo %s|sudo -S %s' % (sudoPassword, chuckCalibrateCommand))
os.system(chuckCalibrateCommand)
time.sleep(1)

#Ask SWRE if they want to reboot the Chuck after calibration is done
rebootQuestion = None
while rebootQuestion not in ("y", "n"):
	rebootQuestion = raw_input("Calibration is done, do you want to reboot Chuck? (Y/N)\n").lower().strip()
	print(rebootQuestion)
	if rebootQuestion[0] == "y":
		print(sudoPassword)
		print("Rebooting Chuck...")
		time.sleep(1)
		#os.system('echo %s|sudo -S %s' % (sudoPassword, chuckReboot))
		os.system(chuckReboot)
	elif rebootQuestion[0] == "n":
		print("Exiting Calibration tool...")
		time.sleep(2)
		exit()


 

#curl -s --header "Authorization: Bearer $jwtToken" --header "Content-Type: application/json" -X GET "https://grm.6river.org/v1/MfpConfigs" | jq '[.[] | {name: .name, site: .siteId}]' > mfps.json
#chuck move --x str(newX) --y str(newY) --theta str(chargeAngle)