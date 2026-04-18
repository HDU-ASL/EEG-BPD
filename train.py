# Imports
import numpy as np
from config import get_config
from data_loader import get_loader
from solver import Solver

import torch


if __name__ == '__main__':
    random_seed = 42
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(random_seed)

    task = 'facial'
    train_config = get_config(mode='train', task=task)
    dev_config = get_config(mode='val', task=task)
    test_config = get_config(mode='test', task=task)

    train_data_loader, test_data_loader = get_loader(train_config)
    dev_data_loader = test_data_loader

    solver = Solver(
        train_config,
        dev_config,
        test_config,
        train_data_loader,
        dev_data_loader,
        test_data_loader,
        is_train=True,
    )
    solver.build()
    solver.train()
