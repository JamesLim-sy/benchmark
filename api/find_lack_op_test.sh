#!bin/bash
paddle_dir=/work/Paddle/paddle/fluid/operators
benchmakr_dir=/work/benchmark/api/tests_v2/configs
python glob_untests_ops.py   -paddle_path ${paddle_dir}  -benchmark_path ${benchmakr_dir}