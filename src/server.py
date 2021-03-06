from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from src.model import SticklebackLeadership
from src.agents import ShyFish, BoldFish, Water


def stickleback_portrail(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Water:
        if agent.deep:
            portrayal["Color"] = ["#768DFF", "#7185F2", "#5C67BF"]
        else:
            portrayal["Color"] = ["#5C67BF", "#4B529B", "#2A2B58"]

        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    if type(agent) is BoldFish:
        portrayal["Color"] = ["#FFFFFF"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["r"] = 1
    
    if type(agent) is ShyFish:
        portrayal["Color"] = ["#AAAAAA"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["r"] = 1    

    return portrayal

canvas_element = CanvasGrid(stickleback_portrail, 20, 20, 500, 500)
chart_element = ChartModule(
    [
        {
            "Label": "Bold Fish", 
            "Color": "#AA0000"
        }, 
        {
            "Label": "Shy Fish", 
            "Color": "#666666"
        }
    ]
)
visualization_elements = [canvas_element]  # [canvas_element, chart_element]
model_params = {}
title = "Leadership in Stickleback Fish Pairs"

server = ModularServer(SticklebackLeadership, visualization_elements, title, model_params)
server.port = 8521
