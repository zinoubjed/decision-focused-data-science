# Benchmark contract and complexity decision

Use the sklearn-bundled UCI optical digits subset, 1,797 images of 8×8 intensities, classes 0–9. Scale fixed physical range by 16; no fitted preprocessing sees test data. Stratified seed-42 split: 1,078 train, 359 validation, 360 test. This is image-level random stratification, not the original UCI writer-independent protocol.

Baseline: training-only StandardScaler and C=1 logistic regression. TensorFlow: 64-ReLU, dropout .2, 32-ReLU, 10-softmax, 6,570 parameters; Adam .001, batch 64, <=60 epochs. Early stopping monitors validation loss, patience 6, restoring best weights. Seeds 42/43/44 use one shared fixed split; report all runs rather than selecting a lucky test seed.

Record training/validation learning history, fit times, validation accuracy and held-out accuracy/macro-F1/log-loss. Final-epoch history may differ from evaluation after restored best weights. A retained-network decision requires mean validation accuracy >= logistic baseline +1 percentage point. This declared complexity hurdle is illustrative, not a universal economic optimum; test metrics do not choose the model.

This run retains logistic regression. Small test improvements from the MLP are insufficient under the validation rule and carry substantially more fitting cost. No GPU, deployment, industrial gain or general deep-learning superiority is claimed. Version/CPU floating arithmetic may prevent bitwise-identical reruns; seeds and deterministic-operation settings are recorded.
