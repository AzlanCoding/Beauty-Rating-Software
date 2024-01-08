import pygame
import facial_keypoints_detecter as fkd
import matplotlib.pyplot as plt
import cv2
from torchvision.utils import save_image
import torch
import numpy as np
import xlsxwriter
from PIL import Image
import shutil
from time import time
import os
def resize(path, basewidth):
    #basewidth = 300
    if not os.path.exists('./xlsxCache/'):
        os.makedirs('./xlsxCache/')
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.LANCZOS)
    #imgFormat = path.split("/")[0]
    imgFormat = path.split(".")[-1]
    imgPath = './xlsxCache/' + str(time()).replace(".","") +"."+ imgFormat
    img.save(imgPath)
    return imgPath

def clearCache():
    if os.path.exists('./xlsxCache/'):
        shutil.rmtree('./xlsxCache')

pygame.init()
def FacialKeyPointEditor(img_path):
    DEFAULT_FIGSIZE,DEFAULT_PREPROCESS_SIZE_RANDOMCROP,DEFAULT_PREPROCESS_SIZE_RANDOMCROP,DEFAULT_PREPROCESS_SCALING_SQRT,DEFAULT_PREPROCESS_SCALING_MEAN = (3.33, 224, 224, 50.0, 100.0)
    def getxy(file_image
            , file_model   = "default"
              ):
        figsizeScale = DEFAULT_FIGSIZE
        faces = net.apps.detect_faces(file_image)
        print(faces[0].tolist())

        # Loading in color image for face detection >>
        image_bgr = cv2.imread(file_image)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        '''# Loading model if file_model is provided >>
        if file_model != "default":
            self.load_model(file_model)
        # else:
        #     self.load_model(DEFAULT_FILE_FKD_NET_MODEL)
        self.eval()'''

        image = np.copy(image_rgb)

        # Including a padding to extract face as HAAR classifier's bounding box, crops sections of the face
        images, keypoints = [], []

        # Looping over the detected faces >>
        len_faces = len(faces)
        fig, axes = plt.subplots(1, len_faces, figsize = (len_faces*figsizeScale*DEFAULT_FIGSIZE, figsizeScale*DEFAULT_FIGSIZE))

        for i, (x,y,w,h) in enumerate(faces):
            #print([x,y,w,h]) xyWidhtHeight of box to detect face

            # Selecting the region of interest that is the face in the image >>
            helf_width_roi = int(max(w,h)*0.35)
            # roi = image[ max(y-padding, 0) : y+h+padding
            #            , max(x-padding, 0) : x+w+padding ]

            roi = image[ max(y-helf_width_roi, 0) : y+h+helf_width_roi
                       , max(x-helf_width_roi, 0) : x+w+helf_width_roi ]

            # Rescaling the detected face to be the expected square size for CNN >>
            roi_rescaled = cv2.resize(roi, (DEFAULT_PREPROCESS_SIZE_RANDOMCROP, DEFAULT_PREPROCESS_SIZE_RANDOMCROP))

            # Converting the face region from RGB to grayscale >>
            roi_gray = cv2.cvtColor(roi_rescaled, cv2.COLOR_RGB2GRAY)

            # Normalizing the grayscale image so that its color range falls in [0,1] instead of [0,255] >>
            roi_normed     = (roi_gray     / 255.0 ).astype(np.float32)
            roi_normed_rgb = (roi_rescaled / 255.0 ).astype(np.float32)

            # Reshaping the numpy image shape (H x W x C) into a torch image shape (C x H x W) >>
            roi = roi_normed
            if len(roi.shape) == 2:
                roi = roi.reshape(roi.shape[0], roi.shape[1], 1)
            roi_transposed     = roi.transpose((2, 0, 1))
            roi_transposed_rgb = roi_normed_rgb

            # Converting to torch array >>
            roi_torch     = torch.from_numpy(roi_transposed)
            roi_torch_rgb = torch.from_numpy(roi_transposed_rgb)
            images.append(roi_torch_rgb)
            output_pts = net.forward(roi_torch)
            keypoints.append(output_pts)

            # Displaying each detected face and the corresponding keypoints >>
            #if plot_enabled:
            # plot_output(roi_torch, output_pts)
            axes_curr = axes if len_faces == 1 else axes[i]
            key_pts_pred = output_pts.data
            key_pts_pred = key_pts_pred.numpy()
            # Undoing normalization of keypoints >>
            key_pts_pred = key_pts_pred[0]*DEFAULT_PREPROCESS_SCALING_SQRT + DEFAULT_PREPROCESS_SCALING_MEAN
            #print(key_pts_pred.tolist())
            #print(dir(key_pts_pred))
                #plot_keypoints(image = roi_transposed_rgb, keypoints_pred = key_pts_pred, cmap = "gray", axes = axes_curr)

        #plt.show()
        plt.close()
        return roi_transposed_rgb, key_pts_pred.tolist()

    #img_path = './Trash/Iman/Camera.png'
    net = fkd.model.Net()
    net.load_model('saved_model_facial_keypoints_detector.pt')
    image, data = getxy(img_path)
    xPlots = []
    yPlots = []

    im = Image.fromarray((image*255).astype(np.uint8))
    im.save("FacialKeypointEditorCache.png")

    screen = pygame.display.set_mode((700,700), pygame.RESIZABLE)
    #print(pygame.display.get_driver())
    pygame.display.set_caption('Facial Keypoint Editor')
    pygame.display.flip()
    face = net.apps.detect_faces("FacialKeypointEditorCache.png").tolist()[0]
    data.append([face[0]+(face[2]/2),face[1]])
    for items in data:
        #print(items)
        xPlots.append(items[0])
        yPlots.append(items[1])
    #print(face)
    imgy = pygame.image.load("FacialKeypointEditorCache.png")
    Zoom = 200
    zoomX = imgy.get_width()/100*Zoom
    zoomY = imgy.get_width()/100*Zoom
    img1 = pygame.transform.scale(imgy,(zoomX,zoomY))




    for items in data:
        pass

    color = (255,0,0)
    color2 = (0,0,255)

    # Variable to keep our game loop running
    running = True

    offsetX = 0
    offsetY = pygame.display.get_surface().get_size()[1]*0.1

    mouseOrigin = []

    def drawMenu(zoom):
        w, h = pygame.display.get_surface().get_size()
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(0,0,w, h*0.1))
        font = pygame.font.Font('freesansbold.ttf', 20)
        zoomBtnW, zoomBtnH = font.size("ResetZoom")
        pygame.draw.rect(screen, (255,0,0), pygame.Rect((w*0.15)-(zoomBtnW/1.5),(h*0.1*0.5)-(zoomBtnH/1.5),zoomBtnW*1.35, zoomBtnH*1.5))
        zoomBtn = font.render("Reset Zoom",True,(255,255,255))
        zoomRect = zoomBtn.get_rect()
        zoomRect.center = (w*0.15,h*0.1*0.5)
        screen.blit(zoomBtn,zoomRect)
        saveBtnW, saveBtnH = font.size("Save")
        pygame.draw.rect(screen, (0,255,0), pygame.Rect((w*0.35)-(saveBtnW/1.5),(h*0.1*0.5)-(saveBtnH/1.5),saveBtnW*1.35, saveBtnH*1.5))
        saveBtn = font.render("Save",True,(255,255,255))
        saveRect = saveBtn.get_rect()
        saveRect.center = (w*0.35,h*0.1*0.5)
        screen.blit(saveBtn,saveRect)
        ZoomW, ZoomH = font.size("Zoom: "+str(zoom)+"%")
        Zoom = font.render("Zoom: "+str(zoom)+"%",True,(255,255,255))
        ZoomRect = Zoom.get_rect()
        ZoomRect.center = (ZoomW/2,ZoomH/2)
        screen.blit(Zoom,ZoomRect)
        return pygame.Rect((w*0.15)-(zoomBtnW/1.5),(h*0.1*0.5)-(zoomBtnH/1.5),zoomBtnW*1.35, zoomBtnH*1.5), pygame.Rect((w*0.35)-(saveBtnW/1.5),(h*0.1*0.5)-(saveBtnH/1.5),saveBtnW*1.35, saveBtnH*1.5)


        
        
        
      
    # game loop
    while running:
        font = pygame.font.Font('freesansbold.ttf', round(3/100*Zoom))
        screen.blit(img1, (offsetX, offsetY))
        pygame.draw.rect(screen, color, pygame.Rect(face[0]/100*Zoom+offsetX,face[1]/100*Zoom+offsetY,face[2]/100*Zoom,face[3]/100*Zoom),  5)
        if pygame.mouse.get_pressed()[1]:
            if mouseOrigin == []:
                mouseOrigin = [0,0]
                mouseOrigin[0], mouseOrigin[1] = pygame.mouse.get_pos()
                mouseOrigin[0] -= offsetX
                mouseOrigin[1] -= offsetY
            else:
                x, y = pygame.mouse.get_pos()
                offsetX = x - mouseOrigin[0]
                offsetY = y - mouseOrigin[1]
        else:
            mouseOrigin = []
        count = 1
        for point in data:
            text = font.render(str(count), True, color2)
            text_width, text_height = font.size(str(count))
            xPlot = point[0]/100*Zoom +offsetX
            yPlot = point[1]/100*Zoom +offsetY
            Radius = 1/100*Zoom
            textRect = text.get_rect()
            textRect.center = (xPlot-text_width,yPlot-text_height)
            screen.blit(text, textRect)
            x, y = pygame.mouse.get_pos()
            if (x > (xPlot - Radius)) and (x < (xPlot + Radius)) and (y > (yPlot - Radius)) and (y < (yPlot + Radius)):
                pygame.draw.circle(screen, color2, (xPlot,yPlot),Radius+1)
                while pygame.mouse.get_pressed()[0]:
                    screen.fill((0,0,0))
                    x, y = pygame.mouse.get_pos()
                    x -= offsetX
                    y -= offsetY
                    point[0]= x/Zoom*100
                    point[1]= y/Zoom*100
                    screen.blit(img1, (offsetX, offsetY))
                    text = font.render(str(count), True, color2)
                    text_width, text_height = font.size(str(count))
                    xPlot = point[0]/100*Zoom +offsetX
                    yPlot = point[1]/100*Zoom +offsetY
                    Radius = 1/100*Zoom
                    textRect = text.get_rect()
                    textRect.center = (xPlot-text_width,yPlot-text_height)
                    screen.blit(text, textRect)
                    pygame.draw.circle(screen, color2, (xPlot,yPlot),Radius+3)
                    drawMenu(Zoom)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        # Check for QUIT event      
                        if event.type == pygame.QUIT:
                            running = False
                    
                    
            else:
                pygame.draw.circle(screen, color2, (xPlot,yPlot),Radius)
            count += 1
        zoomBtn, saveBtn = drawMenu(Zoom)
        if zoomBtn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            Zoom = 200
            offsetX = 0
            offsetY = pygame.display.get_surface().get_size()[1]*0.1
            zoomX = imgy.get_width()/100*Zoom
            zoomY = imgy.get_width()/100*Zoom
            screen.fill((0,0,0))
            img1 = pygame.transform.scale(imgy,(zoomX,zoomY))
        elif saveBtn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            running = False
        else:
            pygame.display.flip()
        
    # for loop through the event queue  
        for event in pygame.event.get():
            screen.fill((0,0,0))
          
            # Check for QUIT event      
            if event.type == pygame.QUIT:
                running = False

            # Chck for scrollWheel
            if event.type == pygame.MOUSEWHEEL:
                Zoom += event.y*10
                zoomX = imgy.get_width()/100*Zoom
                zoomY = imgy.get_width()/100*Zoom
                img1 = pygame.transform.scale(imgy,(zoomX,zoomY))
    pygame.display.quit()
    os.remove("FacialKeypointEditorCache.png")
    xPlots = []
    yPlots = []
    for items in data:
        #print(items)
        xPlots.append(items[0])
        yPlots.append(items[1])
    fig, ax = plt.subplots()
    ax.imshow(image, extent=[0, 223.5, 223.5, 0], cmap="gray")
    plt.scatter(xPlots,yPlots)
    plt.show()
    return image, data


# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('Output.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()
worksheet.set_default_row(hide_unused_rows=True)
worksheet.set_cols.setdefault(1)

# Use the worksheet object to write
# data via the write() method.
heading_format = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter'})
data_format = workbook.add_format({
    'align': 'left',
    'valign': 'vcenter'})
data_format.set_text_wrap()
worksheet.merge_range('A1:A2', 'Name', heading_format)
worksheet.merge_range('B1:B2', 'Original Image', heading_format)
worksheet.merge_range('C1:C2', 'Original Image After Auto Crop', heading_format)
worksheet.merge_range('D1:D2', 'Original AI Scan', heading_format)
worksheet.merge_range('E1:E2', 'Scan After Refinements', heading_format)
worksheet.set_column('A:A', 36)
worksheet.set_column('B:B', 45)
worksheet.set_column('C:C', 32)
worksheet.set_column('D:D', 32)
worksheet.set_column('E:E', 32)
data_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter'})
data_format.set_text_wrap()
n = 5
count = 1
while count <= 69:
    worksheet.merge_range(0,n,0,n+1, 'Keypoint '+str(count), heading_format)
    #worksheet.set_column(1,n, 16)
    #worksheet.set_column(1,n+1, 16)
    worksheet.write(1,n,'X-Axis', heading_format)
    worksheet.write(1,n+1,'Y-Axis', heading_format)
    count += 1
    n += 2
directory = next(os.walk('./cv2Capture'))[1]
directory.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))# Taken from https://stackoverflow.com/questions/36259763/sort-list-of-string-based-on-number-in-string
print(len(directory))

count = 2
for file in directory:
    print(file)
    worksheet.set_row(count, 180)
    worksheet.write(count,0,file, data_format)
    worksheet.insert_image(count,1, resize('./cv2Capture/'+file+'/Camera.png',320))
    worksheet.insert_image(count,3, resize('./cv2Capture/'+file+'/Graph.png',224))
    image, data = FacialKeyPointEditor('./cv2Capture/'+file+'/Camera.png')
    fig, ax = plt.subplots()
    ax.imshow(image, extent=[0, 223.5, 223.5, 0])
    xPlots = []
    yPlots = []
    allData = []
    for items in data:
        xPlots.append(items[0])
        yPlots.append(items[1])
        allData.append(items[0])
        allData.append(items[1])
    plt.scatter(xPlots,yPlots)
    if not os.path.exists('./FacialKeypointEditorCache(Fig)/'):
        os.makedirs('./FacialKeypointEditorCache(Fig)/')
    if not os.path.exists('./FacialKeypointEditorCache(Img)/'):
        os.makedirs('./FacialKeypointEditorCache(Img)/')
    figPath = "./FacialKeypointEditorCache(Fig)/"+str(time()).replace(".","")+".png"
    imgPath = "./FacialKeypointEditorCache(Img)/"+str(time()).replace(".","")+".png"
    plt.savefig(figPath)
    plt.close()
    im = Image.fromarray((image*255).astype(np.uint8))
    im.save(imgPath)
    worksheet.insert_image(count,2, resize(imgPath,224))
    worksheet.insert_image(count,4, resize(figPath,224))
    n = 5
    for points in allData:
        worksheet.write(count,n,points, data_format)
        n += 1
    count += 1
#worksheet.save()
workbook.close()
