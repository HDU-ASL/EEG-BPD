# EEG-BPD

EEG-BPD is a PyTorch project for joint EEG-image learning on pose regression tasks. The codebase trains a bimodal model that uses EEG signals together with RGB images to predict 6-DoF camera pose-related targets.

## Overview

The main training pipeline combines:

- An EEG encoder (`EEGNet`) for reshaped EEG sequences
- A ResNet34-based image encoder for RGB frames
- A bimodal common/private representation model (`BMCL`)
- Pose regression losses for translation and rotation

The current default training entry uses the `desk1` setting through `data_loader7()` in [data_loader.py](/mnt/HYX/EEG-BPD-main/data_loader.py:851).

## Project Structure

- [train.py](/mnt/HYX/EEG-BPD-main/train.py:1): main training entry
- [train_map.py](/mnt/HYX/EEG-BPD-main/train_map.py:1): map-oriented training entry
- [config.py](/mnt/HYX/EEG-BPD-main/config.py:1): runtime configuration and CLI args
- [data_loader.py](/mnt/HYX/EEG-BPD-main/data_loader.py:1): dataset assembly and train/test split logic
- [model.py](/mnt/HYX/EEG-BPD-main/model.py:1): EEG encoder, image encoder, and `BMCL`
- [solver.py](/mnt/HYX/EEG-BPD-main/solver.py:1): training loop and evaluation
- [EEG_reshape.py](/mnt/HYX/EEG-BPD-main/EEG_reshape.py:1): EEG preprocessing helpers
- [utils](/mnt/HYX/EEG-BPD-main/utils): losses and training utilities

## Environment

Recommended Python version:

- Python 3.9+

Core dependencies used by the repository:

- `torch`
- `torchvision`
- `numpy`
- `scipy`
- `pandas`
- `opencv-python`
- `Pillow`
- `matplotlib`
- `scikit-learn`
- `einops`
- `transforms3d`

Example installation:

```bash
pip install torch torchvision numpy scipy pandas opencv-python pillow matplotlib scikit-learn einops transforms3d
```

## Data Layout

The current code uses local absolute paths in several places. By default, `data_loader7()` expects data similar to:

```text
/mnt/HYX/
├── EEG-BPD-main/
├── TEST/
├── 实验五/Subject05/NP/sub05_seq_100.mat
└── rgbd_dataset_freiburg1_desk/
    ├── groundtruth.txt
    ├── rgb.txt
    └── rgb/
        ├── test1(1).png
        ├── test1(2).png
        └── ...
```

Files used by the current default loader:

- EEG file: `/mnt/HYX/实验五/Subject05/NP/sub05_seq_100.mat`
- Ground truth: `/mnt/HYX/rgbd_dataset_freiburg1_desk/groundtruth.txt`
- RGB timestamps: `/mnt/HYX/rgbd_dataset_freiburg1_desk/rgb.txt`
- RGB frames: `/mnt/HYX/rgbd_dataset_freiburg1_desk/rgb/test1(1).png` ... `test1(500).png`
- Split files: `train_indices.csv` and `test_indices.csv` under `opt.facial_splits_path` or `/mnt/HYX/TEST`

## Training

Run the default training script:

```bash
python train.py
```

The training script:

- sets random seed to `42`
- builds train/val/test configs from [config.py](/mnt/HYX/EEG-BPD-main/config.py:46)
- loads data through `get_loader()`
- builds the `BMCL` model
- starts training through `Solver.train()`

## Important Configuration

Useful arguments defined in [config.py](/mnt/HYX/EEG-BPD-main/config.py:64):

- `--subject`: subject id, `0` means all subjects
- `--time_low`: EEG crop lower bound
- `--time_high`: EEG crop upper bound
- `--facial-splits-path`: directory containing `train_indices.csv` and `test_indices.csv`
- `--batch_size`: default `32`
- `--n_epoch`: default `3000`
- `--learning_rate`: default `0.0005`
- `--model`: default `BMCL`

Example:

```bash
python train.py --batch_size 16 --n_epoch 100 --learning_rate 1e-4 --facial-splits-path /mnt/HYX/TEST/
```

## Outputs

During training, the current solver writes artifacts to hardcoded paths:

- model weights: `/home/hyx/test/BCML/models/`
- logs: `/home/hyx/test/BCML/SAVE/`
- predicted/target poses: `/home/hyx/test/BCML/memory/`

If these directories do not exist on your machine, either create them first or update the save paths in [solver.py](/mnt/HYX/EEG-BPD-main/solver.py:120).

## Notes

- The repository currently relies on several absolute filesystem paths. Porting to another machine will be easier if these paths are moved into config arguments.
- `data_loader7()` now auto-generates `train_indices.csv` and `test_indices.csv` if they are missing.
- The current default branch of the pipeline is focused on the `desk1` experiment setup.

## GitHub

Suggested remote for this local repository:

```bash
git remote add origin git@github.com:HDU-ASL/EEG-BPD.git
```

If `origin` already exists, update it with:

```bash
git remote set-url origin git@github.com:HDU-ASL/EEG-BPD.git
```
