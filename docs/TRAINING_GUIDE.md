# SFM-2 Training Guide

## Quick Start

### Prerequisites

- Python 3.8+
- PyTorch 2.0+
- CUDA-capable GPU (recommended)
- 16GB+ RAM

### Installation

```bash
git clone https://github.com/Bryantad/SfM-2.git
cd SfM-2
pip install -r requirements.txt
pip install -e .
```

### Basic Training

```bash
# Configure your training parameters
cp configs/example_config.json configs/my_config.json

# Start training
python src/sfm2/training/pipeline.py --config configs/my_config.json
```

## Configuration

### Training Parameters

```json
{
  "model": {
    "vocab_size": 50000,
    "hidden_size": 768,
    "num_layers": 12,
    "num_attention_heads": 12,
    "max_position_embeddings": 1024
  },
  "training": {
    "batch_size": 16,
    "learning_rate": 5e-5,
    "num_epochs": 10,
    "warmup_steps": 1000,
    "eval_steps": 500
  },
  "data": {
    "train_path": "data/train.json",
    "val_path": "data/val.json",
    "max_length": 512
  }
}
```

## Data Preparation

### Data Format

Training data should be in JSON format:

```json
[
  {
    "input": "def fibonacci(n):",
    "output": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "language": "python",
    "task": "code_completion"
  }
]
```

### Data Processing Pipeline

```bash
# Process and clean your dataset
python src/sfm2/training/data_processing.py \
  --input_dir raw_data/ \
  --output_dir processed_data/ \
  --language python
```

## Advanced Training

### Multi-GPU Training

```bash
python -m torch.distributed.launch \
  --nproc_per_node=4 \
  src/sfm2/training/pipeline.py \
  --config configs/my_config.json \
  --distributed
```

### Fine-tuning from Checkpoint

```bash
python src/sfm2/training/pipeline.py \
  --config configs/my_config.json \
  --resume_from_checkpoint checkpoints/model_epoch_5.pt
```

### Custom Model Architecture

```python
from sfm2.core import SFM2Model, SFM2Config

# Create custom configuration
config = SFM2Config(
    vocab_size=50000,
    hidden_size=1024,  # Larger model
    num_layers=24,     # More layers
    syntax_aware=True  # Enable syntax awareness
)

# Initialize model
model = SFM2Model(config)
```

## Evaluation

### Running Evaluation

```bash
python src/sfm2/training/evaluation.py \
  --model_path checkpoints/best_model.pt \
  --test_data data/test.json \
  --output_dir eval_results/
```

### Custom Evaluation Metrics

```python
from sfm2.training.evaluation import CodeEvaluator

evaluator = CodeEvaluator()
results = evaluator.evaluate(
    model=model,
    test_data=test_data,
    metrics=['bleu', 'code_bleu', 'exact_match', 'functional_correctness']
)
```

## Monitoring and Logging

### TensorBoard Integration

```bash
# Start TensorBoard
tensorboard --logdir logs/

# Training will automatically log metrics
python src/sfm2/training/pipeline.py --config configs/my_config.json
```

### Custom Logging

```python
import logging
from sfm2.utils import setup_logging

setup_logging(log_level='INFO', log_file='training.log')
logger = logging.getLogger(__name__)
```

## Troubleshooting

### Common Issues

**Out of Memory**

- Reduce batch size in configuration
- Use gradient accumulation: `"gradient_accumulation_steps": 4`
- Enable mixed precision: `"fp16": true`

**Slow Convergence**

- Increase learning rate
- Adjust warmup steps
- Check data quality and diversity

**Poor Performance**

- Increase model size
- Add more training data
- Tune hyperparameters

### Performance Optimization

```python
# Enable optimizations
config.update({
    "fp16": True,
    "gradient_checkpointing": True,
    "dataloader_num_workers": 4
})
```

## Best Practices

1. **Start Small**: Begin with a smaller model to validate your pipeline
2. **Monitor Metrics**: Track both loss and task-specific metrics
3. **Regular Checkpoints**: Save model state frequently
4. **Validation**: Use held-out validation set for hyperparameter tuning
5. **Documentation**: Keep detailed logs of experiments and results

## Production Deployment

### Model Export

```bash
# Export trained model for inference
python scripts/export_model.py \
  --checkpoint checkpoints/best_model.pt \
  --output_dir production_models/
```

### API Integration

```python
from sfm2.api import SFM2API

api = SFM2API(model_path='production_models/sfm2_model.pt')
result = api.generate(prompt="def quicksort(arr):", max_length=100)
```

For more advanced topics, see the [API Reference](API_REFERENCE.md) and [Research Methodology](RESEARCH_METHODOLOGY.md).
