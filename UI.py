import PySimpleGUI as sg
import math
import time


sg.theme('bluemono')
font=('Franklin Gothic Book',16)
basic = {'justification':'center'}
button= {'font':font}
inputs={'font':('Franklin Gothic Book',20), 'text_color':'#000000','background_color':'#F7F7F7'}
inputColumnVisible=True

def InputItem(num):
    return [sg.Column(size=(1000,46),background_color='#859FCC',pad=0,layout=[[sg.Text(f'{num}. ',size=(3,2),pad=0,background_color='#859FCC'), sg.Input(**inputs,pad=0,key="inf"+str(num),size=(27,100),border_width=0,enable_events=True), sg.Button('X',size=(2,1),button_color=('#F7F7F7','#859FCC'), key="deleteButton"+str(num))],[sg.HorizontalSeparator(pad=(0,5),color='#53697c')]])]
topColumn=[[sg.Button('file',**button,size=(4,1),pad=(0,0),enable_events=True,key="file"),sg.Text("UniCalculator", **basic, size=105,font=('Franklin Gothic Book',20), background_color='#859FCC')]]
inputColumn=[[sg.HorizontalSeparator(pad=(0,0),color='#53697c')]]
sizeColumn=[[sg.Button('<',**button,size=(3,1),key="frameSize",pad=0,border_width=1)]]
buttonColumn=[[sg.Button('+',**button,size=(3,1),key="addFunction",pad=0,border_width=1)]]
zoomButtonColumn=[[sg.vtop(sg.Button(image_source="zoom.png",key="zoomOut",border_width=0,pad=(0,0),image_subsample=15,image_size=(40,35)))],
                [sg.vtop(sg.Button(image_source="zoom-out.png",key="zoomIn",pad=(0,5),border_width=0,image_subsample=15,image_size=(40,35)))],
                  [sg.vbottom(sg.Button(image_source="run.png",key="run",border_width=0,pad=(0,15),image_subsample=10,image_size=(70,40)))]]

functionList=[]
functionNum=1
layout=[
    [sg.pin(sg.Column(layout=topColumn,expand_x=True,size=(2000,50),pad=0))],
    [sg.pin(sg.Column(layout=inputColumn,size=(500,665),background_color='#859FCC',pad=0,scrollable=True,vertical_scroll_only=True,key="inputColumn")),sg.pin(elem=sg.Graph(canvas_size=(900, 650), graph_bottom_left=(-10,-7.222), graph_top_right=(10,7.222),background_color='white',enable_events=True,float_values = True, drag_submits=True,border_width=5, key='graph'),vertical_alignment = None,shrink = True,expand_x = True,expand_y = True,),sg.vbottom(sg.Column(layout=zoomButtonColumn))],
    [sg.pin(sg.Column(layout=sizeColumn,background_color='#859FCC',pad=0,size=(42,45),key="sizeColumn")),sg.pin(sg.Column(layout=buttonColumn,background_color='#859FCC',pad=0,size=(472,45),key="buttonColumn"))]
]
window = sg.Window('My Title')
window.layout(layout)
window.finalize()

graph=window["graph"]
graphWindowLocation=[[-10,-7.222],[10,7.222]]
gridWidth=0.5
graphInitialDrag=[]

graphInitialTime=time.time()
timeNow=time.time()

def changeGrid(graphWindowLocation,gridWidth):
    if (graphWindowLocation[1][0]-graphWindowLocation[0][0])/gridWidth<40:
        gridWidth=gridWidth/2
    elif (graphWindowLocation[1][0]-graphWindowLocation[0][0])/gridWidth>80:
        gridWidth = gridWidth * 2

    return gridWidth

def drawGrid(gridWidth,graphWindowLocation):

    for x in range(math.floor(graphWindowLocation[0][1]/gridWidth),math.ceil(graphWindowLocation[1][1]/gridWidth)):
        if x%5==0:
            graph.draw_line((graphWindowLocation[0][0], gridWidth * x),
                            (graphWindowLocation[1][0], gridWidth * x), color="black", width=1)
            graph.DrawText(gridWidth * x, (-gridWidth, gridWidth * x + gridWidth / 1.5), color='blue')
        else:
            graph.draw_line((graphWindowLocation[0][0], gridWidth*x), (graphWindowLocation[1][0], gridWidth*x), color="#bcbce0", width=1)
    for x in range(math.floor(graphWindowLocation[0][0] / gridWidth),math.ceil(graphWindowLocation[1][0] / gridWidth)):
        if x%5==0:
            graph.draw_line((gridWidth * x, graphWindowLocation[0][1]), (gridWidth * x, graphWindowLocation[1][1]),color="black", width=1)
            graph.DrawText(gridWidth * x, (gridWidth * x + gridWidth / 1.5, -gridWidth), color='green')
        else:
            graph.draw_line((gridWidth*x,graphWindowLocation[0][1]), (gridWidth*x,graphWindowLocation[1][1]), color="#bcbce0", width=1)
    graph.draw_line((graphWindowLocation[0][0],0),(graphWindowLocation[1][0],0),color="black",width=4)
    graph.draw_line((0,graphWindowLocation[0][1]), (0,graphWindowLocation[1][1]), color="black", width=4)
    labelList=[]
    for x in range(1,1000):
        pointX=graphWindowLocation[0][0]+(graphWindowLocation[1][0]-graphWindowLocation[0][0])/1000*x
        pointY = math.sin(pointX / 20) * 50
        graph.DrawPoint((pointX,pointY),size=(graphWindowLocation[1][0]-graphWindowLocation[0][0])/200,color="red")
        if pointY >=graphWindowLocation[0][1] and pointY <= graphWindowLocation[1][1]:
            labelList.append(pointX)
    if len(labelList)>0:
        print(labelList)
        print(labelList[math.floor(len(labelList)/2)])
        graph.DrawText("y=50sin(x/20)", (labelList[math.floor(len(labelList)/2)],math.sin((labelList[math.floor(len(labelList)/2)]) / 20) * 50+gridWidth), color='black')

gridWidth = changeGrid(graphWindowLocation, gridWidth)
drawGrid(gridWidth, graphWindowLocation)

while True:
    window.Size = (1500, 770)
    event, value = window.read()
    if event[0:3]=="inf":
        functionList[int(event[3:])-1]=value[event]
        print(functionList)
    if event == "frameSize":
        if inputColumnVisible==True:
            window["inputColumn"].update(visible=False)
            window["buttonColumn"].update(visible=False)
            window["frameSize"].update(text=">")
            window["graph"].set_size((1415,650))
            window["graph"].change_coordinates((graphWindowLocation[0][0] * 1.57, graphWindowLocation[0][1]),
                                               (graphWindowLocation[1][0] * 1.57, graphWindowLocation[1][1]))
            graphWindowLocation = [[graphWindowLocation[0][0] * 1.57, graphWindowLocation[0][1]],
                                   [graphWindowLocation[1][0] * 1.57, graphWindowLocation[1][1]]]
            graph.erase()
            gridWidth = changeGrid(graphWindowLocation, gridWidth)
            drawGrid(gridWidth, graphWindowLocation)
            inputColumnVisible =False
        elif inputColumnVisible==False:
            window["inputColumn"].update(visible=True)
            window["buttonColumn"].update(visible=True)
            window["frameSize"].update(text="<")
            window["graph"].set_size((900, 650))
            window["graph"].change_coordinates((graphWindowLocation[0][0] / 1.57, graphWindowLocation[0][1]),
                                               (graphWindowLocation[1][0] / 1.57, graphWindowLocation[1][1]))
            graphWindowLocation = [[graphWindowLocation[0][0] / 1.57, graphWindowLocation[0][1]],
                                   [graphWindowLocation[1][0] / 1.57, graphWindowLocation[1][1]]]
            graph.erase()
            gridWidth = changeGrid(graphWindowLocation, gridWidth)
            drawGrid(gridWidth, graphWindowLocation)
            inputColumnVisible =True
    if event == "addFunction":
        functionList.append("")
        window.extend_layout(container=window['inputColumn'],rows=[InputItem(functionNum)])
        window["inputColumn"].contents_changed()
        functionNum+=1
    if event == "zoomIn":
        timeNow = time.time()
        if timeNow-graphInitialTime>=0.15:
            window["graph"].change_coordinates((graphWindowLocation[0][0]*1.5,graphWindowLocation[0][1]*1.5),(graphWindowLocation[1][0]*1.5,graphWindowLocation[1][1]*1.5))
            graphWindowLocation=[[graphWindowLocation[0][0]*1.5,graphWindowLocation[0][1]*1.5],[graphWindowLocation[1][0]*1.5,graphWindowLocation[1][1]*1.5]]
            graph.erase()
            gridWidth=changeGrid(graphWindowLocation,gridWidth)
            drawGrid(gridWidth,graphWindowLocation)
            graphInitialTime = time.time()
        else:
            graph.erase()
            gridWidth=changeGrid(graphWindowLocation,gridWidth)
            drawGrid(gridWidth,graphWindowLocation)
    if event == "zoomOut":
        timeNow = time.time()
        if timeNow - graphInitialTime >= 0.15:
            window["graph"].change_coordinates((graphWindowLocation[0][0]/1.5,graphWindowLocation[0][1]/1.5),(graphWindowLocation[1][0]/1.5,graphWindowLocation[1][1]/1.5))
            graphWindowLocation=[[graphWindowLocation[0][0]/1.5,graphWindowLocation[0][1]/1.5],[graphWindowLocation[1][0]/1.5,graphWindowLocation[1][1]/1.5]]
            graph.erase()
            gridWidth=changeGrid(graphWindowLocation,gridWidth)
            drawGrid(gridWidth,graphWindowLocation)
            graphInitialTime = time.time()
        else:
            graph.erase()
            gridWidth=changeGrid(graphWindowLocation,gridWidth)
            drawGrid(gridWidth,graphWindowLocation)
    if event[0:5] == "graph":
        print(value)
        if graphInitialDrag==[]:
            graphInitialDrag=[value['graph'][0],value['graph'][1]]
            graphInitialTime = time.time()
        if event=="graph+UP":
            timeNow=time.time()
            if timeNow-graphInitialTime>=0.05:
                window["graph"].change_coordinates((graphWindowLocation[0][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[0][1]+2*(-value['graph'][1]+graphInitialDrag[1])),(graphWindowLocation[1][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[1][1]+2*(-value['graph'][1]+graphInitialDrag[1])))
                graphWindowLocation=[[graphWindowLocation[0][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[0][1]+2*(-value['graph'][1]+graphInitialDrag[1])],[graphWindowLocation[1][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[1][1]+2*(-value['graph'][1]+graphInitialDrag[1])]]
                graph.erase()
                drawGrid(gridWidth, graphWindowLocation)
                graphInitialDrag = []
                graphInitialTime = time.time()
            else:
                graph.erase()
                drawGrid(gridWidth, graphWindowLocation)
                graphInitialDrag = []
        else:
            timeNow=time.time()
            if timeNow-graphInitialTime>=0.05:
                window["graph"].change_coordinates((graphWindowLocation[0][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[0][1]+2*(-value['graph'][1]+graphInitialDrag[1])),(graphWindowLocation[1][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[1][1]+2*(-value['graph'][1]+graphInitialDrag[1])))
                graphWindowLocation=[[graphWindowLocation[0][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[0][1]+2*(-value['graph'][1]+graphInitialDrag[1])],[graphWindowLocation[1][0]+2*(-value['graph'][0]+graphInitialDrag[0]), graphWindowLocation[1][1]+2*(-value['graph'][1]+graphInitialDrag[1])]]
                graph.erase()
                drawGrid(gridWidth, graphWindowLocation)
                graphInitialDrag = [value['graph'][0], value['graph'][1]]
                graphInitialTime=time.time()
            else:
                graph.erase()
                drawGrid(gridWidth, graphWindowLocation)
                graphInitialDrag = [value['graph'][0], value['graph'][1]]



    if event == sg.WIN_CLOSED:
        break
window.close()