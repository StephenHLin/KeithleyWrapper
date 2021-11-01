"""
Created May 08, 2014
@author Stephen
written for Python 2.7
requires: PyVISA, Numpy, numutil
Written using: Anaconda


-Updated as of April 20 2018
Quotation marks were causing errors, specifically in the *IDN? command. Use single quotations, not double.

"""
#Define Class Keithley
class K2602():

 
    #Connnects to the Keithley Device
    def connect(self,GPIB,rm):    
        self.rm = rm
        self.instrument = self.rm.get_instrument('GPIB::'+str(GPIB),timeout=0.1) #Connects with the device in the GPIB port
        #self.instrument.write('waitcomplete()')
        self.instrument.write('*IDN?') #Requests the device for identification
        #self.instrument.write('waitcomplete()')
        print(self.instrument.read())  #Displays the response
                   
    def initialize(self):
        try:
            BufferSize = 100000 #Keithley should default to this value by itself.
            self.instrument.chunk_size = BufferSize  #Sets the buffersize for data logging(in bytes)
            self.instrument.timeout = 120 #Sets the keithley timeout parameter, again, not sure if this auto-prompts in Matlab 
            
            #-----------Set all Parameters-----------
            self.instrument.write('smua.reset()') #Resets channel A
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.reset()')#Resets channel B
            self.instrument.write('waitcomplete()')
            
            self.instrument.write('smua.nvbuffer1.clear()')#Clear buffer 1 in Channel A
            self.instrument.write('smua.nvbuffer2.clear()')#Clear buffer 2 in Channel A
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.nvbuffer1.clear()')#Clear buffer 1 in Channel B
            self.instrument.write('smub.nvbuffer2.clear()')#Clear buffer 2 in Channel B
            self.instrument.write('waitcomplete()')
            
            #-------NOT overwriting Previous Data in buffer -------
            self.instrument.write('smua.nvbuffer1.appendmode = 1')#Channel A Buffer 1
            self.instrument.write('smua.nvbuffer2.appendmode = 1')#Channel A Buffer 2
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.nvbuffer1.appendmode = 1')#Channel B Buffer 1
            self.instrument.write('smub.nvbuffer2.appendmode = 1')#Channel B Buffer 2
            self.instrument.write('waitcomplete()')
            
            self.instrument.write('smua.nvbuffer1.collectsourcevalues = 0')#Channel A Buffer 1 
            self.instrument.write('smua.nvbuffer2.collectsourcevalues = 0')#Channel A Buffer 2
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.nvbuffer1.collectsourcevalues = 0')#Channel B Buffer 1 
            self.instrument.write('smub.nvbuffer2.collectsourcevalues = 0')#Channel B Buffer 2
            self.instrument.write('waitcomplete()')
            
            self.instrument.write('smua.nvbuffer1.collecttimestamps = 0')#Channel A Buffer 1
            self.instrument.write('smua.nvbuffer2.collecttimestamps = 0')#Channel A Buffer 2
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.nvbuffer1.collecttimestamps = 0')#Channel B Buffer 1
            self.instrument.write('smub.nvbuffer2.collecttimestamps = 0')#Channel B Buffer 2
            self.instrument.write('waitcomplete()')
            
            #---------Set the Buffer Initial Count to 1---------
            self.instrument.write('smua.measure.count = 1')#Channel A
            self.instrument.write('waitcomplete()')
            self.instrument.write('smub.measure.count = 1')#Channel B
            self.instrument.write('waitcomplete()')
               
            print('Keithley Connected')
            
        except:
            self.ShowAllErrors()
    
    def disconnect(self):
        #-------------Turn output off if still on------------
        self.instrument.write('print(smua.source.output)')
        self.instrument.write('waitcomplete()')
        stateA =float(self.instrument.read())
        
        self.instrument.write('print(smub.source.output)')
        self.instrument.write('waitcomplete()')
        stateB =float(self.instrument.read())
        
        #----------if output on Channel A is on, turn it off before disconnecting
        if stateA == 1:
            self.instrument.write('smua.source.output = smua.OUTPUT_OFF')
            self.instrument.write('waitcomplete()')
    
        #----------if output on Channel B is on, turn it off before disconnecting 
        if stateB == 1:
            self.instrument.write('smub.source.output = smub.OUTPUT_OFF')
            self.instrument.write('waitcomplete()')
    
        self.instrument.write('*CLS') #Clears States
        self.instrument.write('waitcomplete()')
        self.instrument.write('errorqueue.clear()')#clears error queue
        self.instrument.write('waitcomplete()')        
        self.instrument.write('*RST') #resets the instrument to default stage
        self.instrument.write('waitcomplete()')
        self.instrument.close #disconnects with the instrument 
        print('Keithley Disconnected.')
        
    #Sets current limits for A and B channels
    #no error is returned to pyVisa, thus I had to use a manual way of checking the input from the user
    #to display the correct error
    #The limiti setting in the last 'else' portion is so that keithley will generate an error to read
    #otherwise the machine will not return an error
        
    def limitCurrA(self,limiti):
        #limiti = input("Enter Current limit (Max: 3amps): ")
            
        if isinstance(limiti,(int,long,float,complex)):
            if limiti > 3:
                self.instrument.write('smua.source.limiti ='+str(limiti))
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()
            
            else:
                self.instrument.write('smua.source.limiti ='+str(limiti)) #Communicates to device to change the current
                self.instrument.write('waitcomplete()')            
                print('Success')    
            
        else:
            self.instrument.write('smua.source.limiti ='+str(limiti))
            self.instrument.write('waitcomplete()')
            self.ShowAllErrors()
            
                 
    def limitCurrB(self,limiti):
        #limiti = input("Enter Current limit (Max: 3amps): ")
    
        if isinstance(limiti,(int,long,float,complex)):
            if limiti > 3:
                self.instrument.write('smub.source.limiti ='+str(limiti))
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()
                
            else:
                self.instrument.write('smub.source.limiti ='+str(limiti)) #Communicates to device to change the current
                self.instrument.write('waitcomplete()')            
                print('Success')    
            
        else:
            self.instrument.write('smub.source.limiti ='+str(limiti))
            self.instrument.write('waitcomplete()')
            self.ShowAllErrors()
            
                
    #Sets the voltage limits for A and B Channels
    def limitVoltA(self,limitv):
        #limitv = input("Enter Voltage limit (max 40volts): ")
        if isinstance(limitv,(int,long,float,complex)):
            if limitv > 40:
                self.instrument.write('smua.source.limitv ='+str(limitv))
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()
            
            else:
                self.instrument.write('smua.source.limitv ='+str(limitv)) #Communicates to device to change the current
                self.instrument.write('waitcomplete()')            
                print('Success')    
            
        else:
            self.instrument.write('smua.source.limitv ='+str(limitv))
            self.instrument.write('waitcomplete()')
            self.ShowAllErrors()
                
    def limitVoltB(self,limitv):
        #limitv = input("Enter Voltage limit (max 40volts): ")
        if isinstance(limitv,(int,long,float,complex)):
            if limitv > 40:
                self.instrument.write('smub.source.limitv ='+str(limitv))
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()
                
            else:
                self.instrument.write('smub.source.limitv ='+str(limitv)) #Communicates to device to change the current
                self.instrument.write('waitcomplete()')            
                print('Success')    
            
        else:
            self.instrument.write('smub.source.limitv ='+str(limitv))
            self.instrument.write('waitcomplete()')
            self.ShowAllErrors()
    
    
    #Sets the integration time of the ADCS in the keithley for the measurement functions
    #NPLC stands for Number of Power Line Cycles
    #Caluclation is NPLC/60Hz
    #Changing the nplc values will affect teh usable digits, the amount of reading noise
    #and the ultimate reading rate of the instrument
    #The range of values are: 0.001, to 25. Where 0.001 isthe fastest (least precise)
    # and 25 is the slowest (most precise)
    def setnplcA(self,nplc):
        #nplc = input("Enter Number of Powerline Cycles: ")
        try:
            self.instrument.write('smua.measure.nplc ='+str(nplc)) #Delay for NPLC power cycle (nplc/60Hz)
            self.instrument.write('waitcomplete()')
            print('Success')
            
        except:
            self.ShowAllErrors()
            
    def setnplcB(self,nplc):
        #nplc = input("Enter Number of Powerline Cycles: ")
        try:
            self.instrument.write('smub.measure.nplc ='+str(nplc)) #Delay for NPLC power cycle (nplc/60Hz)
            self.instrument.write('waitcomplete()')
            print('Success')
            
        except:
            self.ShowAllErrors()

         
#---------Code Runs, Still needs testing
#Not tested exclusively yet.
#Doesn't fully make use of built in buffer as it tends to time out through python
         
    def startInputTrigger(self,ioport,mode,timeout):
        #ioport = raw_input('Enter IO port: ')
        #mode = raw_input('Enter mode: ')
        #timeout = raw_input('Enter timeout: ')
        #Change "smua" to whatever channel you decide to work on (smua or smub)
    
            dataArray =[]
    
            self.instrument.write('digio.trigger['+str(ioport)+'].mode = '+str(mode)) #sets the mode
            self.instrument.write('waitcomplete()')
            self.instrument.write('digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') # Sets the time out period
            self.instrument.write('waitcomplete()')
            print('Waiting for Trigger')
            #self.instrument.write('triggered = digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') #Checks if device detects the trigger
            #self.instrument.write('waitcomplete()')
            
            
            
            #Important note: all spaces required normally (e.g: triggered = digio.trigger)
            #Need to be kept in the str chunk for the code to work.
            #Each line of code is also seperated by a space
            #E.g if _____ do
            #        something
            #    end
            #should be written as ('if ____ do something end')
            
            
            #while loop, if triggered = true, measures and records, then waits to see if triggered = false or true
            self.instrument.write('while (digio.trigger['+str(ioport)+'].wait('+str(timeout)+')) == true do smua.measure.i(mybuffer) end')
            return            
            #self.instrument.write('while triggered == true do measure = smua.measure.i() waitcomplete() smua.measure.overlappedi(mybuffer) waitcomplete() triggered = nil rnum = rnum+1 triggered = digio.trigger['+str(ioport)+'].wait('+str(timeout)+') end')
            self.instrument.write('printbuffer(1,mybuffer.n, mybuffer.readings) waitcomplete()')

            dataArray.append((self.instrument.read()))#Writes the printed data to the array
            #probably in format of : "0235\n2346346\n" etc. May need further organizing
            #Confirmation: It is in unicode format just like above ^
            
            print('Operation Complete')
            self.instrument.write('print(mybuffer.n)') #Prints # of readings
            rnum = self.instrument.read() 
            print dataArray
            print ('Readings Taken: '+str(rnum)) # # reading message     
            
#Old Code, TOO SLOW-------            
            """dataArray = []
            self.instrument.write('digio.trigger['+str(ioport)+'].mode = '+str(mode)) #sets the mode
            self.instrument.write('waitcomplete()')
            self.instrument.write('digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') # Sets the time out period
            self.instrument.write('waitcomplete()')
            print('Waiting for Trigger')
            self.instrument.write('triggered = digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') #Checks if device detects the trigger
            self.instrument.write('waitcomplete()')   
            self.instrument.write('measure = smua.measure.i()')#Gets the Measurement
            self.instrument.write('waitcomplete()')  
            self.instrument.write('smua.measure.overlappedi(mybuffer)') #Stores the measurement to Buffer
            self.instrument.write('waitcomplete()')  
            self.instrument.write('print(triggered)') #prints response
            self.instrument.write('waitcomplete()')   
            trig = str(self.instrument.read())
            
            
            #self.instrument.write('if triggered == true then\n smua.measure.i(smua.mybuffer)\n print(mybuffer[1])\nelse\n print("Timed Out")')
            
            while (trig == 'true\n'):
                print('Trigger Detected.')
                self.instrument.write('measure = smua.measure.i()')#Gets the Measurement
                self.instrument.write('waitcomplete()')  
                self.instrument.write('smua.measure.overlappedi(mybuffer)') #Stores the measurement to Buffer
                self.instrument.write('waitcomplete()')   
                #data = float(self.instrument.read()) #Assigns last reading to variable
                #Probably dont need
                
                self.instrument.write('print(measure)') #print last measurement taken
                self.instrument.write('waitcomplete()')
                dataArray.append(float(self.instrument.read())) #Adds last printed message(measurement) to Array
                self.instrument.write('waitcomplete()')
                print('Reading added to buffer')
                
                #Repeat until false detected
                self.instrument.write('digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') # Sets the time out period
                self.instrument.write('waitcomplete()')
                self.instrument.write('triggered = digio.trigger['+str(ioport)+'].wait('+str(timeout)+')') #Checks if device detects the trigger
                self.instrument.write('waitcomplete()')    
                self.instrument.write('print(triggered)') #prints response
                self.instrument.write('waitcomplete()')   
            """ 
            #trig = str(self.instrument.read())

            #print('No Trigger Detected') #When false occurs
            #print dataArray #For testing if values are stored properly
            self.ShowAllErrors()
            
            
#--------------------------------------#

     
    def turnChannelOn(self,channel):
        #channel = raw_input("Enter Desired Channel(a or b) to turn on: ")
        smuX = 'smu' + str(channel)
        state = 2  #for testing, also make sures the default value of "0" isn't misinterpreted when debugging
        
        
        try:
            self.instrument.write('print('+str(smuX)+'.source.output)') #Requests the current status of the channel(0 is off, 1 is on)
            self.instrument.write('waitcomplete()')             
            state = float(self.instrument.read())
        
            if state == 0.0: #has to be 1.0 or 0.0 because keithley returns with 1 decimal
                self.instrument.write(str(smuX)+'.source.output = '+str(smuX)+'.OUTPUT_ON')
                self.instrument.write('waitcomplete()')
                print('Channel '+str(channel)+' turned on.')

        except:
            self.ShowAllErrors()
            
            
    def turnChannelOff(self,channel):
        #channel = raw_input("Enter Desired Channel(a or b) to turn off: ")
        smuX = 'smu'+str(channel)
        state = 2  #for testing, also make sures the default value of "0" isn't misinterpreted when debugging    
    
        try:
            self.instrument.write('print('+str(smuX)+'.source.output)')#Requests the current status of the channel(0 is off, 1 is on)
            self.instrument.write('waitcomplete()')             
            state = float(self.instrument.read())
        
            if state == 1.0: #has to be 1.0 or 0.0 because keithley returns with 1 decimal
                self.instrument.write(str(smuX)+'.source.output =' +str(smuX) +'.OUTPUT_OFF')
                self.instrument.write('waitcomplete()')
                print('Channel '+str(channel)+' turned off.')

        except:
            self.ShowAllErrors()
    
    def clearBuffer(self,channel,buff):
        #channel = raw_input("Enter Channel(a or b) to clear buffer: ")
        #buff = raw_input("Enter which Buffer to clear(1 or 2): ")
        smuX = 'smu'+str(channel)
        buffX = 'nvbuffer'+str(buff)
        
        if (channel=='a') or (channel =='b'):
            if (buff == 1) or (buff == 2):
                self.instrument.write(str(smuX)+'.'+str(buffX)+'.clear()')
                self.instrument.write('waitcomplete()')             
                self.instrument.write(str(smuX)+'.'+str(buffX)+'.appendmode = 1')
                self.instrument.write('waitcomplete()')             
                self.instrument.write(str(smuX)+'.measure.count = 1')
                self.instrument.write('waitcomplete()')             
                print ('Channel '+str(channel)+' buffer '+str(buff)+' cleared.')
            
            else:
                self.instrument.write(str(smuX)+'.'+str(buffX)+'.clear()')#To create the error to display
                self.instrument.write('waitcomplete()') 
                self.ShowAllErrors()
            
        else:
            self.instrument.write(str(smuX)+'.'+str(buffX)+'.clear()')#To create the error to display
            self.instrument.write('waitcomplete()') 
            self.ShowAllErrors()
    
    def logVoltage(self,channel,buff):
        #channel = raw_input('Choose a Channel(a or b): ') 
        #buff = raw_input('Choose a buffer(1 or 2): ')
        smuX = 'smu'+str(channel)
        buffX = 'nvbuffer'+str(buff)
        
        if (channel=='a') or (channel =='b'):
            if (buff == 1) or (buff == 2):
                self.instrument.write(str(smuX)+'.measure.v('+str(smuX)+'.'+str(buffX)+')') #Command to measure voltage, stores in designated buffer
                self.instrument.write('waitcomplete()')
                print ('Voltage Logged.')
            
            else:
                self.instrument.write(str(smuX)+'.measure.v('+str(smuX)+'.'+str(buffX)+')') #To create the error to display
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()

                
        else:
            self.instrument.write(str(smuX)+'.measure.v('+str(smuX)+'.'+str(buffX)+')')
            self.instrument.write('waitcomplete()') 
            self.ShowAllErrors()

    
    def logCurrent(self,channel,buff):
        #channel = raw_input('Choose a Channel(a or b): ') 
        #buff = raw_input('Choose a buffer(1 or 2): ')
        smuX = 'smu'+str(channel)
        buffX = 'nvbuffer'+str(buff)
        
        if (channel=='a') or (channel =='b'):
            if (buff == 1) or (buff == 2):
                self.instrument.write(str(smuX)+'.measure.i('+str(smuX)+'.'+str(buffX)+')') #Command to measure Current, stores in designated buffer
                self.instrument.write('waitcomplete()')
                print ('Current Logged.')
            
            else:
                self.instrument.write(str(smuX)+'.measure.i('+str(smuX)+'.'+str(buffX)+')') #To create the error to display
                self.instrument.write('waitcomplete()')
                self.ShowAllErrors()
        
        else:
            self.instrument.write(str(smuX)+'.measure.i('+str(smuX)+'.'+str(buffX)+')')
            self.instrument.write('waitcomplete()') 
            self.ShowAllErrors()

    #Returns the varaible 'data' which contains all the measurements from channel X
    #nPoints is the number of measurements from the internal buffer
    #should store to a file 'data' or something
    def getLoggedData(self,channel,buff,nPoints):
        #channel = raw_input('Choose a Channel(a or b): ') 
        #buff = raw_input('Choose a buffer(1 or 2): ')
        #nPoints = raw_input('Enter how many points desired: ')
        smuX = 'smu'+str(channel)
        buffX = 'nvbuffer'+str(buff)

        try:
            #check if output of Channel x is OFF
            self.instrument.write('print('+str(smuX)+'.source.output)')
            self.instrument.write('waitcomplete()')             
            state = int(self.instrument.read())
        
            if state == 1: #if channel is on, turn it off before downloading the data
                self.instrument.write(str(smuX)+'.source.output='+str(smuX)+'.OUTPUT_OFF')
                self.instrument.write('waitcomplete()') 
                
            self.instrument.write('printbuffer(1,'+str(nPoints)+','+str(smuX)+'.'+str(buffX)+'.readings)')
            self.instrument.write('waitcomplete()')
        
            data = float(self.instrument.read())
            print data
            
        except:
            self.ShowAllErrors()

    def setCurrent(self,channel,i):
        #channel = raw_input('Choose a Channel(a or b): ') 
        #i = input('Enter amps(Max: 3): ')
        smuX = 'smu'+str(channel)
        self.instrument.write('display.'+str(smuX)+'.measure.func = 0') #Switches display on keithley to show whats happening
        self.instrument.write('waitcomplete()')     
    
        #Check if channel output is On and if the source is set to output a current
        try:
            self.instrument.write('print('+str(smuX)+'.source.output)') #returns the current source output, tells if channel is on or off
            self.instrument.write('waitcomplete()')
            state = float(self.instrument.read())
            #print state
            
            self.instrument.write('print('+str(smuX)+'.source.func)') #returns the current source function, DCAMPS, DCVOLTS, OHMS, or watts
            self.instrument.write('waitcomplete()')
            source = float(self.instrument.read())  #(0:DCAMPS, 1: VOLTS)
            #print source
        
            #if output is off, turn it on before setting the current
            if state == 0.0:
                self.instrument.write(str(smuX)+'.source.output ='+str(smuX)+'.OUTPUT_ON') #Turn on channel X output
                self.instrument.write('waitcomplete()')
                
            #if source is set to DCVOLTS, set it to DCAMPS before setting the current
            #could re-write this as, "if not DCAMPS, set to DCAMPS, instead of having a requirement of it being DCVOLTS first    
            if source == 1.0:
                self.instrument.write(str(smuX)+'.source.output =' +str(smuX)+'.OUTPUT_OFF') #Turn off channel X output
                self.instrument.write('waitcomplete()')
                self.instrument.write(str(smuX)+'.source.func = 0')#sets source to output current
                self.instrument.write('waitcomplete()')
                self.instrument.write(str(smuX)+'.source.output =' +str(smuX)+'.OUTPUT_ON')#Turn on channel X output again
                self.instrument.write('waitcomplete()')

            #-----Set Current i-----    
            self.instrument.write(str(smuX)+'.source.leveli =' +str(i)) #set current of channel X  
            self.instrument.write('waitcomplete()')             
            print('Current has been set successfully.')
        
        except:
            self.ShowAllErrors()

    def setVoltage(self,channel,v):
        #channel = raw_input('Choose a Channel(a or b): ') 
        #v = input('Enter volts(Max: 30): ')
        smuX = 'smu'+str(channel)
        self.instrument.write('display.'+str(smuX)+'.measure.func = 1') #Changes display to show user what is happening
        self.instrument.write('waitcomplete()') 
        
        #Check if channel output is On and if the source is set to output a current
        try:
            self.instrument.write('print('+str(smuX)+'.source.output)')
            self.instrument.write('waitcomplete()')             
            state = float(self.instrument.read())   
            self.instrument.write('print('+str(smuX)+'.source.func)')    
            self.instrument.write('waitcomplete()')             
            source = float(self.instrument.read())  #(0:DCAMPS, 1: VOLTS)

            #if output is off, turn it on before setting the current
            if state == 0.0:
                self.instrument.write(str(smuX)+'.source.output ='+str(smuX)+'.OUTPUT_ON') #Turn on channel X output
                self.instrument.write('waitcomplete()')
        
            #if source is set to DCAMPS, set it to DCVOLTS before setting the voltage
            if source == 0.0:
                self.instrument.write(str(smuX)+'.source.output =' +str(smuX)+'.OUTPUT_OFF') #Turn off channel X output
                self.instrument.write('waitcomplete()')
                self.instrument.write(str(smuX)+'.source.func = 1')#sets source to output voltage
                self.instrument.write('waitcomplete()')
                self.instrument.write(str(smuX)+'.source.output =' +str(smuX)+'.OUTPUT_ON')#Turn on channel X output again
                self.instrument.write('waitcomplete()')
            
            #-----Set Voltage v-----    
            self.instrument.write(str(smuX)+'.source.levelv =' +str(v)) #set voltage source of channel X
            self.instrument.write('waitcomplete()')   
            print('Voltage has been set successfully.')
            
        except:
            self.ShowAllErrors()
    
    def getCurrent(self,channel):
        #channel = raw_input('Choose a Channel(a or b): ') 
        smuX = 'smu'+str(channel)   
        try:
            self.instrument.write('print('+str(smuX)+'.measure.i())') #asks machine to take a measurement
            self.instrument.write('waitcomplete()')
            current = float(self.instrument.read())
            #print current
            return current
            
        except:
            self.ShowAllErrors()
        
    def getVoltage(self,channel):
        #channel = raw_input('Choose a Channel(a or b): ') 
        smuX = 'smu'+str(channel)   
            
        try:  
            self.instrument.write('print('+str(smuX)+'.measure.v())') #asks machine to take a measurement
            self.instrument.write('waitcomplete()')            
            voltage = float(self.instrument.read())
            #print voltage
            return voltage
            
        except:
            self.ShowAllErrors()

   
#Used for Debgging. If more errors occured than expected. Disable the error part of the function, add a 'pass'
#then run this script. 
#This script will list out all the errors in queue before clearing them.             
    def ShowAllErrors(self):
        self.instrument.write('print(errorqueue.count)')
        self.instrument.write('waitcomplete()') 
        ErrorNum = int(float(self.instrument.read()))
        print ('Errors in Queue: '+str(ErrorNum))
        #print ErrorNum
        
        if ErrorNum == 0:
            self.instrument.write('errorqueue.clear()')#clears error queue
            self.instrument.write('waitcomplete()')
            print 'There are no errors.'
        else:
            errorStr = '';
            while (ErrorNum > 0):
                self.instrument.write('errorcode,message = errorqueue.next()')
                self.instrument.write('waitcomplete()')             
                self.instrument.write('print(errorcode, message)') #Gets error from keithley
                self.instrument.write('waitcomplete()')
                errorStr = '\n'+ errorStr+self.instrument.read().encode('ascii','replace')
                self.instrument.write('waitcomplete()')
                ErrorNum = ErrorNum - 1          
                
            self.instrument.write('errorqueue.clear()')#clears error queue
            self.instrument.write('waitcomplete()')   
            print 'All Errors Displayed. Error Queue Cleared.'
            raise InstrumentError(errorStr)
        
class InstrumentError(Exception):
    pass;