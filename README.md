# Running the Project

## StarCraft II Setup
You can see [here](https://github.com/lior8/CIAI-Project/tree/main/smac#installing-starcraft-ii) a guide to install StarCraft II and where to put the SMAC maps.
If you are using Windows, we recommend utilizing WSL and installing StarCraft II on it for faster running.

## Conda Environments
2 environments [requirements](https://github.com/lior8/CIAI-Project/tree/main/Requirements) are provided: rllib and pymarl_3. rllib is for running the heuristic agents in smac, and pymarl_3 is for running the learning agents. Make sure to use the correct one for the following steps.

## Running Heuristic Agents
Simply setup the rllib environment and run [random_agents.py](https://github.com/lior8/CIAI-Project/blob/main/smac/smac/examples/random_agents.py) from the smac directory. It is a modified version of the original script from smac, which allows to run the heuristic agents instead of purely random ones. It also calls a few extra methods and logs to make the resulting debug log require less adapting when trying to work with it.

## Training the Agents
Make sure to look at src/config of pymarl2, especially look at default.yaml, algs/qmix.yaml and envs/sc2 which gives you a list of possible parameters to change. Here are a few intereting ones:
- difficulty - means the difficuly of the map as detailed in smac starcraft environment file.
- debug - Turn this to true when you want to output trajectories.
- batch_size_run - How many environments to run in parallel, use 1 for trajectory creation and more for training.
- save_model & save_model_interval - should the model be saved and if so, how often?
- checkpoint_path - load a model from this chekpoint. Note that this is the folder in results/models that filled with folders with number names, since each of those represents a checkpoint at that step count. We did not manage to use the checkpoint to resume learning after stopping, but it can be used to evaluate.
- evaluate: Is it evaluation of training?

**NOTE: If you do save models, make sure to change "name:" parameter in qmix, otherwise you will not be able to differentiate between different models**

To run the environment, simply use the following command from the pymarl2 folder (e.g., this runs 2s3z):
  ```
python src/main.py --config=qmix_2s3z --env-config=sc2 with env_args.map_name=2s3z
  ```
Note: While probably possible, we did not manage to change more than 1 env_args with "with".

  ## Trajectory Extraction
  Make sure the environment outputs debug information, and that it only runs one instance (and not parallel instances) and save both the stderr and stout to the file.

  ## Running on the Cluster
  To run in the cluster use the following instructions:
  1. install StarCraft II Linux version in your home folder and put the maps in.
  2. Install glibc-2.18 from source as you will need it to run the environment (this will be long, so you might want to submit a job to do it):
     ```
     curl -O http://ftp.gnu.org/gnu/glibc/glibc-2.18.tar.gz
     tar zxf glibc-2.18.tar.gz
     cd glibc-2.18/
     mkdir build
     cd build/
     ../configure --prefix=/usr
     make -j2
     mv libc.a $CONDA_PREFIX/lib # This command is instead of 'make install'
     ```
   3. Then you need to point the linux to the new place where it is installed. This needs to be done every time you activate the environment (including with the slurm files):
      ```
      export LD_LIBRARY_PATH="$CONDA_PREFIX/lib"
      ```

## SmacTrace Trace Interface
This is a wrapper to the debug files which provides a convinient interface to work with. Make sure to use the adapter when using a heuristic trace because they act a bit differently from the pymarl2 ones and needs to be slightly adapted before they can be analyzed.

## Analysis
Two files are needed for the analysis: 
1. ReadTrajectories.py, which uses the SmacTrace files and transforms trajectory objects into a csv. In order to run it, extract traces.zip and replace the input_dir with its location. 
2. TrajectoryClustering.ipynb which reads the csvs and clusters them. Replace input_dir with the location of all csvs (output of ReadTrajectories.py)
