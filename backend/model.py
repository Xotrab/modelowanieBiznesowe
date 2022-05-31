import pygraphviz as pgv
from itertools import product
from collections import defaultdict
from typing import Dict, Set
from IPython.display import Image, display
import os
import pandas as pd
import pm4py

#Graph class
class MyGraph(pgv.AGraph):
  
    def __init__(self, *args):
        super(MyGraph, self).__init__(strict=False, directed=True, *args)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        self.edge_attr.update(penwidth='2')
        self._created_connectors = set()
 
    def add_event(self, name):
        super(MyGraph, self).add_node(name, shape="circle", label="")
 
    def add_end_event(self, name):
        super(MyGraph, self).add_node(name, shape="circle", label="",penwidth='3')

    def add_and_gateway(self, *args):
        super(MyGraph, self).add_node(*args, shape="diamond",
                                  width=".7",height=".7",
                                  fixedsize="true",
                                  fontsize="40",label="+")
 
    def add_xor_gateway(self, *args, **kwargs):
        super(MyGraph, self).add_node(*args, shape="diamond",
                                  width=".7",height=".7",
                                  fixedsize="true",
                                  fontsize="40",label="×")
 
    def add_and_split_gateway(self, source, targets, *args):
        gateway = 'ANDs '+str(source)+'->'+str(targets)        
        self.add_and_gateway(gateway,*args)
        super(MyGraph, self).add_edge(source, gateway)
        for target in targets:
            super(MyGraph, self).add_edge(gateway, target)
 
    def add_xor_split_gateway(self, source, targets, *args):
        gateway = 'XORs '+str(source)+'->'+str(targets) 
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).add_edge(source, gateway)
        for target in targets:
            super(MyGraph, self).add_edge(gateway, target)
 
    def add_and_merge_gateway(self, sources, target, *args):
        gateway = 'ANDm '+str(sources)+'->'+str(target)
        self.add_and_gateway(gateway,*args)
        super(MyGraph, self).add_edge(gateway,target)
        for source in sources:
            super(MyGraph, self).add_edge(source, gateway)
 
    def add_xor_merge_gateway(self, sources, target, *args):
        gateway = 'XORm '+str(sources)+'->'+str(target)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).add_edge(gateway,target)
        for source in sources:
            super(MyGraph, self).add_edge(source, gateway)

    def add_xor_merge_to_and_split(self, sources, targets, *args):
      xor_gateway = 'XORm '+str(sources)+'->'+str(targets)
      and_gateway = 'ANDs '+str(sources)+'->'+str(targets)

      connector_name = and_gateway + xor_gateway
      if(connector_name in self._created_connectors):
        return
      
      self._created_connectors.add(connector_name)

      self.add_xor_gateway(xor_gateway, *args)
      self.add_and_gateway(and_gateway, *args)
      for source in sources:
        super(MyGraph, self).add_edge(source, xor_gateway)
      
      super(MyGraph, self).add_edge(xor_gateway, and_gateway)

      for target in targets:
        super(MyGraph, self).add_edge(and_gateway, target)

    def add_and_merge_to_xor_split(self, sources, targets, *args):
      xor_gateway = 'XORs '+str(sources)+'->'+str(targets)
      and_gateway = 'ANDm '+str(sources)+'->'+str(targets)

      connector_name = and_gateway + xor_gateway
      if(connector_name in self._created_connectors):
        return
      
      self._created_connectors.add(connector_name)

      self.add_xor_gateway(xor_gateway, *args)
      self.add_and_gateway(and_gateway, *args)
      for source in sources:
        super(MyGraph, self).add_edge(source, and_gateway)
      
      super(MyGraph, self).add_edge(and_gateway, xor_gateway)

      for target in targets:
        super(MyGraph, self).add_edge(xor_gateway, target)

    def add_xor_split_and_return_name(self, source, targets, *args):
      xor_gateway = 'XORs '+str(source)+str(targets)
      self.add_xor_gateway(xor_gateway, *args)
      super(MyGraph,self).add_edge(source, xor_gateway)
      for target in targets:
        super(MyGraph,self).add_edge(xor_gateway, target)
      
      return xor_gateway

    def add_self_loop(self, event, *args):
      xor_gateway = 'XORs ' + str(event) + str(event)
      self.add_xor_gateway(xor_gateway, *args)
      super(MyGraph,self).add_edge(event, xor_gateway)
      super(MyGraph,self).add_edge(xor_gateway, event)
      
      return xor_gateway


    def add_short_loop(self, loop_source, loop_target, *args):
      xor_gateway_start = 'XORs ' + str(loop_source) + str(loop_target)
      self.add_xor_gateway(xor_gateway_start, *args)
      
      xor_gateway_end = 'XORm ' + str(loop_source) + str(loop_target)
      self.add_xor_gateway(xor_gateway_end, *args)

      super(MyGraph,self).add_edge(loop_target, xor_gateway_start)
      super(MyGraph,self).add_edge(xor_gateway_start, loop_source)
      super(MyGraph,self).add_edge(loop_source, xor_gateway_end)
      super(MyGraph,self).add_edge(xor_gateway_end, loop_target)

      return xor_gateway_start, xor_gateway_end

#Method for filtering the traces based on the given threshold and the helper for counting event occurences
def get_counts_for_events(traces):
  occuring_events = {x for l in traces for x in l}
  events_with_counts = {x: 0 for x in occuring_events}
  for x in [j for d in traces for j in d]:
    events_with_counts[x]+=1
  
  return events_with_counts

def preprocess_traces(traces, threshold=0):
  events_with_counts = get_counts_for_events(traces)
  new_traces = []
  for trace in traces:
    new_trace = []
    for event in trace:
      if events_with_counts[event]>threshold:
        new_trace.append(event + " - " + str(events_with_counts[event]))
    if(len(new_trace)>0):
      new_traces.append(new_trace)
  
  return new_traces

#Methods for extracting the self loops
def leave_only_first_occurrence(trace, element):
  first_skipped = False;
  new_trace = []
  for event in trace:
    if event == element:
      if first_skipped:
        continue 
      first_skipped = True
    
    new_trace.append(event)
  return new_trace

def extract_self_loops(traces):
  self_loops = set()
  new_traces = []
  for trace in traces:
    new_trace = [trace[0]]
    for i in range(1, len(trace)):
      if trace[i] in self_loops:
        if trace[i] not in new_trace:
          new_trace.append(trace[i])
        continue

      if trace[i] != trace[i-1]:
        new_trace.append(trace[i])
        continue

      if trace[i] not in new_trace:
        new_trace.append(trace[i])

      else:
        new_trace = leave_only_first_occurrence(new_trace, trace[i])

      self_loop = trace[i]
      self_loops.add(self_loop)

    new_traces.append(new_trace)
  
  return self_loops, new_traces

#Methods for extracting short loops
def are_short_loop(short_loops, pred, curr):
  is_curr_key_pred_value = pred in short_loops and short_loops[pred] == curr
  is_pred_key_curr_value = curr in short_loops and short_loops[curr] == pred

  return is_curr_key_pred_value or is_pred_key_curr_value

def should_add_short_loop(short_loops, pred, curr, succ):
  if pred != succ:
    return False
  
  return not are_short_loop(short_loops, pred, curr)

def extract_short_loops(traces):
  new_traces = []
  short_loops = {}

  for trace in traces:
    if(len(trace)<3):
      continue

    new_trace = [trace[0]]
    for i in range(1,len(trace)-1):
      if should_add_short_loop(short_loops, trace[i-1], trace[i], trace[i+1]): 
        short_loops[trace[i-1]] = trace[i]

  if len(short_loops.keys()) == 0:
    new_traces = traces.copy()
    return short_loops, new_traces

  for key in short_loops:
    for trace in traces:
      new_trace = leave_only_first_occurrence(trace, key)
      if short_loops[key] in new_trace:
        new_trace = list(filter(lambda x: x != short_loops[key], new_trace))

      new_traces.append(new_trace)
  return short_loops, new_traces

#Method for getting the direct successions from the traces
def get_direct_successions(traces):
  successions = { }
  for trace in traces:
    prev_event = None
    for event in trace:
      if event not in successions:
        successions[event] = set()
      if prev_event != None:
        successions[prev_event].add(event)
      prev_event = event

  to_remove = []  
  for key in successions: 
    if len(successions[key]) == 0:
      to_remove.append(key)

  for key in to_remove:
    del successions[key]
    
  return successions

#Method for getting the causality based on direct successions
def get_causality(direct_succession) -> Dict[str, Set[str]]:
    causality = defaultdict(set)
    for ev_cause, events in direct_succession.items():
        for event in events:
            if ev_cause not in direct_succession.get(event, set()):
                causality[ev_cause].add(event)
    return dict(causality)

#Method for getting the inversed causality based on given causality
def get_inv_causality(causality) -> Dict[str, Set[str]]:
    inv_causality = defaultdict(set)
    for key, values in causality.items():
        for value in values: 
          inv_causality[value].add(key)
    return {k: v for k, v in inv_causality.items() if len(v) >= 1}

#Method for getting the parallel events including the short loops logic
def get_parallel_events_plus(successions, traces, short_loops):
  parallel_events = []
  for key in successions:
    for successor_key in successions[key]:
      if successor_key in successions and key in successions[successor_key] and not are_short_loop(short_loops, key, successor_key):
        for key_set in parallel_events:
          if key in key_set:
            key_set.add(successor_key)
        else:
          parallel_events.append(set([key, successor_key]))

  filtered_parallel_events = []
  for parallels in parallel_events:
    if(parallels not in filtered_parallel_events):
      filtered_parallel_events.append(parallels)

  return filtered_parallel_events

#Method for checking if the events are parallel
def check_if_parallel(event_collection, parallel_events):
      event_set = set(event_collection)
      for par_event in parallel_events:
        if event_set.issubset(par_event):
          return True
      return False

#Method for creating the proper graph
def create_graph_plus(start_set_events, end_set_events, parallel_events, causality, inv_causality, short_loops, self_loops, non_special_events):
  G = MyGraph()

  # Key -> (Input_name, Output_name)
  LUT = {}

  for event in non_special_events:
    LUT[event] = (event,event)

  for event in self_loops:
    output_name = G.add_self_loop(event)
    LUT[event] = (event, output_name)

  for event in short_loops:
    input_name, output_name = G.add_short_loop(event, short_loops[event])
    LUT[event] = (input_name, output_name)
    
  # adding start event
  G.add_event("start")
  start_events_labels = {LUT[x][0] for x in start_set_events}
  if len(start_events_labels) > 1:
      if check_if_parallel(start_set_events, parallel_events): 
          G.add_and_split_gateway("start", start_events_labels)
      else:
          G.add_xor_split_gateway("start", start_events_labels)
  else: 
      G.add_edge("start",list(start_events_labels)[0])

  # adding split gateways based on causality
  for event in causality:
      if len(causality[event]) > 1:
          should_draw = True
          for element in causality[event]: 
            if(element in inv_causality and len(inv_causality[element]) > 1):
              should_draw = False
              break

          if(should_draw):
            causality_labels = [LUT[x][0] for x in causality[event]]
            if set(causality[event]) in parallel_events:        
                G.add_and_split_gateway(LUT[event][1], causality_labels)
            else:
                G.add_xor_split_gateway(event,causality_labels)
      elif event not in end_set_events and len(causality[event]) == 1 and (list(causality[event])[0] not in inv_causality or len(inv_causality[list(causality[event])[0]])==1):
        target = LUT[list(causality[event])[0]][0]
        G.add_edge(LUT[event][1],target)

  # adding merge gateways based on inverted causality
  for event in inv_causality:
      if len(inv_causality[event]) > 1:
        should_draw_connector = False
        targets = []
        potential_connectors = {}
        for element in inv_causality[event]:
          if(element in causality and len(causality[element]) > 1):
            for potential_connector in potential_connectors:
              if set(potential_connector) == causality[element]:
                potential_connectors[potential_connector].append(element)
                break
            else:

              potential_connectors[tuple(causality[element])] = [element]
            
        biggest_target = []
        for potential_targets in potential_connectors.values():
          if(len(potential_targets) > len(biggest_target)):
            biggest_target = potential_targets
        
        targets = [LUT[x][0] for x in causality[list(inv_causality[event])[0]]]
        
        if(len(biggest_target)>1): 
          should_draw_connector = True
          targets = [LUT[x][0] for x in causality[biggest_target[0]]]
          sources = [LUT[x][1] for x in biggest_target]

        sources = [LUT[x][1] for x in inv_causality[event]]
        
        parallel = None
        for par in parallel_events:
          if par.issubset(inv_causality[event]):
            parallel = par
            break

        if parallel != None:
            if(should_draw_connector):
              G.add_and_merge_to_xor_split(parallel, targets)
            else:
              G.add_and_merge_gateway(parallel,event)
        else:
            if(should_draw_connector):
              G.add_xor_merge_to_and_split(sources, targets)
            else:
              G.add_xor_merge_gateway(sources,event)
              
  # adding end event
  G.add_end_event("end")
  end_events_and_gateways = set(end_set_events)
  for event in end_set_events:
    if event in causality:
      targets = [LUT[x][0] for x in causality[event]]
      name = G.add_xor_split_and_return_name(LUT[event][1], targets)
      end_events_and_gateways.remove(event)
      end_events_and_gateways.add(name)
      LUT[name] = (name, name)

  end_events_labels = {LUT[x][1] for x in end_events_and_gateways}

  if len(end_events_and_gateways) > 1:
      if check_if_parallel(end_set_events, parallel_events): 
          G.add_and_merge_gateway(end_events_labels,"end")
      else:
          G.add_xor_merge_gateway(end_events_labels,"end")    
  else: 
      G.add_edge(list(end_events_labels)[0],"end")

  G.draw('model.png', prog='dot')
#   display(Image('model.png')) 

#Main draw method
def draw_for_traces_integrated_plus(traces, threshold):
  traces = preprocess_traces(traces, threshold)
  self_loops, new_traces = extract_self_loops(traces)
  short_loops, new_traces = extract_short_loops(new_traces)
 
  occuring_events = {x for l in traces for x in l} 
  non_special_events = occuring_events.difference(set(self_loops)).difference(short_loops.keys()).difference(short_loops.values())
  succ = get_direct_successions(new_traces)
  caus = get_causality(succ)
  inv_caus = get_inv_causality(caus)
  par = get_parallel_events_plus(succ, new_traces, short_loops)

  tr_start = list(set([trace[0] for trace in traces]))
  tr_end = list(set([trace[-1] for trace in traces]))

  if(len(new_traces) == 0):
    print("No traces found")
    return

  create_graph_plus(tr_start, tr_end, par, caus, inv_caus, short_loops, self_loops, non_special_events)

#Method for loading the given file into the pandas dataframe
def load_file(file):
  filename, file_extension = os.path.splitext(file)
  
  if file_extension == '.csv':
    df = pd.read_csv(file)
    df['Start Timestamp'] = pd.to_datetime(df['Start Timestamp'])
    return df

  elif file_extension == '.xes':
    log = pm4py.read_xes(file)
    df =  pm4py.convert_to_dataframe(log)
    df_cleared = df.drop(columns=['concept:name', 'lifecycle:transition', 'case:concept:name', 'case:variant', 'case:creator'])
    df_cleared.rename(columns={'case:variant-index': 'Case ID', 'time:timestamp': 'Start Timestamp'}, inplace=True)
    df_reordered = df_cleared[['Case ID', 'Activity', 'Start Timestamp']]
    df_reordered['Start Timestamp'] = pd.to_datetime(df_reordered['Start Timestamp'])

    return df_reordered

  return None

#Method for getting the traces based on the pandas dataframe for the loaded file
def get_traces_from_dataframe(df):
  return list(\
      df.sort_values(by=['Case ID','Start Timestamp'])\
      .groupby(['Case ID'])\
      .agg({'Activity': lambda x: list(x)})['Activity'])

#Method for generating the BPMN png file for the given file and the event threshold
def generate_BPMN(filename_with_extension, threshold):
    df = load_file(filename_with_extension)
    traces = get_traces_from_dataframe(df)
    draw_for_traces_integrated_plus(traces, threshold)
