import PySimpleGUI as sg
import math
sg.theme('bluemono')
font=('Franklin Gothic Book',16)
basic = {'justification':'center'}
button= {'font':font}
inputs={'font':('Franklin Gothic Book',20), 'text_color':'#000000','background_color':'#F7F7F7'}
inputColumnVisible=True

def InputItem(num, formula):
    return [sg.Column(size=(1000,46),background_color='#859FCC',pad=0,layout=[[sg.Text(f'{num}. ',size=(3,2),pad=0,background_color='#859FCC'), sg.Input(**inputs,pad=0,key="inf"+str(num),size=(27,100),border_width=0,default_text=str(formula)), sg.Button('X',size=(2,1),button_color=('#F7F7F7','#859FCC'), key="infb"+str(num))],[sg.HorizontalSeparator(pad=(0,5),color='#53697c')]])]
topColumn=[[sg.Button('file',**button,size=(4,1),pad=(0,0),enable_events=True,key="file"),sg.Text("UniCalculator", **basic, size=105,font=('Franklin Gothic Book',20), background_color='#859FCC')]]
inputColumn=[[sg.HorizontalSeparator(pad=(0,0),color='#53697c')]]
sizeColumn=[[sg.Button('<',**button,size=(3,1),key="frameSize",pad=0,border_width=1)]]
buttonColumn=[[sg.Button('+',**button,size=(3,1),key="addFunction",pad=0,border_width=1)]]
zoomButtonColumn=[[sg.vbottom(sg.Button(image_source="zoom.png",key="zoomIn",border_width=0,pad=(0,10),image_subsample=10,button_color='#859FCC',image_size=(40,40)))],
                  [sg.vbottom(sg.Button(image_source="zoom-out.png",key="zoomOut",pad=0,border_width=0,image_subsample=10,button_color='#859FCC',image_size=(40,40)))]]

functionList=[]

layout=[
    [sg.pin(sg.Column(layout=topColumn,expand_x=True,size=(2000,50),pad=0))],
    [sg.pin(sg.Column(layout=inputColumn,size=(500,665),background_color='#859FCC',pad=0,scrollable=True,vertical_scroll_only=True,key="inputColumn")),sg.pin(elem=sg.Graph(canvas_size=(900, 650), graph_bottom_left=(-10,-7.2), graph_top_right=(10,7.2),background_color='white',enable_events=True,float_values = True, drag_submits=True, key='graph'),vertical_alignment = None,shrink = True,expand_x = True,expand_y = True,),sg.vbottom(sg.Column(layout=zoomButtonColumn))],
    [sg.pin(sg.Column(layout=sizeColumn,background_color='#859FCC',pad=0,size=(42,45),key="sizeColumn")),sg.pin(sg.Column(layout=buttonColumn,background_color='#859FCC',pad=0,size=(472,45),key="buttonColumn"))]
]
window = sg.Window('My Title')
window.layout(layout)
window.finalize()

graph=window["graph"]
graphWindowLocation=[[-10,-7.2],[10,7.2]]
gridWidth=0.45

def changeGrid(graphWindowLocation,gridWidth):
    if (graphWindowLocation[1][0]-graphWindowLocation[0][0])/gridWidth<40:
        gridWidth=gridWidth/2
    elif (graphWindowLocation[1][0]-graphWindowLocation[0][0])/gridWidth>80:
        gridWidth = gridWidth * 2
    print(str(gridWidth))
    return gridWidth

def drawGrid(gridWidth,graphWindowLocation):
    print(graphWindowLocation)
    for x in range(math.floor(graphWindowLocation[0][0]/gridWidth-1.00),math.ceil(graphWindowLocation[0][1]/gridWidth+1.00)):

        graph.draw_line((graphWindowLocation[0][0], gridWidth*x), (graphWindowLocation[0][1], gridWidth*x), color="#bcbce0", width=1)
        graph.draw_line((gridWidth*x,graphWindowLocation[0][0]), (gridWidth*x,graphWindowLocation[0][1]), color="#bcbce0", width=1)
        graph.draw_line((graphWindowLocation[0][0], 5*gridWidth*x), (graphWindowLocation[0][1], 5*gridWidth*x), color="black", width=1)
        graph.draw_line((5*gridWidth*x,graphWindowLocation[0][0]), (5*gridWidth*x,graphWindowLocation[0][1]), color="black", width=1)
    graph.draw_line((graphWindowLocation[0][0],0),(graphWindowLocation[0][1],0),color="black",width=4)
    graph.draw_line((0,graphWindowLocation[1][0]), (0,graphWindowLocation[1][1]), color="black", width=4)


gridWidth = changeGrid(graphWindowLocation, gridWidth)
drawGrid(gridWidth, graphWindowLocation)


def updateFunction(functionList):
    inf = [InputItem(num=x, formula=functionList[x-1]) for x in range(1,len(functionList)+1)]+[[sg.Button('+',**button,size=(3,1),key="addFunction")]]
    return inf
while True:
    window.Size = (1500, 770)
    event, value = window.read()
    print("event:",event)
    print("value:",value)
    print(layout)
    # if str(event)[0]=="i" and str(event)[1]=="n" and str(event)[2]=="f"and str(event)[3]=="b":
    #     del functionList[int(event[4:])-1]
    #     for x in range(0,len(functionList)):
    #         functionList[x] = value['inf'+str(x+1)]
    #     inputFrame=updateFunction(functionList)
    #
    #     window["inputColumn"].contents_changed()
    if event == "frameSize":
        if inputColumnVisible==True:
            window["inputColumn"].update(visible=False)
            window["buttonColumn"].update(visible=False)
            window["frameSize"].update(text=">")
            window["graph"].set_size((1415,650))

            inputColumnVisible =False
        elif inputColumnVisible==False:
            window["inputColumn"].update(visible=True)
            window["buttonColumn"].update(visible=True)
            window["frameSize"].update(text="<")
            window["graph"].set_size((900, 650))
            inputColumnVisible =True
    if event == "addFunction":
        print(layout)
        functionList.append("")
        inputFrame = updateFunction(functionList)
        print(functionList)
        window.extend_layout(container=window['inputColumn'],rows=[InputItem(len(functionList),"")])
        window["inputColumn"].contents_changed()
    if event == "zoomIn":
        window["graph"].change_coordinates((graphWindowLocation[0][0]*1.5,graphWindowLocation[0][1]*1.5),(graphWindowLocation[1][0]*1.5,graphWindowLocation[1][1]*1.5))
        graphWindowLocation=[[graphWindowLocation[0][0]*1.5,graphWindowLocation[0][1]*1.5],[graphWindowLocation[1][0]*1.5,graphWindowLocation[1][1]*1.5]]
        graph.erase()
        print(graphWindowLocation)
        gridWidth=changeGrid(graphWindowLocation,gridWidth)
        drawGrid(gridWidth,graphWindowLocation)
    if event == "zoomOut":
        window["graph"].change_coordinates((graphWindowLocation[0][0]/1.5,graphWindowLocation[0][1]/1.5),(graphWindowLocation[1][0]/1.5,graphWindowLocation[1][1]/1.5))
        graphWindowLocation=[[graphWindowLocation[0][0]/1.5,graphWindowLocation[0][1]/1.5],[graphWindowLocation[1][0]/1.5,graphWindowLocation[1][1]/1.5]]
        graph.erase()
        print(graphWindowLocation)
        gridWidth=changeGrid(graphWindowLocation,gridWidth)
        drawGrid(gridWidth,graphWindowLocation)
    if event[0:4] == "graph":
        pass
    if event == sg.WIN_CLOSED:
        break
window.close()
