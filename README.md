# behavior-pattern-miner
(Unfinished) Anwendung Behavior Pattern Mining nach  
Diamantini, C., Genga, L. & Potena, D. Behavioral process mining for unstructured processes. J Intell Inf Syst 47, 5–32 (2016). https://doi.org/10.1007/s10844-016-0394-7

# Installation

First you need to install the Python Distribution Anaconda and PM4Py 2.2
For Both follow installation guide of PM4PY 2.2: https://pm4py.fit.fraunhofer.de/install

After installing PM4PY and Anaconda you are ready to build instance graphs.  

To extract behavioral pattern you need to build subdue via make:
Open your console in subdue-5.2.2/src and run the following:  
    
    make
  
    make install
  
    make clean
For more Details consult user manual in subdue-5.2.2/docs  
Beware Subdue is tested on linux.

# Usage

Use PM4PY Import Methods to import your Event Log.  
Use PM4Py iIM to generate a PetriNet (Workflow net) which represents Event Casual Relation to the best.  
For Instance Graph repair purpose get Pm4Py alignment from PetriNet and Event Log, but beware Alignment calculation is very slow.  

Functions to generate 
- Casual Relation from Petri Net, 
- Instance Graph from Event log and Casual Relation
- to repair instance Graph
- to generate Instance Graph and Repair
in src.  
You find a usage example in BehavioralPattern.ipynb (jupyter Notebook).  

