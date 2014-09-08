
# coding: utf-8

# In[ ]:

# #Define basic colors
# red = [255,0,0]
# green = [0,255,0]
# blue = [0,0,255]
# yellow = [255,255,0]
# orange = [255,8*16,0]
# white = [255,255,255]
# purple = [92,53,102]

# colorArr = [red,green,blue,yellow,orange,white,purple]

# ### df_init()


# # Create dancefloor matrix
# import numpy as np
# df = np.zeros((16,16,3), dtype=np.uint8))


# # %Frames per second
# fps = 10

# df[:,1,1] = 255;
# df[:,4,2] = 255;
# df[:,7,3] = 255;


# # %Floor loop
# while True:
    
#     operation = random('unid',5);
    
#     switch(operation)
        
#         case 1
#             size = random('unid',15)+1;
#             center = [random('unid',5)+2,random('unid',6)+1];
            
#             color = colorArr(random('unid',length(colorArr)),:);
            
#             df = drawSquare(df, center, size, color);
            
        
#         case 2%concentric squares
#            % df = drawSquare(df, center, size, color);
            
#         case 3
#             size = random('unid',4)+2;
#             center = [random('unid',5)+2,random('unid',6)+1];
            
#             color = colorArr(random('unid',length(colorArr)),:);
            
#             df = drawFilledSquare(df, center, size, color);
            
#     end
    
#         xshift = random('unid',3)-2;
#         yshift = random('unid',3)-2;
#         %The number of times to do the operation
#     for i=1:random('unid',5)+15
            

#         if (xshift == 0) && (yshift == 0)
#             xshift = 1;
#         end
#         df = circshift(df, [xshift, yshift]);
#         df_write();
#         pause(1/fps)



# In[ ]:




# In[ ]:

def set_pixel(df, x, y, color):
    df_copy = df
    for c in range(len(color)):
        df_copy[x, y, c] = color[c]
    return df_copy


# In[ ]:

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i


# In[ ]:

def draw_line(df, x1, y1, x2, y2, color):
    if x1 > 16:
        x1 = 16
    if x1 < 1:
        x1 = 1
        
    if x2 > 16:
        x2 = 16
    if x2 < 1:
        x2 = 1
        
    if y1 > 16:
        y1 = 16
    if y1 < 1:
        y1 = 1
        
    if y2 > 16:
        y2 = 16    
    if y2 < 1:
        y2 = 1
        
    dx = abs(x2-x1)+1
    dy = abs(y2-y1)+1
    d = [dx,dy]
    
    xpoints = round(linspace(x1,x2,max(d)))
    ypoints = round(linspace(y1,y2,max(d)))
    
    for i in xpoints:
         df = setPixel(df, xpoints[i],ypoints[i],color)
    
    return df


# In[ ]:

def drawSquare(df, center, size, color):
    # draw right line
    df = drawLine(df, center[0]-size/2+1, center[1]+size/2, center{0}+size/2, center[1]+size/2, color)
    # draw bottom line
    df = drawLine(df, center[0]+size/2, center[1]+size/2-1, center[0]+size/2, center[1]-size/2+1, color)
    # draw left line
    df = drawLine(df, center[0]-size/2+1, center[1]-size/2+1, center[0]+size/2, center[1]-size/2+1, color)
    # draw top line
    df = drawLine(df, center[0]-size/2+1, center[1]+size/2, center[0]-size/2+1, center[1]-size/2+1, color)
    return df


# In[ ]:

def drawFilledSquare(df, center, size, color):
    for i in range(size):
        df = drawLine(df, center[0]-size/2+1+i, center[1]+size/2, center[0]-size/2+1+i, center[1]-size/2+1, color)
    return df

