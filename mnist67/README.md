# MNIST 6 vs 7 Classifier

Simple MLP training script for binary classification of digits 6 and 7 from MNIST.

## Examples

```bash
# With 2 hyperparameters
uv run train.py --learning_rate 0.001 --batch_size 32

# With all hyperparameters
uv run train.py --learning_rate 0.001 --batch_size 32 --model_width 128 --model_depth 3 --dataset_size 3000 --epochs 5
```

