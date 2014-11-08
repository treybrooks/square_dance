
# coding: utf-8

# In[1]:

def set_pixel(df, x, y, color):
    df[x,y,0] = color[0]
    df[x,y,1] = color[1]
    df[x,y,2] = color[2]
    return df


# In[2]:

def draw_line(df, x1, y1, x2, y2, color):
    if x1 > 15:
        x1 = 15
    elif x1 < 0:
        x1 = 0
        
    if x2 > 15:
        x2 = 15
    elif x2 < 0:
        x2 = 0
        
    if y1 > 15:
        y1 = 15
    elif y1 < 0:
        y1 = 0
        
    if y2 > 15:
        y2 = 15    
    elif y2 < 0:
        y2 = 0

    dx = abs(x2-x1)+1
    dy = abs(y2-y1)+1
    d = [dx,dy]
    
    xpoints = [int(round(p)) for p in np.linspace(x1, x2, max(d))]
    ypoints = [int(round(p)) for p in np.linspace(y1, y2, max(d))]
       
    for i in range(len(xpoints)):
        x = xpoints[i]
        y = ypoints[i]
        df = set_pixel(df, x, y, color)
    
    return df


# In[3]:

def draw_square(df, center, size, color):
    # draw right line
    df = draw_line(df, center[0]-size/2+1, center[1]+size/2,   center[0]+size/2,   center[1]+size/2,   color)
    # draw bottom line
    df = draw_line(df, center[0]+size/2,   center[1]+size/2-1, center[0]+size/2,   center[1]-size/2+1, color)
    # draw left line
    df = draw_line(df, center[0]-size/2+1, center[1]-size/2+1, center[0]+size/2,   center[1]-size/2+1, color)
    # draw top line
    df = draw_line(df, center[0]-size/2+1, center[1]+size/2,   center[0]-size/2+1, center[1]-size/2+1, color)
    return df


# In[4]:

def draw_filled_square(df, center, size, color):
    for i in range(size):
        df = draw_line(df, center[0]-size/2+1+i, center[1]+size/2, center[0]-size/2+1+i, center[1]-size/2+1, color)
    return df


# In[5]:

def convert_array(arr):
    arr = arr.tostring()
    try:
        iter(arr[0])
        arr = list(chain.from_iterable(arr))
    except TypeError:
        pass
    data = list('DANCEFLOOR') + [1] + arr
    
    return bytearray(data)


# In[6]:

class InvalidData(Exception):
    pass

def validate_array(arr):
    size = 16*16
    if not len(arr) in (size, size * 3):
        raise InvalidData('array must be length 64 or 192')
    if len(arr) == size:
        for el in arr:
            if len(el) != 3:
                raise InvalidData('Element %s not length 3' % el)
            for i in el:
                if not 255 >= i >= 0:
                    raise InvalidData('Invalid RGB value %s', str(i))


# In[7]:

def df_write(data):
    LATCH = bytearray(list('DANCEFLOOR') + [2])
    
    h = len(data)
    w = len(data[1])
    data0 =  [data[i][:h / 2] for i in range(w / 2)] # top_left
    data1 = [data[i][h / 2:] for i in range(w / 2)] # top_right
    data2 =  [data[i][:h / 2] for i in range(w / 2, w)] # bot_left
    data3 = [data[i][h / 2:] for i in range(w / 2, w)] # bot_right
    
    sock.sendto(convert_array(np.asarray(data0)),(u1,port))
    sock.sendto(convert_array(np.asarray(data1)),(u2,port))
    sock.sendto(convert_array(np.asarray(data2)),(u3,port))
    sock.sendto(convert_array(np.asarray(data3)),(u4,port))
    
    #Latch frame
    sock.sendto(LATCH,(u1,port))
    sock.sendto(LATCH,(u2,port))
    sock.sendto(LATCH,(u3,port))
    sock.sendto(LATCH,(u4,port))


# In[10]:

# setup block

from itertools import chain 
import socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
port = 21337

u1 = '10.0.0.5'
u2 = '10.0.0.3'
u3 = '10.0.0.4'
u4 = '10.0.0.6'
# 10.0.0.6	54:55:58:44:46:34	DF4
# 3	10.0.0.5	54:55:58:44:46:31	DF1
# 4	10.0.0.4	54:55:58:44:46:33	DF3
# 5	10.0.0.3	54:55:58:44:46:32	DF2


# Define basic colors
pink   = [200,25,25]
red    = [255,0,0]

orange = [255,128,0]
yellow = [255,255,0]

green  = [0,255,0]
turq   = [0,200,200]
blue   = [0,0,255]
purple = [150,20,102]

black  = [0,0,0]


# the HULK
rich_purple = [123,50,148]
med_purple  = [194,165,207]
white       = [247,247,247]
med_green   = [166,219,160]
dark_green  = [0,136,55]
the_hulk = [rich_purple, med_purple, white, med_green, dark_green]


# halloween
halloween = [green, orange, black, purple]

# color Sea themed colors
under_the_sea = [turq, blue, green, purple]

schemes = [the_hulk, halloween, under_the_sea]

# Create dancefloor matrix
df = np.zeros((16,16,3), dtype=np.uint8)


# Frames per second
fps = 10.

# df[:,1,0] = 255
# df[:,4,1] = 255
# df[:,7,2] = 255

from random import randint, choice
from time import sleep

frames = []
debug = False

ROWS = 16
COLS = 16
max_dim = max([ROWS,COLS])

# Floor loop
# for dummy in range(50):
while True:
    color_list = choice(schemes)
    for dummy in xrange(5000):
        operation = randint(0,5) # half the time, it won't add anything

        if operation == 0:
            if debug: print 'square'
            size = randint(3, max_dim-2)
            center = [randint(2,ROWS-1), randint(2,COLS-1)]
            color = choice(color_list)
    #         print center, size, color
            df = draw_square(df, center, size, color)

        elif operation == 1:
            if debug: print 'full square'
            size = randint(3, max_dim/3)
            center = [randint(2,ROWS-1), randint(2,COLS-1)]
            color = choice(color_list)
    #         print center, size, color
            df = draw_filled_square(df, center, size, color)

        else:
            if debug: print 'none'

        xshift = randint(-1,1)
        yshift = randint(-1,1)
        if xshift == 0 and yshift == 0:
                xshift = 1

        for i in range(randint(10,20)):
            df = np.roll(df, xshift, axis=1)
            df = np.roll(df, yshift, axis=0)
    #         frames.append(df)
            df_write(df)
            sleep(1/fps)


# In[ ]:

from random import random, choice, randint
from time import sleep 

rich_purple = [123,50,148]
med_purple  = [194,165,207]
white       = [247,247,247]
med_green   = [166,219,160]
dark_green  = [0,136,55]
color_list = [rich_purple, med_purple, white, med_green, dark_green]

fps = 10

# Create dancefloor matrix
df = np.zeros((16,16,3), dtype=np.uint8)

ROWS =16
COLS =16
max_dim =16

p = 0.5
boxes = []
debug = False

for dummy in range(100):
    
    ran = random()
    if ran > p:
        boxes.append(choice([Box('square'), Box('filled_square')]))
        if debug: print 'added: ', boxes[-1]

    for pattern in boxes:
        if pattern.life >= 0:
            df = pattern.draw(df)
            pattern.weaken()
        else:
            if debug: print 'Removing: ', boxes[-1]
            boxes.remove(pattern)
        
    # shift that shit around and make it pretty (any non-zero velocity)
    xshift, yshift = choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
    for i in range(randint(10,20)):
        df = np.roll(df, xshift, axis=1)
        df = np.roll(df, yshift, axis=0)
        df_write(df)
        sleep(1/fps)


# In[41]:

from datetime import datetime, timedelta

class SquareDance():
    def __init__(self, color_list, life_span, debug=False):
        self.life = 0
        self.birth_time = 0 # datetime.now()
        self.death_time = 200+life_span # datetime.now()+life_span
        self.df = np.zeros((16,16,3), dtype=np.uint8)
        self.boxes = []
        self.debug = debug
        self.fps = 2
        self.p = 0.5
        
    def run(self):
        while self.life <= self.death_time:
            ran = random()
            
            while len(self.boxes) < 3:
                self.boxes.append(choice([Box('square'), Box('filled_square')]))
                if self.debug: print 'added: ', self.boxes[-1]
            
            if ran > self.p:
                self.boxes.append(choice([Box('square'), Box('filled_square')]))
                if self.debug: print 'added: ', self.boxes[-1]

            for pattern in self.boxes:
                if pattern.life >= 0:
                    df = pattern.draw(self.df)
                    pattern.weaken()
                else:
                    if self.debug: print 'Removing: ', self.boxes[-1]
                    self.boxes.remove(pattern)

            # shift that shit around and make it pretty (any non-zero velocity)
            xshift, yshift = choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
            for i in range(randint(10,20)):
                self.df = np.roll(self.df, xshift, axis=1)
                self.df = np.roll(self.df, yshift, axis=0)
                for box in self.boxes:
                    box.update([xshift, yshift])
                df_write(self.df)
                sleep(1/self.fps)            
            
            self.life += 1
        
#         self.terminate()
        
    def terminate(self):
        while len(self.boxes) > 1:
            xshift, yshift = choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
            for i in range(randint(10,20)):
                self.df = np.roll(self.df, xshift, axis=1)
                self.df = np.roll(self.df, yshift, axis=0)
                for box in self.boxes:
                    box.update([xshift, yshift])
                df_write(self.df)
                sleep(1/self.fps)
        return False
        


# In[42]:

from operator import add

class Box():
    def __init__(self, kind):
        self.center = [randint(2,ROWS-1), randint(2,COLS-1)]
        self.color = choice(color_list)
        self.kind = kind
        if self.kind == 'square':
            self.size = randint(3, max_dim-2)
        elif self.kind == 'filled_square':
            self.size = randint(3, max_dim/3)
        self.life = 10
            
    def __str__(self):
        ret_str = ''
        ret_str += self.kind+':\n'
        ret_str += '    Size: '  +str(self.size)  +'\n'
        ret_str += '    Center: '+str(self.center)+'\n'
        ret_str += '    Color: ' +str(self.color) +'\n'
        return ret_str
        
    def draw(self, df):
        if self.kind == 'square':
            return draw_square(df, self.center, self.size, self.color)
        elif self.kind == 'filled_square':
            return draw_filled_square(df, self.center, self.size, self.color)
        
    def update(self, shifts):
        self.center = map(add, self.center, shifts)
        
    def weaken(self):
        self.life -= 1


# In[43]:

# setup block

from itertools import chain 
import socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
port = 21337

u1 = '192.168.1.101'
u2 = '192.168.1.102'
u3 = '192.168.1.103'
u4 = '192.168.1.104'



# In[44]:

from random import choice, random
from time import sleep 

# Define basic colors
pink   = [200,25,25]
red    = [255,0,0]

orange = [255,128,0]
yellow = [255,255,0]

green  = [0,255,0]
turq   = [0,200,200]
blue   = [0,0,255]
purple = [150,20,102]

black  = [0,0,0]


# the HULK
rich_purple = [123,50,148]
med_purple  = [194,165,207]
white       = [247,247,247]
med_green   = [166,219,160]
dark_green  = [0,136,55]
the_hulk = [rich_purple, med_purple, white, med_green, dark_green]


# halloween
halloween = [green, orange, black, purple]

# color Sea themed colors
under_the_sea = [turq, blue, green, purple]

schemes = [the_hulk, under_the_sea, halloween]

ROWS = 16
COLS = 16
max_dim = max([ROWS, COLS])
# Lets get this party started!!!
while True:
    color_list = choice(schemes)
    life_span  = 500 # timedelta(0,60*2)
    sq = SquareDance(color_list, life_span)
    sq.run()


# In[40]:

del sq


# In[13]:




# In[ ]:



