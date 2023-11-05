#Import modules
import taipy as tp
from taipy import Config, Scope, Gui
import pandas as pd
import numpy as np

#Back-End Code
#Filter function for best/worst colleges within 1 stat
def filtering_college(initial_dataset: pd.DataFrame, selected_stat, ):
    completed_graph_dataset = initial_dataset[selected_stat]
    completed_graph_data = completed_graph_dataset.nlargest(10, selected_stat, keep = "all")
    return completed_graph_data

#Data Node Creation
initial_dataset_cfg = Config.configure_data_node(id="initial_dataset",storage_type="csv",path="College_Data.csv",scope=Scope.GLOBAL)

selected_stat_cfg = Config.configure_data_node(id = "selected_stat", default_data = "Name", slope = Scope.GLOBAL)

completed_graph_data_cfg = Config.configure_data_node(id="completed_graph_data", scope=Scope.GLOBAL)

#Task Creation
filtered_college_cfg = Config.configure_task(id = "filtered_college", function=filtering_college, input = [initial_dataset_cfg, selected_stat_cfg], output = [completed_graph_data_cfg])

#Pipeline Creation
pipeline_cfg = Config.configure_scenario(id="pipeline",task_configs=[filtered_college_cfg])

#Scenario Creation
scenario_cfg = Config.configure_scenario(id = "scenario", pipeline_configs = [pipeline_cfg])
#scenario = tp.create_scenario(scenario_cfg)
#Core creation
if __name__ == "__main__":
    tp.Core().run()
#Start of Front-End Code
#Callback Function
def modify_df(state):
    scenario.selected_node.write(state.selected_stat)
    tp.submit(scenario)
    state.df = scenario.completed_graph_data_cfg.read()

list_stats = ["Name","Private","Apps","Accept","Enroll","Top10perc","Top25perc","F.Undergrad","P.Undergrad","Outstate","Room.Board","Books","Personal","PhD","Terminal","S.F.Ratio","perc.alumni","Expend","Grad.Rate"]
selected_stat = "Top10perc"
df = pd.DataFrame(columns = ["Name", selected_stat], copy = True)
#Variable Instantiation

#App Creation
college_stat_app = """<|{selected_stat}|selector|lov={list_stats}|on_change=modify_df|dropdown|>
<|{df}|chart|x=Name|y=selected_stat|type=bar|title=College Stats|>"""



#Runs the app (finally)
print(selected_stat)
Gui(page = college_stat_app).run()
