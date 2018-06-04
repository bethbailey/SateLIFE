# Write-up

## SateLIFE

### Contributors: Cooper Nederhood, Beth Bailey, Laurence Warner, Jo Denby

##### Primary code contribution by: Beth Bailey, Jo Denby, Cooper Nederhood

### Description of data

### Hypotheses

##### The Kuznets Curve

See the diagram below for an example of the Kuznets curve hypothesis.

<img src="kuznets.htm" width="200" height="200">

Developing nations like DRC & Republic of Congo are expected to be on the left hand side of the graph, and undergo environmental degradation as they develop over time.

Measures of environmental degradation:

* Reduction of green spaces: NDVI - Normalized Difference Vegatation Index
* Light pollution: Night Lights Index
* Urban build-up: Land Surface Temperature

### Algorithms

### Big data

#### Automation via Bash Scripts
In order to maximize our use of MPI via the Google Cloud VM platform while avoiding the tedium of manually initializing, preparing, and linking instances/nodes, we wrote a handful of Bash scripts that would automate the process. For `gcloudsetup.sh`, the user simply runs the script specifying the nubmer of VM instances desired, and the shell, using the `gcloud` command-line interface, will create those instances, send over requisite files/data via `SCP`, and install necessary software and packages. From within each node, the script also calls `chain.sh`, which connects each node to each other nodes via `SSH` to facilitate MPI. Finally, `update.sh` serves to automate the process of sending files and directories to all nodes at once. Look within the scripts for explicit documentation.
### Results

### Challenges
