# AMQs

Running the AMQ evaluations requires:
* bloom_filter2
* cython
* pybbhash (from https://github.com/dib-lab/pybbhash/pull/18)

A directory with pybbhash is included with this repository. Inside the pybbhash directory, run ```python3 setup.py build_ext --inplace``` to set up bbhash.

Run the evaluations with ```python3 main.py```.
