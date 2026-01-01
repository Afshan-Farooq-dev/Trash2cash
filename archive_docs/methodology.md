# Methodology (Detailed)

This document provides a detailed methodology for the Trash2Cash project: tool choices, dataset inventory and processing, model experiments and evaluation, training procedures, deployment constraints, experimental observations, and recommended next steps for production readiness.

## 1. Tools & Technologies (Detailed)

- Languages & Frameworks
  - Python 3.11
  - Django (project backend and REST APIs)
  - Kotlin (mobile QR generator app)

- Machine Learning & Deep Learning
  - TensorFlow 2.x / Keras: primary training and export to `.h5` / SavedModel for inference on the server.
  - PyTorch (1.12+): used for Ultralytics YOLOv8 experiments.
  - Ultralytics YOLOv8 (detection prototypes)

- Computer Vision and Utilities
  - OpenCV (>=4.5): frame capture, preprocessing, image transforms
  - pyzbar: QR code detection/decoding
  - NumPy, Pandas: data handling
  - Matplotlib, Seaborn: visualization and confusion matrices
  - scikit-learn: metrics (precision/recall/f1), train-test splitting

- Development, Execution & Reproducibility
  - Google Colab (free/Pro): GPU-backed training during experiments
  - Local workstation with optional GPU for final runs
  - Docker (optional) for packaging inference services

- Suggested Python packages to pin in `requirements.txt`
  - tensorflow==2.11.*
  - torch==1.12.*
  - ultralytics==8.*
  - opencv-python
  - pyzbar
  - scikit-learn
  - pandas
  - matplotlib

### Suitability and justification
- TensorFlow/Keras is used for the final classification models because Keras provides straightforward transfer-learning APIs and easy export to `.h5` for server-side inference.
- PyTorch/Ultralytics (YOLOv8) is appropriate for detection workflows and fast prototyping of object-localization approaches; it is widely used and supported.
- OpenCV and `pyzbar` are lightweight, reliable tools for stream processing and QR decoding; OpenCV supports the MJPEG stream from ESP32-CAM and efficient preprocessing.
- Google Colab allows consistent GPU access for reproducible experiments and quick iteration.

## 2. Dataset Inventory & Strategy

### Datasets explored (representative)
During development we explored approximately 15 datasets from Kaggle, Roboflow and GitHub. Representative examples:

- `garbage_classification` (Kaggle)
- `TACO` (Trash Annotations in Context)
- `TrashNet` (commonly used academic dataset)
- `CIFAR-10` (used only for architecture validation / experimentation)
- Multiple Roboflow public datasets (various trash/rubbish collections with bounding boxes or classifications)
- Several GitHub-hosted community datasets and collected samples

Note: you may later provide the full list of exact dataset names/links; the repository contains metadata and scripts used to import and normalize those datasets.

### Dataset merging approach
- Inspect dataset licenses and metadata to ensure allowed usage.
- Standardize class labels: create a canonical label set used across all experiments:
  - plastic, paper, metal, glass, cardboard, trash
- Convert dataset formats into a uniform folder/CSV format; unify image sizes, and store origin/source metadata for later analysis.

### Data curation and balancing
- Identify class imbalance by inspecting per-class counts.
- Apply one or more of:
  - Oversampling (duplicate or augment minority samples)
  - Undersampling (for very large majority classes when safe)
  - Targeted augmentation: more aggressive transforms on under-represented classes
- Keep a provenance column for each sample so that any low-quality source can be filtered out during error analysis.

### Annotation and label cleaning
- When merging datasets, normalize label synonyms and remove ambiguous labels.
- If a dataset contains bounding boxes but no class mapping, convert them to the project's class taxonomy or discard if incompatible.

## 3. Model Families Evaluated (and rationale)

We evaluated both detection and classification families to decide the best operational flow.

- Detection-first options (YOLOv8 family)
  - YOLOv8n (nano) and YOLOv8s (small) were used for object localization experiments. Rationale: detection can identify multiple objects and enable cropping + classification pipelines.
  - Findings: YOLOv8 variants gave good localization accuracy, but full real-time inference on CPU was costly. On GPU, results were promising for throughput.

- Pure classification options (transfer learning)
  - MobileNetV3 (transfer learning) chosen as final classifier: favorable speed on CPU + good accuracy when fine-tuned.
  - EfficientNetV2/Vb3 variants were tested to measure accuracy gains; they improved offline metrics but increased inference time and model size, making them less suitable for CPU-only deployments.
  - Simple custom CNNs were useful as baselines to validate pipeline and sanity-check data.

Model selection criteria:
- Real-time latency (target: sub-300ms inference on server CPU if possible)
- Classification accuracy on held-out validation sets
- Model size and memory footprint (for deployment)
- Ease of export to `.h5` / SavedModel or TFLite

## 4. Experimental Design & Training Configuration

### Typical training pipeline
1. Prepare dataset splits with stratified sampling when possible (train/val/test e.g., 80/10/10)
2. Apply on-the-fly augmentations in training data loader
3. Use a transfer-learning backbone initialized with ImageNet weights
4. Train with cross-entropy (or focal loss for strong imbalance) and monitor validation metrics
5. Use callbacks: EarlyStopping (patience 6-10), ReduceLROnPlateau or cosine annealing schedule

### Example hyperparameters (typical)
- Batch size: 16-64 (GPU); 8-16 for CPU-constrained environments
- Epochs: 20-80 (early stopping normally stops earlier)
- Optimizer: AdamW or SGD with momentum
- Initial LR: 1e-3 (head), 1e-4 (fine-tune) with decay
- Input size: 224x224 for classification models; 416/640 for YOLO detection experiments

### Augmentation details
- Geometric: random horizontal/vertical flips, rotations up to ±15°, random crops
- Photometric: brightness/contrast, color jitter, blur, Gaussian noise
- Advanced: Cutout/MixUp for regularization on mixed-source data

### Metrics & logging
- Track: validation accuracy, per-class precision & recall, F1-score, confusion matrix
- Log: training/validation loss curves, per-epoch metrics, and sample-wise misclassification lists
- Tools: TensorBoard or Weights & Biases (optional for experiment tracking)

## 5. Observations & Results (qualitative)

- Merging datasets increased validation set coverage and reduced overfitting to a single dataset, improving offline metrics in many experiments.
- Class imbalance remained a significant issue for rare classes (e.g., cardboard in some sources). Oversampling and stronger augmentation helped but introduced risk of overfitting to augmented artifacts.
- Domain gap: images coming from ESP32-CAM (low-res, constrained viewpoint, variable lighting) differed significantly from many web/GPU-collected datasets. This caused a drop in real-time accuracy vs. offline validation.
- Detection + classification pipelines (YOLO → crop → classifier) improved accuracy in frames with multiple objects, but added latency and complexity.

## 6. Deployment Considerations & Real-time Constraints

- Target inference environment: Django server (CPU-bound) that receives frames or captures from ESP32-CAM stream.
- Optimization options:
  - Model quantization (post-training, e.g., TFLite int8) to reduce latency and memory.
  - Use TFLite or ONNX runtime for faster CPU inference.
  - Edge acceleration (Coral Edge TPU, NPU) if deploying at scale.
- Fallback policies:
  - If classifier confidence < threshold (e.g., 0.7), classify as `trash` or prompt for manual/hold processing.
  - Combine temporal smoothing: require N consecutive frames with same label to accept automatic sorting.

## 7. Reproducibility & Code Organization

- Keep training notebooks and final scripts in `notebooks/` and `training/` folders with `requirements.txt` or `environment.yml`.
- Save model checkpoints and export final artifacts in `models/` with clear naming and metadata (training data sources, date, validation metrics).
- Provide a short README with commands to reproduce training and inference steps.

## 8. Recommendations & Next Steps (Actionable)

1. Run an on-site data collection campaign: record hundreds to thousands of labeled frames from the ESP32-CAM under target lighting and placement conditions.
2. Create a small, curated fine-tuning set and fine-tune the MobileNetV3 model on that distribution.
3. Implement quantization and test inference latency using TFLite / ONNX on the target server.
4. Optionally prototype a YOLOv8n detection + classifier pipeline and measure end-to-end latency on target hardware.
5. Establish continuous metrics logging (per-frame confidence, per-class error rates) to support iterative improvements.

## Appendix: Example training command (Keras)

This is a canonical example — adapt paths and hyperparameters to your environment.

```bash
python training/train_classifier.py \
  --data_dir data/merged_dataset \
  --model_name MobileNetV3_small_100 \
  --batch_size 32 \
  --img_size 224 \
  --epochs 40 \
  --lr 1e-4 \
  --output_dir models/waste_mobilenetv3
```

---

Document last updated: November 13, 2025
