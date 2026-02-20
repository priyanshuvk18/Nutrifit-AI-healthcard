# Food Recognition Model Training Guide

## Overview
This guide explains how to train the food recognition model using your own dataset.

## Prerequisites
- TensorFlow 2.13+
- Food dataset organized in folders
- GPU recommended for faster training

## Dataset Structure
```
food_dataset/
├── train/
│   ├── apple/
│   │   ├── apple_001.jpg
│   │   ├── apple_002.jpg
│   │   └── ...
│   ├── banana/
│   └── ...
└── validation/
    ├── apple/
    ├── banana/
    └── ...
```

## Training Script

```python
from backend.ml.food_recognition import FoodRecognitionModel

# Create model
model = FoodRecognitionModel(num_classes=50)
model.build_model()

# Train
history = model.train(
    train_data_dir='./food_dataset/train',
    validation_data_dir='./food_dataset/validation',
    epochs=20
)

# Save trained model
model.save_model('./models/food_recognition_model.h5')
```

## Using Pre-trained Model

If you don't have training data, the system uses a **simple classifier** that:
- Maps images to foods in the nutrition database
- Provides consistent results based on image properties
- Works for demo/testing purposes

## Real CNN Model Usage

```python
from backend.ml.food_recognition import FoodRecognitionModel

# Load trained model
model = FoodRecognitionModel()
model.load_model('./models/food_recognition_model.h5')
model.load_nutrition_database('./data/nutrition_dataset.csv')

# Predict food and get calories
result = model.estimate_calories('path/to/food_image.jpg')
print(result)
```

## Public Food Datasets

To train a production model, use public datasets:

1. **Food-101**: 101,000 images of 101 food categories
   - Download: https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/

2. **UEC FOOD-256**: Japanese food dataset
   - 256 categories of food

3. **Recipe1M**: Large-scale recipe dataset with images

## Transfer Learning Tips

1. **Freeze base layers**: Keep MobileNetV2 weights frozen initially
2. **Fine-tuning**: After 10 epochs, unfreeze last 20 layers
3. **Data augmentation**: Use rotation, flip, zoom for better generalization
4. **Class imbalance**: Use class weights if dataset is imbalanced

## Model Performance

Expected accuracy:
- **Top-1 accuracy**: 60-75% (exact match)
- **Top-3 accuracy**: 85-90% (within top 3 predictions)

## Production Deployment

For production:
1. Train model on Food-101 dataset
2. Convert to TensorFlow Lite for mobile
3. Host model on cloud (AWS S3, GCS)
4. Use model versioning for updates
